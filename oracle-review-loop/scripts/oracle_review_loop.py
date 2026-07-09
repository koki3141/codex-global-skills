#!/usr/bin/env python3
"""Run a two-thread Oracle creator/evaluator loop until the evaluator passes it."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import random
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path


PASS_PHRASE = "100点満点です。合格です。終了してください"
PASS_MARKER = "FINAL_DECISION: PASS"
REVISE_MARKER = "FINAL_DECISION: REVISE"
UTC = getattr(dt, "UTC", dt.timezone.utc)


def utc_now_iso() -> str:
    return dt.datetime.now(UTC).isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Keep one Oracle creator thread and one Oracle evaluator thread, "
            "passing outputs between them until the evaluator returns PASS."
        )
    )
    parser.add_argument("--goal", required=True, help="The explicit goal the creator must satisfy.")
    parser.add_argument(
        "--rubric",
        action="append",
        default=[],
        help="A 100-point evaluation criterion. Repeatable; combined with --rubric-file.",
    )
    parser.add_argument(
        "--rubric-file",
        action="append",
        default=[],
        type=Path,
        help="Markdown/text file defining the 100-point evaluation criteria. Repeatable.",
    )
    parser.add_argument(
        "--derive-rubric",
        action="store_true",
        help="Ask Oracle to create a 100-point rubric, save it, and stop for review by default.",
    )
    parser.add_argument(
        "--approve-derived-rubric",
        action="store_true",
        help="Continue into the creator/evaluator loop immediately after deriving the rubric.",
    )
    parser.add_argument("--rubric-slug", help="Slug for the rubric-design thread when deriving a rubric.")
    parser.add_argument(
        "--file",
        action="append",
        default=[],
        dest="files",
        help="Context file, directory, or glob to attach to every Oracle call. Repeatable.",
    )
    parser.add_argument(
        "--state",
        type=Path,
        default=Path(".oracle-review-loop-state.json"),
        help="JSON state file storing the fixed creator/evaluator session ids.",
    )
    parser.add_argument(
        "--run-dir",
        type=Path,
        default=None,
        help="Directory for generated creator/evaluator markdown outputs.",
    )
    parser.add_argument("--creator-session", help="Existing creator Oracle session id/slug.")
    parser.add_argument("--evaluator-session", help="Existing evaluator Oracle session id/slug.")
    parser.add_argument(
        "--creator-browser-tab",
        help="Existing ChatGPT conversation URL/tab ref to use when resuming the creator thread.",
    )
    parser.add_argument(
        "--evaluator-browser-tab",
        help="Existing ChatGPT conversation URL/tab ref to use when resuming the evaluator thread.",
    )
    parser.add_argument("--last-creator-output", help="Last creator output markdown when resuming manually.")
    parser.add_argument("--last-evaluator-output", help="Last evaluator output markdown when resuming manually.")
    parser.add_argument("--creator-slug", help="Slug for the creator thread when initializing.")
    parser.add_argument("--evaluator-slug", help="Slug for the evaluator thread when initializing.")
    parser.add_argument("--model", default="gpt-5.5-pro", help="Oracle model label/id.")
    parser.add_argument("--engine", default="browser", choices=["browser", "api"], help="Oracle engine.")
    parser.add_argument("--timeout", default="60m", help="Oracle timeout per call.")
    parser.add_argument("--max-rounds", type=int, default=1000, help="Maximum revision/evaluation rounds.")
    parser.add_argument(
        "--delay-min-seconds",
        type=float,
        default=0.0,
        help="Minimum polite delay before each Oracle call; 0 allows immediate calls.",
    )
    parser.add_argument(
        "--delay-max-seconds",
        type=float,
        default=600.0,
        help="Maximum polite delay before each Oracle call.",
    )
    parser.add_argument(
        "--delay-distribution",
        choices=["power-law", "exponential", "uniform", "none"],
        default="power-law",
        help="Delay distribution for spacing Oracle calls. Use none to disable.",
    )
    parser.add_argument(
        "--delay-power-alpha",
        type=float,
        default=1.8,
        help="Shape parameter for bounded power-law delays; larger values favor shorter waits.",
    )
    parser.add_argument(
        "--oracle-bin",
        default=None,
        help="Path to the oracle binary. Defaults to PATH lookup, then ~/Library/pnpm/oracle.",
    )
    parser.add_argument(
        "--no-manual-login",
        action="store_true",
        help="Do not pass browser manual-login flags.",
    )
    parser.add_argument(
        "--no-bundle-files",
        action="store_true",
        help="Do not ask Oracle browser mode to bundle attachments.",
    )
    parser.add_argument(
        "--browser-attachments",
        choices=["auto", "never", "always"],
        default=None,
        help="Pass through Oracle browser attachment mode.",
    )
    parser.add_argument(
        "--browser-attachment-timeout",
        help="Pass through Oracle browser attachment timeout, e.g. 180000.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print commands and write no Oracle outputs or state.",
    )
    parser.add_argument(
        "--force-new",
        action="store_true",
        help="Ignore existing state and initialize two new Oracle threads.",
    )
    return parser.parse_args()


def slugify(text: str, *, max_words: int = 3) -> str:
    asciiish = re.sub(r"[^A-Za-z0-9]+", " ", text).strip().lower()
    words = asciiish.split()
    if len(words) >= 2:
        return "-".join(words[:max_words])
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:8]
    return f"oracle-loop-{digest}"


def resolve_oracle_bin(value: str | None) -> str:
    if value:
        return value
    found = shutil.which("oracle")
    if found:
        return found
    fallback = Path.home() / "Library" / "pnpm" / "oracle"
    if fallback.exists():
        return str(fallback)
    raise SystemExit("oracle binary not found on PATH or at ~/Library/pnpm/oracle")


def read_state(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_rubric_state(args: argparse.Namespace, state: dict, run_dir: Path) -> None:
    state.update(
        {
            "created_at": state.get("created_at", utc_now_iso()),
            "goal": args.goal,
            "rubric": args.rubric_text,
            "rubric_output": getattr(args, "rubric_output", None),
            "run_dir": str(run_dir),
            "rubric_review_required": True,
        }
    )
    if not args.dry_run:
        write_state(args.state, state)


def oracle_base(args: argparse.Namespace, *, browser_tab: str | None = None) -> list[str]:
    cmd = [
        args.oracle_bin,
        "--engine",
        args.engine,
        "--model",
        args.model,
        "--timeout",
        args.timeout,
        "--wait",
        "--no-notify",
    ]
    if args.engine == "browser" and not args.no_manual_login:
        cmd.extend(["--browser-manual-login", "--browser-input-timeout", "120000"])
    if args.engine == "browser" and not args.no_bundle_files:
        cmd.append("--browser-bundle-files")
    if args.engine == "browser":
        cmd.extend(["--browser-archive", "never"])
        if args.browser_attachments:
            cmd.extend(["--browser-attachments", args.browser_attachments])
        if args.browser_attachment_timeout:
            cmd.extend(["--browser-attachment-timeout", args.browser_attachment_timeout])
        if browser_tab:
            cmd.extend(["--browser-tab", browser_tab])
    return cmd


def add_files(cmd: list[str], files: list[str]) -> list[str]:
    for file_arg in files:
        cmd.extend(["--file", file_arg])
    return cmd


def polite_delay_seconds(args: argparse.Namespace) -> float:
    if args.delay_distribution == "none":
        return 0.0
    min_seconds = float(args.delay_min_seconds)
    max_seconds = float(args.delay_max_seconds)
    if min_seconds < 0 or max_seconds < 0:
        raise SystemExit("Delay bounds must be non-negative.")
    if max_seconds < min_seconds:
        raise SystemExit("--delay-max-seconds must be >= --delay-min-seconds.")
    if max_seconds == min_seconds:
        return min_seconds

    rng = random.SystemRandom()
    if args.delay_distribution == "uniform":
        return rng.uniform(min_seconds, max_seconds)
    if args.delay_distribution == "exponential":
        span = max_seconds - min_seconds
        raw = rng.expovariate(1.0)
        return min_seconds + min(raw / 4.0, 1.0) * span

    alpha = float(args.delay_power_alpha)
    if alpha <= 0:
        raise SystemExit("--delay-power-alpha must be > 0.")
    lower = min_seconds
    upper = max_seconds
    if lower == 0:
        # Pareto-style bounded sampling needs a positive lower bound.
        lower = 0.001
    u = rng.random()
    lower_term = lower ** (-alpha)
    upper_term = upper ** (-alpha)
    return (lower_term - u * (lower_term - upper_term)) ** (-1.0 / alpha)


def wait_before_oracle(args: argparse.Namespace) -> None:
    seconds = polite_delay_seconds(args)
    if seconds <= 0:
        return
    print(f"[delay] Waiting {seconds:.1f}s before Oracle call.", flush=True)
    if not args.dry_run:
        time.sleep(seconds)


def run_command(cmd: list[str], *, args: argparse.Namespace) -> None:
    wait_before_oracle(args)
    print("$ " + " ".join(shell_quote(part) for part in cmd), flush=True)
    if args.dry_run:
        return
    completed = subprocess.run(cmd, text=True)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def shell_quote(value: str) -> str:
    if re.fullmatch(r"[A-Za-z0-9_./:=@%+,-]+", value):
        return value
    return "'" + value.replace("'", "'\"'\"'") + "'"


def read_output(path: Path, *, dry_run: bool) -> str:
    if dry_run:
        return ""
    if not path.exists():
        raise SystemExit(f"Expected Oracle output was not written: {path}")
    return path.read_text(encoding="utf-8", errors="replace")


def load_rubric(inline_items: list[str], rubric_files: list[Path]) -> str:
    parts: list[str] = []
    for index, item in enumerate(inline_items, start=1):
        stripped = item.strip()
        if stripped:
            parts.append(f"### Inline criterion {index}\n{stripped}")
    for path in rubric_files:
        if not path.exists():
            raise SystemExit(f"Rubric file not found: {path}")
        text = path.read_text(encoding="utf-8", errors="replace").strip()
        if text:
            parts.append(f"### Rubric file: {path}\n{text}")
    return "\n\n".join(parts).strip()


def has_passed(evaluator_output: str) -> bool:
    stripped_lines = [line.strip() for line in evaluator_output.splitlines() if line.strip()]
    return bool(
        stripped_lines
        and stripped_lines[-1] == PASS_MARKER
        and PASS_PHRASE in evaluator_output
    )


def quality_contract(goal: str, rubric: str) -> str:
    return f"""ゴール:
{goal}

100点満点の評価基準:
{rubric}
"""


def rubric_prompt(goal: str) -> str:
    return f"""あなたは評価設計者です。

ゴール:
{goal}

添付ファイルを読み、このゴールに対する「100点満点の評価基準」を作成してください。

要件:
- 100点満点の評価基準を作る前に、評価軸を更新してください。特にゴールが AI、agent、知識管理、レビュー、自動化、研究支援に関係する場合は、OpenAI 公式情報と最新の agent 研究を一次情報として確認し、rubric に反映してください。
- 外部調査できない場合は、その制約を明記し、添付ファイルだけに基づく暫定rubricであることを出力してください。
- 直接の根拠とあなたの推論を分け、参照した公式資料や論文を短く列挙してください。
- 100点とは何が満たされた状態かを、評価者と作成者が同じ意味で使えるように定義してください。
- 評価基準は、ゴール達成に必要な観点だけに限定してください。
- 好み、スコープ拡大、追加実験、追加機能などを、必須基準に混ぜないでください。
- 可能なら配点合計が100点になるようにしてください。
- 各観点について、満点条件、減点条件、失格条件を明記してください。
- 最後に「このrubricは以後の評価ループで固定し、途中で変更しない」と明記してください。

出力は、そのまま固定rubricとして保存できるMarkdownにしてください。
"""


def creator_initial_prompt(goal: str, rubric: str) -> str:
    return f"""あなたは作成者です。

{quality_contract(goal, rubric)}

添付ファイルを読み、ゴールを満たす初稿を作成してください。
出力は、そのまま評価者に渡されます。
100点満点の評価基準をすべて満たすことを明示的に意識してください。
制約、前提、未解決点がある場合も、最終成果物として読める形に統合してください。
"""


def creator_revision_prompt(goal: str, rubric: str) -> str:
    return f"""あなたは作成者です。

{quality_contract(goal, rubric)}

添付された評価者の出力を読み、100点満点となる修正をしてください。
評価者の指摘に逐条反応するだけでなく、最終成果物として一貫する形に統合してください。
100点満点の評価基準をすべて満たすように、足りない根拠、構造、制約、表現を補ってください。
出力は、修正後の成果物本文を中心にしてください。
"""


def evaluator_prompt(goal: str, rubric: str) -> str:
    return f"""あなたは評価者です。

{quality_contract(goal, rubric)}

添付された作成者の出力を100点満点で評価し、100点満点となる改善案を示してください。
評価は上記の「100点満点の評価基準」に限定してください。
基準にない好み、追加要求、スコープ拡大を減点理由にしないでください。
逆に、基準の一部でも未達、不明、根拠不足、矛盾、実行不能があれば100点満点にしないでください。

出力には必ず次を含めてください。
1. Score: N/100
2. 100/100 かどうか
3. 評価基準ごとの合否と減点理由
4. 100点満点となるための最小修正案

100点満点と評価できる場合は、必ず本文中に次の文をそのまま出力してください。
{PASS_PHRASE}

さらに、100点満点と評価できる場合は、回答の最後の非空行に必ず次を単独で出力してください。
{PASS_MARKER}

100点未満の場合は、回答の最後の非空行に必ず次を単独で出力してください。
{REVISE_MARKER}

採点は甘くしないでください。ただし、ゴール達成に不要な追加要求は減点理由にしないでください。
"""


def output_path(run_dir: Path, role: str, round_index: int) -> Path:
    return run_dir / f"{round_index:02d}-{role}.md"


def call_new_session(
    args: argparse.Namespace,
    *,
    slug: str,
    prompt: str,
    output: Path,
    files: list[str],
    browser_tab: str | None = None,
) -> None:
    cmd = oracle_base(args, browser_tab=browser_tab)
    cmd.extend(["--slug", slug, "--write-output", str(output), "-p", prompt])
    add_files(cmd, files)
    run_command(cmd, args=args)


def call_followup(
    args: argparse.Namespace,
    *,
    session_id: str,
    prompt: str,
    output: Path,
    files: list[str],
    browser_tab: str | None = None,
) -> None:
    cmd = oracle_base(args, browser_tab=browser_tab)
    cmd.extend(["--followup", session_id, "--write-output", str(output), "-p", prompt])
    add_files(cmd, files)
    run_command(cmd, args=args)


def derive_rubric(args: argparse.Namespace, run_dir: Path) -> tuple[str, Path]:
    base_slug = slugify(args.goal)
    rubric_output = run_dir / "00-rubric.md"
    rubric_session = args.rubric_slug or f"{base_slug}-rubric"
    call_new_session(
        args,
        slug=rubric_session,
        prompt=rubric_prompt(args.goal),
        output=rubric_output,
        files=args.files,
    )
    if args.dry_run:
        return (
            "DRY RUN: rubric will be generated by Oracle and frozen in 00-rubric.md.",
            rubric_output,
        )
    return read_output(rubric_output, dry_run=False).strip(), rubric_output


def initialize_state(args: argparse.Namespace, state: dict, run_dir: Path) -> dict:
    base_slug = slugify(args.goal)
    creator_session = args.creator_session or state.get("creator_session")
    evaluator_session = args.evaluator_session or state.get("evaluator_session")

    if creator_session and evaluator_session and not args.force_new:
        state.update(
            {
                "creator_session": creator_session,
                "evaluator_session": evaluator_session,
                "goal": args.goal,
                "rubric": args.rubric_text,
                "rubric_review_required": False,
                "run_dir": str(run_dir),
            }
        )
        if args.last_creator_output:
            state["last_creator_output"] = args.last_creator_output
        if args.last_evaluator_output:
            state["last_evaluator_output"] = args.last_evaluator_output
        if "last_evaluator_output" not in state:
            raise SystemExit(
                "Existing sessions require a state file with last_evaluator_output "
                "or an explicit --last-evaluator-output path."
            )
        return state

    creator_session = args.creator_slug or f"{base_slug}-creator"
    evaluator_session = args.evaluator_slug or f"{base_slug}-evaluator"

    creator_output = output_path(run_dir, "creator", 1)
    call_new_session(
        args,
        slug=creator_session,
        prompt=creator_initial_prompt(args.goal, args.rubric_text),
        output=creator_output,
        files=args.files,
    )

    evaluator_output = output_path(run_dir, "evaluator", 1)
    evaluator_files = [str(creator_output), *args.files]
    call_new_session(
        args,
        slug=evaluator_session,
        prompt=evaluator_prompt(args.goal, args.rubric_text),
        output=evaluator_output,
        files=evaluator_files,
    )

    state.update(
        {
            "created_at": utc_now_iso(),
            "goal": args.goal,
            "rubric": args.rubric_text,
            "rubric_output": getattr(args, "rubric_output", None),
            "rubric_review_required": False,
            "creator_session": creator_session,
            "evaluator_session": evaluator_session,
            "run_dir": str(run_dir),
            "last_round": 1,
            "last_creator_output": str(creator_output),
            "last_evaluator_output": str(evaluator_output),
        }
    )
    if not args.dry_run:
        write_state(args.state, state)
    return state


def main() -> int:
    args = parse_args()
    args.oracle_bin = resolve_oracle_bin(args.oracle_bin)

    if not args.files:
        raise SystemExit("At least one --file is required so Oracle has concrete project context.")
    if args.max_rounds < 1:
        raise SystemExit("--max-rounds must be >= 1")

    state = {} if args.force_new else read_state(args.state)
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    if args.run_dir:
        run_dir = args.run_dir
    elif state.get("run_dir"):
        run_dir = Path(state["run_dir"])
    else:
        run_dir = Path(".oracle-review-loop") / timestamp
    if not args.dry_run:
        run_dir.mkdir(parents=True, exist_ok=True)

    requested_rubric = load_rubric(args.rubric, args.rubric_file)
    stored_rubric = state.get("rubric") if not args.force_new else None
    rubric_review_pending = bool(state.get("rubric_review_required")) and not (
        state.get("creator_session") and state.get("evaluator_session")
    )
    if stored_rubric and not rubric_review_pending:
        if args.derive_rubric:
            raise SystemExit("This loop already has a frozen rubric. Use --force-new to derive a new one.")
        if requested_rubric and requested_rubric != stored_rubric:
            raise SystemExit("This loop already has a frozen rubric. Use --force-new to change it.")
        args.rubric_text = stored_rubric
        args.rubric_output = state.get("rubric_output")
    elif stored_rubric and rubric_review_pending:
        if args.derive_rubric:
            raise SystemExit("A derived rubric is already waiting for review. Rerun without --derive-rubric.")
        rubric_output = state.get("rubric_output")
        if requested_rubric:
            args.rubric_text = requested_rubric
        elif rubric_output and Path(rubric_output).exists():
            args.rubric_text = Path(rubric_output).read_text(encoding="utf-8", errors="replace").strip()
        else:
            args.rubric_text = stored_rubric
        args.rubric_output = rubric_output
    elif requested_rubric:
        args.rubric_text = requested_rubric
        args.rubric_output = None
    elif args.derive_rubric:
        args.rubric_text, rubric_output = derive_rubric(args, run_dir)
        args.rubric_output = str(rubric_output)
        if not args.approve_derived_rubric:
            write_rubric_state(args, state, run_dir)
            print(f"Derived rubric written to: {rubric_output}")
            print(
                "Review or edit the rubric, then rerun without --derive-rubric "
                "to start the fixed creator/evaluator loop."
            )
            return 0
    else:
        raise SystemExit(
            "A 100-point evaluation rubric is required. "
            "Use --rubric, --rubric-file, or --derive-rubric."
        )

    state = initialize_state(args, state, run_dir)

    evaluator_text = read_output(Path(state["last_evaluator_output"]), dry_run=args.dry_run)
    if has_passed(evaluator_text):
        print("Evaluator already returned PASS.")
        return 0

    creator_session = state["creator_session"]
    evaluator_session = state["evaluator_session"]
    start_round = int(state.get("last_round", 1)) + 1

    for round_index in range(start_round, args.max_rounds + 1):
        creator_output = output_path(run_dir, "creator", round_index)
        call_followup(
            args,
            session_id=creator_session,
            prompt=creator_revision_prompt(args.goal, args.rubric_text),
            output=creator_output,
            files=[state["last_evaluator_output"], *args.files],
            browser_tab=args.creator_browser_tab,
        )

        evaluator_output = output_path(run_dir, "evaluator", round_index)
        call_followup(
            args,
            session_id=evaluator_session,
            prompt=evaluator_prompt(args.goal, args.rubric_text),
            output=evaluator_output,
            files=[str(creator_output), *args.files],
            browser_tab=args.evaluator_browser_tab,
        )

        evaluator_text = read_output(evaluator_output, dry_run=args.dry_run)
        state.update(
            {
                "goal": args.goal,
                "rubric": args.rubric_text,
                "rubric_output": getattr(args, "rubric_output", None),
                "rubric_review_required": False,
                "run_dir": str(run_dir),
                "last_round": round_index,
                "last_creator_output": str(creator_output),
                "last_evaluator_output": str(evaluator_output),
                "updated_at": utc_now_iso(),
            }
        )
        if not args.dry_run:
            write_state(args.state, state)

        if has_passed(evaluator_text):
            print(f"Evaluator returned PASS at round {round_index}.")
            return 0

    if args.dry_run:
        print("Dry run complete.")
        return 0

    print(f"Reached --max-rounds={args.max_rounds} without PASS.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
