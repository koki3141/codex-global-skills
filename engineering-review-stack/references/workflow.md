# Engineering review workflow fallback

この参照は、公式Superpowers pluginを使った工程にユーザー固有の境界を追加するための補助資料である。公式pluginが利用不能な場合は、同じ品質floorを保つfallbackとして使う。

## 0. Triage

次の三段階から最小のものを選ぶ。

| レベル | 条件 | 実行 |
| --- | --- | --- |
| light | 小さく可逆、局所的、既知の検証がある | 現状確認、変更、対象テスト、diff確認 |
| standard | 複数ファイル、仕様判断、通常の機能追加 | 設計、計画、branch/worktree、TDD、二段階レビュー |
| critical | 不可逆、高blast-radius、競合する設計・原因仮説 | standardに加えてAgent Arena、独立検証、rollout/rollback |

工程数を増やすこと自体を品質とみなさない。決定的検証で解ける問題は討論させない。

## 1. Context packet

実装開始前に、次を一か所へ固定する。

```text
objective:
non_goals:
acceptance_criteria:
constraints:
allowed_side_effects:
forbidden_actions:
baseline:
verification:
rollback:
```

既存のissue、spec、ADR、Notion、Obsidianノートが正本なら、そのリンクまたはファイルを参照し、会話内で別仕様を作らない。

## 2. Baseline

最低限確認する。

```bash
git status --short --branch
git log -1 --oneline
```

加えて、プロジェクトで定義されたsetup、test、lint、type check、buildのうち、変更前ベースラインとして必要なものを実行する。既存失敗は新規失敗と分離して記録する。

## 3. Design

設計メモは次を含む。

- 現状の制約と変更対象。
- 候補案を最低2つ。ただし明白な場合は無理に水増ししない。
- 採用案と棄却理由。
- API、データ、状態、依存関係への影響。
- 互換性、移行、観測性、ロールバック。
- 何を観測すれば設計が誤りと分かるか。

完全に仕様化済みで局所的な実装なら、長い設計会議をせず、設計前提を短く記録して進む。

## 4. Plan

各タスクは、独立してレビューできるサイズにする。

```text
task_id:
goal:
files:
changes:
tests_first:
verification:
dependencies:
definition_of_done:
```

悪いタスクは「認証を実装する」のように大きく、完了条件がない。良いタスクは「失効済みrefresh tokenを拒否するテストを追加し、検証関数を最小変更し、対象テストと既存auth suiteを通す」のように観測可能である。

## 5. Isolation

- 原則としてtopic branchまたはworktreeを使う。
- main/masterへの直接変更は、ユーザーまたはrepo規則が明示した場合だけ。
- worktreeを使っても、同じ論理的write setの並列書き込みは安全にならない。
- 既存dirty treeを勝手にclean、reset、stashしない。
- generated file、lockfile、migrationなど共有資源のownerを一つにする。

## 6. TDD loop

各振る舞いについて次を繰り返す。

1. 受入条件をテストへ落とす。
2. テストが期待した理由で失敗することを確認する。
3. 最小実装を追加する。
4. 対象テストを通す。
5. 必要な周辺テストを通す。
6. 重複と複雑性を減らす。
7. テストを再実行する。
8. 小さなdiffとしてレビューする。

テストを先に書けない場合は、次のいずれかを明示する。

- 文書のみの変更。
- 既存の決定的検証で十分。
- 外部環境が必要でローカル再現不能。
- legacy制約でcharacterization testを先に置く。
- テスト追加が変更より危険で、人間承認を得た。

「時間がない」は単独では省略理由にならない。

## 7. Per-task completion

タスク完了時に、次へ進む前に確認する。

- 仕様適合レビューに未解決事項がない。
- 品質レビューのCritical/Importantが解消済み。
- 対象テストが直近の実装後に成功している。
- 不要なファイルやdebug出力がない。
- plan外の追加実装は削除または明示承認済み。
- diffが次のタスクと混ざっていない。

## 8. Final integration

全タスク後に次を行う。

- 全体の仕様適合レビュー。
- relevant test suite、lint、type check、build。
- migration、configuration、docs、observability、rollbackの確認。
- `git diff`と`git status`の最終確認。
- 変更理由を説明できるfocused commit。
- PR、merge、keep、discardのどれに進むかをユーザー指示に従って決める。

## 9. Stop conditions

次の場合は工程を増やさず停止またはエスカレートする。

- 完了条件と品質floorを満たした。
- 必要な権限、入力、環境がない。
- 同じ失敗を原因変更なしで再試行しようとしている。
- 追加レビューが新しい証拠を生まない。
- 残作業が逐次的でsubagent overheadを下回る。
- 設計の好みや不可逆判断が人間決定を必要とする。
