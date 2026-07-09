---
name: oracle-review-loop
description: This skill should be used when running Oracle creator/evaluator review loops with fixed chat threads, a user-approved 100-point rubric, and repeated improvement until PASS.
---

# Skill: oracle-review-loop

Oracle を使って、作成者スレッドと評価者スレッドを固定した反復レビューを行う。評価基準は作業開始前に提示し、ユーザー確認後に固定する。

## 使う場面

- ユーザーが「Oracleで100点まで回す」「評価者と作成者を分ける」「同じチャットスレッドを使い続ける」と依頼したとき。
- 研究計画、README、設計書、提案書などを、明示 rubric に基づいて段階的に改善したいとき。
- 評価基準そのものを Oracle に作らせたいが、ループ中に基準を動かしたくないとき。

## 原則

- Oracle prompt と添付計画は、まずグローバル skill `/Users/koki/.codex/skills/oracle-prompt-design/SKILL.md` に従って設計する。
- skill は「毎回読む長いログ」ではなく、必要時に読む手順・コード・参照の束として保つ。
- まずゴールと100点満点の評価基準を分ける。
- 100点満点の評価基準を作る前に、対象が AI、agent、知識管理、レビュー、自動化、研究支援に関係する場合は、OpenAI 公式情報と最新の agent 研究で評価軸を更新する。
- 評価基準が未定なら、`--derive-rubric` で作成して停止し、ユーザーに提示する。
- ユーザーが確認・編集した rubric だけを固定基準として使う。
- ループ開始後に rubric を変更しない。変更する場合は新しいループとして開始する。
- 作成者と評価者は別々の Oracle session とし、以後は `--followup` で同じチャットスレッドを使い続ける。
- Oracle 出力は助言扱いとし、最終採用前に対象ファイルと検証コマンドで確認する。
- ループ後に残すのは、全文 transcript ではなく「再利用可能な手順」「失敗パターン」「rubric 改善」だけに蒸留する。
- この skill 自体を会話履歴や反復失敗から更新する場合は、グローバル skill `/Users/koki/.codex/skills/skill-improver/SKILL.md` を使う。

## デフォルト手順

1. `oracle-prompt-design` で Oracle を使う妥当性、prompt、添付計画を設計する。
2. Attach / Exclude / Missing を明示し、送信範囲を最小化する。
3. 評価基準を作る前に、必要なら OpenAI 公式情報と最新 agent 研究から評価軸を更新し、根拠と推論を分ける。
4. 明示 rubric がなければ `--derive-rubric` で生成して止める。
5. 生成された `00-rubric.md` をユーザーに提示し、確認・編集してもらう。
6. 固定 rubric で `/Users/koki/.codex/skills/oracle-review-loop/scripts/oracle_review_loop.py` を実行する。
7. 評価者が `FINAL_DECISION: PASS` を返したら停止する。
8. 最終出力を人間側で確認し、必要なファイル編集と検証を別途行う。
9. 同じ失敗や改善が再発しそうなら、`skill-improver` で transcript 全体ではなく短い教訓として反映する。

## 安全ゲート

- private vault 内容、秘密情報、個人情報、未公開研究情報を送る前に、送信対象を明示して承認を取る。
- 実行前に必要なら `oracle --dry-run summary --files-report ...` で送信候補を確認する。
- API engine はコストが発生するため、明示承認なしに使わない。
- 待機ジッターは負荷低減のために使う。検知回避を目的にしない。

## 参照

- 実行例と再開手順: `references/oracle-review-loop-runbook.md`
- Prompt と添付計画: `/Users/koki/.codex/skills/oracle-prompt-design/SKILL.md`
- Skill 改善手順: `/Users/koki/.codex/skills/skill-improver/SKILL.md`
- 実装スクリプト: `/Users/koki/.codex/skills/oracle-review-loop/scripts/oracle_review_loop.py`
