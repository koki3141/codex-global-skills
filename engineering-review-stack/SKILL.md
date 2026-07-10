---
name: engineering-review-stack
description: このskillは、ユーザーが「開発レビュー・スタックで進めて」「設計、TDD、独立レビュー、最終検証まで通して」と依頼した場合、または重大な複数ファイル変更にユーザー固有の証拠・費用・レビュー・停止条件が必要な場合に使う。公式Superpowers pluginを基本工程として利用し、通常の小変更や公式skillだけで十分な作業には使わない。
license: MIT
metadata:
  version: "1.1.0"
  official_plugin: "superpowers"
  upstream_repo: "obra/superpowers"
  upstream_commit: "d884ae04edebef577e82ff7c4e143debd0bbec99"
  profile: "official-first-user-policy"
---

# Engineering Review Stack

## 役割

公式Superpowers pluginとCodex標準機能を土台にし、ユーザー固有の品質ゲートを合成する薄いglobal profileである。

```text
目的と証拠境界
→ 公式Superpowersによる設計・計画・TDD
→ Codex標準 /review と独立レビュー
→ 必要な場合だけ cost-aware subagents / Agent Arena
→ verification-loop と claim calibration
```

公式Superpowersをコピーして置き換えるものではない。同名skillを作らず、公式pluginの更新を優先する。

## 起動ゲート

次のいずれかを満たす場合に使う。

- ユーザーが`$engineering-review-stack`を明示した。
- 複数コンポーネントにまたがり、仕様、設計、実装、テスト、レビューを分離する必要がある。
- migration、公開API、security、data loss、研究結論など、失敗時の手戻りまたは影響が大きい。
- 公式Superpowersだけでは、ユーザー固有のevidence、privacy、cost、claim、commit境界を満たせない。

次では起動しない。

- 一行修正、既知の可逆変更、単純な説明。
- 純粋な調査でコード変更がない。
- `/review`または一つの公式skillだけで完了する。
- ユーザーが最短経路を明示している。

## 公式機能の優先

1. `/plugins`で公式`superpowers` pluginが利用可能か確認する。
2. 利用可能なら、タスクに必要な公式skillだけを使う。代表例:
   - `brainstorming`
   - `writing-plans`
   - `using-git-worktrees`
   - `test-driven-development`
   - `requesting-code-review`
   - `receiving-code-review`
   - `verification-before-completion`
   - `finishing-a-development-branch`
3. 公式pluginが未導入または利用不能なら、`references/workflow.md`と`references/review-gates.md`をfallbackとして使い、その劣化を報告する。
4. 公式skillの内容を会話内で再実装せず、このprofileは追加のユーザー契約だけを担当する。

## ユーザー固有の追加契約

### 1. 目的と完了条件

曖昧な依頼では`$define-goal`を使い、objective、non-goals、acceptance criteria、allowed side effects、forbidden actions、verification、rollbackを固定する。

### 2. Evidence gate

原因、履歴、完全性、最新版、欠落、正しさを判断する作業では、実装前に`$evidence-gated-investigation`を使う。推測を仕様またはroot causeとして固定しない。

### 3. Delegation gate

subagentは既定値ではない。独立した非自明な作業が二つ以上あり、所有権と検証経路を分けられる場合だけ`$cost-aware-subagents`を使う。

- 同一Codex内で十分ならnative subagentsを使う。
- cross-provider、durable background、resumeが必要な場合だけ`$orchestrator`へ進む。
- 同じ論理的write setへ複数writerを置かない。
- 統合と最終検証は親が行う。

### 4. Agent Arena gate

`$agent-arena`は次の場合だけ使う。

- 不可逆または高blast-radiusの設計判断。
- 複数の妥当案またはroot cause仮説が競合する。
- 一次資料、コード、テスト、ログで争点を反証できる。
- security、data loss、migration、公開API、研究主張で単一モデルの過信が危険である。

日常的な小変更、通常のdiffレビュー、決定的テストだけで解ける問題に討論を追加しない。

### 5. Review gate

通常の差分はCodex標準`/review`を最初に使う。重大な実装では次を分離する。

1. 仕様適合レビュー。
2. コード品質レビュー。
3. 親による最終検証。

作成者の自己レビューだけで独立レビューを代替しない。指摘は`accepted`、`rejected`、`uncertain`、`deferred`へ証拠付きで分類する。

### 6. Completion gate

完了直前に`$verification-loop`を使い、変更後の状態で対象テスト、relevant suite、lint、format、type check、build、最終diff、未追跡ファイル、migration、docs、rollout、rollbackを確認する。

重大な結論は`$claim-calibration`で、確認済み、推定、未確認を分離する。未実行の検証を成功扱いしない。

## 標準フロー

```text
1. closest AGENTS.md、ユーザー指示、git statusを確認
2. objective / non-goals / acceptance / safety / rollbackを固定
3. 必要ならevidence-gated investigation
4. 公式Superpowersで設計と計画
5. topic branchまたはworktreeで隔離
6. RED → GREEN → REFACTOR
7. 仕様適合レビュー
8. コード品質レビュー
9. 重要指摘を修正して同じゲートを再実行
10. verification-loop
11. claim calibration
12. commit、PR、merge、push、deployはユーザー指示とrepo規則に従う
```

詳細なfallbackと判定形式は、必要な場合だけ参照ファイルを読む。

## 完了報告

最低限、次を報告する。

- 利用した公式skillと、このprofileが追加したユーザー固有規則。
- 採用設計、重要前提、棄却案。
- 変更ファイルまたはcommit。
- 実行した検証と結果。
- 仕様レビュー、品質レビュー、受理・却下した指摘。
- subagent、Orchestrator、Agent Arenaを使った場合の理由、構成、劣化条件。
- 残存リスクと未確認事項。

## 参照

- `references/workflow.md` — 公式plugin利用不能時を含む詳細fallback。
- `references/review-gates.md` — ユーザー固有の仕様・品質・完了判定。
- `SOURCE.md` — 公式pluginとの境界と更新手順。
