# Agent Arena protocol

## Task packet

```yaml
question:
decision_owner:
stakes:
success_criteria:
constraints:
known_facts:
unknowns:
approved_scope:
allowed_tools:
forbidden_actions:
privacy_boundary:
required_output:
budget:
```

既知事実と推測を混ぜない。参加者には結論誘導を含めず、必要な生の証拠または参照先を渡す。

## Round 1: independent positions

各参加者へ同一packetを渡し、他者回答を見せない。返却schema:

```yaml
recommendation:
reasoning:
assumptions:
claims:
evidence:
uncertainties:
falsification_conditions:
requested_checks:
```

### Validation gate

以下は無効回答である。

- 起動通知や進捗だけ。
- stack trace、auth error、timeout。
- requested schemaを満たさない空疎な文。
- 他者回答を見た形跡があるanchored回答。
- 実行したと主張するが証拠がない検証。

機械的失敗を「反対意見なし」または合意として数えない。

## Claim ledger

重要な主張を次の表へ分解する。

| claim_id | source_agent | atomic_claim | claim_type | evidence_needed | status | evidence | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |

`claim_type`:

- factual。
- code behavior。
- performance。
- security。
- causal/root cause。
- user preference。
- risk/forecast。

`status`:

- `verified`。
- `refuted`。
- `partially_supported`。
- `unverified`。
- `not_testable_here`。

同じ主張を複数モデルが繰り返しても証拠件数は増えない。

## Evidence gate

優先順位:

1. 実行可能な決定的テスト、再現、計算。
2. 対象コード、設定、schema、logの直接観察。
3. 公式仕様、一次資料、原論文。
4. 信頼できる二次資料。
5. モデルの専門判断。
6. 多数決。

性能、価格、model availability、規則、APIは現在性を確認する。現時点で確認できない場合は日付と未確認を明示する。

## Round 2: cross-critique

各参加者へ、他者のpositionと関連するclaim ledgerだけを渡す。指示:

- 攻撃する中心主張を特定する。
- 反例または不足証拠を示す。
- 再現可能ならコマンド、入力、期待結果を示す。
- 隠れた前提と代替仮説を挙げる。
- 合意の水増し、称賛、全体要約をしない。
- 本当に残る合意だけを最後に短く示す。

返却schema:

```yaml
attacked_claims:
reproductions:
counterexamples:
missing_evidence:
alternative_hypotheses:
genuine_agreements:
```

## Round 3: revision

各参加者へ自分に向けられた批判と検証結果を渡す。返却schema:

```yaml
accepted_critiques:
rejected_critiques:
revised_recommendation:
surviving_claims:
residual_uncertainty:
confidence:
falsification_condition:
next_minimum_test:
```

全面転向は、どの証拠で変わったかがない限り採用しない。

## Judge rubric

候補を可能なら匿名化し、各項目を0から4で評価する。

| 項目 | 0 | 4 |
| --- | --- | --- |
| correctness | 明確な誤り | 主要主張が検証済み |
| evidence | 根拠なし | 一次証拠・再現可能 |
| feasibility | 実行不能 | 制約内で具体的に実装可能 |
| risk handling | 重大リスク無視 | failure、rollback、monitoringを扱う |
| simplicity | 不要に複雑 | 最小十分 |
| constraint fit | 条件違反 | ユーザー条件に適合 |

点数は裁定補助であり、verifiedな反証を平均点で打ち消してはならない。

## Synthesis

```markdown
## 合意点
- 合意:
- 最強の根拠:
- 収束の証拠力: 強い / 中程度 / 弱い

## 対立点
### D1
- 立場A:
- 立場B:
- 証拠:
- 裁定:
- 未解決なら必要な確認:

## 結論
- 推奨:
- 確信度:
- 反証条件:
- 次の最小検証:

## Arena limitations
- 実参加者:
- model family:
- tools:
- privacy制約:
- mechanical failures:
- degraded mode:

## Audit trail
- 受理した批判:
- 却下した批判:
- 保留した少数意見:
```

## No averaging

「AとBの中間」に自動的に寄せない。次の順で扱う。

- 片側だけが再現可能な証拠を持つなら、その側を採る。
- 両側が異なる目的関数を最適化しているなら、価値判断として分離する。
- 証拠不足なら、結論を薄めるのではなく、必要な観測を指定する。
- 少数意見が高impact・低probabilityのfailureを指摘するなら保持する。
