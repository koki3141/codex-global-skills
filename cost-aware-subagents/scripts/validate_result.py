#!/usr/bin/env python3
"""Validate a cost-aware-subagents result JSON using only the standard library."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

STATUSES = {"done", "blocked", "uncertain"}
SEVERITIES = {"critical", "high", "medium", "low", "info"}
TEST_RESULTS = {"pass", "fail", "not_run"}
REQUIRED = {
    "task_id",
    "status",
    "summary",
    "findings",
    "artifacts",
    "tests",
    "open_questions",
    "recommended_next_action",
}


def fail(message: str) -> None:
    raise ValueError(message)


def require_type(value: Any, expected: type, path: str) -> None:
    if not isinstance(value, expected):
        fail(f"{path} must be {expected.__name__}, got {type(value).__name__}")


def validate(data: Any) -> None:
    require_type(data, dict, "root")
    missing = REQUIRED - set(data)
    if missing:
        fail(f"missing required keys: {', '.join(sorted(missing))}")

    for key in ("task_id", "status", "summary", "recommended_next_action"):
        require_type(data[key], str, key)

    if not data["task_id"].strip():
        fail("task_id must not be empty")
    if data["status"] not in STATUSES:
        fail(f"status must be one of {sorted(STATUSES)}")

    for key in ("artifacts", "open_questions"):
        require_type(data[key], list, key)
        if not all(isinstance(item, str) for item in data[key]):
            fail(f"every {key} item must be a string")

    require_type(data["findings"], list, "findings")
    for index, finding in enumerate(data["findings"]):
        path = f"findings[{index}]"
        require_type(finding, dict, path)
        required = {"claim", "evidence", "severity", "confidence"}
        missing = required - set(finding)
        if missing:
            fail(f"{path} missing keys: {', '.join(sorted(missing))}")
        require_type(finding["claim"], str, f"{path}.claim")
        require_type(finding["evidence"], list, f"{path}.evidence")
        if not all(isinstance(item, str) for item in finding["evidence"]):
            fail(f"every {path}.evidence item must be a string")
        if finding["severity"] not in SEVERITIES:
            fail(f"{path}.severity must be one of {sorted(SEVERITIES)}")
        confidence = finding["confidence"]
        if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
            fail(f"{path}.confidence must be numeric")
        if not 0 <= float(confidence) <= 1:
            fail(f"{path}.confidence must be between 0 and 1")
        if finding["severity"] in {"critical", "high", "medium"} and not finding["evidence"]:
            fail(f"{path} needs evidence for material severity")

    require_type(data["tests"], list, "tests")
    for index, test in enumerate(data["tests"]):
        path = f"tests[{index}]"
        require_type(test, dict, path)
        required = {"command", "result", "evidence"}
        missing = required - set(test)
        if missing:
            fail(f"{path} missing keys: {', '.join(sorted(missing))}")
        require_type(test["command"], str, f"{path}.command")
        require_type(test["evidence"], str, f"{path}.evidence")
        if test["result"] not in TEST_RESULTS:
            fail(f"{path}.result must be one of {sorted(TEST_RESULTS)}")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} RESULT.json", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        validate(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
