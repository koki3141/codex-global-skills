---
name: claim-calibration
description: Use this skill before finalizing any answer that includes uncertain conclusions, investigation results, debugging conclusions, root cause claims, data quality judgments, historical claims, or statements about absence, completeness, origin, or correctness.
---

# Claim Calibration Skill

## Purpose

Match the strength of the answer to the strength of the evidence.

## Claim Strength Levels

### Level 0: Observation
Directly seen.
- *Example*: "このログには `Permission denied` が出ています。"

### Level 1: Bounded Observation
Directly seen within a scope.
- *Example*: "現在のブランチでは、このファイルは見つかりません。"

### Level 2: Inference
Likely, but not directly proven.
- *Example*: "権限設定が原因である可能性が高いです。"

### Level 3: Strong Conclusion
Well-supported after checking alternatives.
- *Example*: "この環境では、権限不足が失敗原因です。"

### Level 4: Global Conclusion
Broad and risky.
- *Example*:
  - "このファイルは存在しません。"
  - "元々こうでした。"
  - "完全に復元できました。"

## Rule

Do not output Level 4 claims unless the evidence gate was passed.

---

## Required Phrasing

Use:
- 確認できた範囲では
- 現時点の証拠では
- この探索範囲では
- 有力な仮説は
- まだ未確認です
- 完全性は保証できません

Avoid:
- 確実に
- 間違いなく
- 元々
- 完全に
- 存在しない
- これで確定

## Final Check

Before final answer, rewrite every strong claim into one of:
- Confirmed Fact
- Inference
- Unknown

If a sentence does not fit one of these categories, weaken it or remove it.
