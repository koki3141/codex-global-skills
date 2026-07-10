# Engineering review gates

## Gate 1: specification compliance

最初のレビュアーは「良いコードか」ではなく「要求どおりか」を判定する。実装者の説明ではなく、spec、受入条件、diff、テストを読む。

返却形式:

```text
verdict: PASS | FAIL | INSUFFICIENT_EVIDENCE
missing_requirements:
extra_scope:
behavioral_mismatches:
evidence:
required_fixes:
```

FAIL条件:

- 要求された振る舞いが欠ける。
- 仕様外の機能、依存、API変更が追加される。
- 受入条件を満たす証拠がない。
- テストが要求を実際には検査していない。
- 移行、互換性、権限、安全制約を破る。

仕様適合がPASSするまで、コード品質の承認だけで先へ進まない。

## Gate 2: code quality

二番目のレビュアーは、仕様適合済みの実装について品質を判定する。

確認対象:

- 正確性と境界条件。
- セキュリティ、認可、入力検証、秘密情報。
- 競合、再試行、冪等性、トランザクション。
- エラー処理、観測性、運用可能性。
- 複雑性、重複、命名、保守性。
- テストの独立性、決定性、失敗時の診断性。
- 性能と資源使用。ただし測定なしに断定しない。
- 後方互換性、公開API、data migration。
- 文書と実装の一致。

返却形式:

```text
verdict: PASS | FAIL | INSUFFICIENT_EVIDENCE
critical:
important:
minor:
evidence:
required_fixes:
```

CriticalとImportantは修正後に同じゲートを再実行する。Minorは追跡または明示的に受容できる。

## Gate 3: final verification

完了主張の直前に、親が実行する。

1. 対象テストを新しい状態で実行する。
2. relevant suiteを実行する。
3. lint、format、type check、buildの該当項目を実行する。
4. 最終diffと未追跡ファイルを確認する。
5. 設定、migration、文書、rollout、rollbackを確認する。
6. 失敗を隠すskip、filter、`|| true`、stale cacheがないか確認する。
7. 実行不能な検証は、未確認として理由と影響を報告する。

## 独立性

- 実装者の自己レビューは必要だが、独立レビューの代替ではない。
- fresh subagentでも、実装者の結論だけを渡すとanchoringする。
- レビュアーには一次入力、spec、diff、テストを渡す。
- 同系列モデルの一致は弱い証拠であり、決定的テストや一次資料を優先する。
- 高リスクでは、作成者と異なるモデル、方法、証拠経路の少なくとも一つを使う。
- 通常レビューはCodex標準`/review`を優先し、このprofileは追加rubricが必要な場合だけ使う。

## 指摘の受理

レビューコメントは権威ではない。各指摘を次で分類する。

- `accepted`: 再現または一次資料で妥当。
- `rejected`: 反証があり、理由を記録。
- `uncertain`: 証拠不足。必要な確認を特定。
- `deferred`: 今回のscope外で、issue等へ移管。

多数決で分類しない。
