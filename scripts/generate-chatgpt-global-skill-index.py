#!/usr/bin/env python3
"""Generate chatgpt-global-skill-index.md from active global Codex skills."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "chatgpt-global-skill-index.md"
REPO_URL = "https://github.com/koki3141/codex-global-skills"
BRANCH = "main"


def active_skill_paths() -> list[Path]:
    return sorted(
        path
        for path in ROOT.glob("*/SKILL.md")
        if path.parent.name not in {".system", "backup"}
    )


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    try:
        raw_frontmatter = text.split("\n---\n", 1)[0].removeprefix("---\n")
    except IndexError:
        return {}

    data: dict[str, str] = {}
    for line in raw_frontmatter.splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")
    return data


def table_cell(text: str) -> str:
    return " ".join(text.split()).replace("|", "\\|")


def render() -> str:
    rows: list[str] = []
    for skill_path in active_skill_paths():
        rel_path = skill_path.relative_to(ROOT).as_posix()
        frontmatter = parse_frontmatter(skill_path.read_text(encoding="utf-8"))
        name = frontmatter.get("name") or skill_path.parent.name
        description = frontmatter.get("description") or "Skill手順を参照する。"
        url = f"{REPO_URL}/blob/{BRANCH}/{rel_path}"
        rows.append(
            f"| `{table_cell(name)}` | {table_cell(description)} | [SKILL.md]({url}) |"
        )

    table_rows = "\n".join(rows)
    return f"""---
title: ChatGPT Global Skill Index
date: 2026-07-09
tags:
  - status/evergreen
  - type/index
  - domain/external-brain
  - domain/agent
aliases:
  - ChatGPT global skills
  - Codex global skills
github_url: {REPO_URL}/blob/{BRANCH}/chatgpt-global-skill-index.md
raw_url: https://raw.githubusercontent.com/koki3141/codex-global-skills/{BRANCH}/chatgpt-global-skill-index.md
---

# ChatGPT Global Skill Index

## 役割

このファイルは、ChatGPT WebからグローバルCodex skillを参照するための公開索引である。

## GitHubリンク

- 表示用: [chatgpt-global-skill-index.md]({REPO_URL}/blob/{BRANCH}/chatgpt-global-skill-index.md)
- 読み取り用: [raw Markdown](https://raw.githubusercontent.com/koki3141/codex-global-skills/{BRANCH}/chatgpt-global-skill-index.md)

## Webでの利用ルール

1. ユーザーの依頼が下のSkillの説明に合う場合、該当する `SKILL.md` を読む。
2. `SKILL.md` に相対パスの `references/`、`scripts/`、`templates/`、`assets/` が出る場合、必要なものだけ追加で読む。
3. ローカル実行、Git操作、CLI、ファイル編集が必要な手順は、実行したふりをしない。
4. Webから読めないファイルや未公開ファイルが必要な場合は、必要な添付、コマンド、確認条件として明示する。
5. 複数Skillが該当する場合は、最小セットを選び、適用順を短く示してから作業する。

## Skill一覧

| Skill | 使う場面 | 参照 |
|---|---|---|
{table_rows}
"""


def main() -> int:
    OUTPUT.write_text(render(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
