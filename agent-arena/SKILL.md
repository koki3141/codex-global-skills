---
name: agent-arena
description: このskillは、ユーザーが「Agent Arenaを使って」「CodexとClaudeで独立レビューして」「この設計を異種モデルでred-teamして」と依頼した場合、または重大で対立的・反証可能な設計判断、root cause、実装計画、研究主張、PRを証拠付きで相互検証する必要がある場合に使う。単純な調査、通常の小変更、決定的テストだけで解ける問題には使わない。
license: MIT
metadata:
  version: "0.3.0-local"
  upstream_repo: "zhjai/agent-arena"
  upstream_commit: "a9b4f262bddb4efd9b25c2b14c82ba3bb5570751"
  related_skills: "superpowers,cost-aware-subagents,evidence-gated-investigation,claim-calibration"
---

# Agent Arena

## 目的

複数のエージェントを単に多数決させるのではなく、独立回答、主張抽出、証拠確認、相互反証、改訂、裁定を通して、過信と共通幻覚を減らす。

中核原則は次である。

> Independent first. Evidence before consensus. Deterministic checks before model judgment. Dissent preserved.

## 起動ゲート

次の両方を満たす場合に使う。

1. 結論を誤った場合の影響が大きい。
2. 複数の妥当な見方がある、または主張を一次資料・コード・テスト・ログ・計算で反証できる。

適例:

- アーキテクチャ、公開API、schema、migration、rollout。
- 競合する障害原因仮説。
- 重要な実装計画またはPR。
- セキュリティ、データ損失、研究結論、評価設計。
- 単一モデルの確信に依存したくない意思決定。

不適例:

- 単純な事実確認、翻訳、整形。
- 一行修正や低リスクな可逆変更。
- 既知のテストまたは一次資料だけで決着する問題。
- アイデア数を増やすだけの一般的brainstorming。

## モード

最小十分なモードを選ぶ。

| モード | 用途 |
| --- | --- |
| `quick_panel` | 2者の短い独立回答と1回の反証 |
| `design_debate` | 設計案、実装計画、durable contract |
| `evidence_arena` | 現在の事実、研究主張、性能・仕様の検証 |
| `code_review_arena` | diff、PR、重要実装の独立レビュー |
| `bug_root_cause_arena` | 競合する原因仮説と再現テスト |
| `full_arena` | 高リスク案件の全プロトコル |
| `solo_red_team` | 異種参加者が使えない場合の劣化モード |

既定は2参加者、独立回答と反証・改訂の2段階。`full_arena`だけ必要に応じて3段階へ増やす。

## 参加者

異質性は次の順に優先する。

1. 異なるモデル系列と異なる実行環境。
2. 異なるモデル系列。
3. 同系列でも異なる証拠経路・方法。
4. 同一モデルの役割分け。これは独立性が最も弱い。

Codex内では、許可され利用可能ならClaude Code CLIを異種参加者として確認する。外部CLIがない場合、同一系列subagentへ劣化したことを明示し、合意の証拠力を下げる。ロール名だけで異質性を主張しない。

## プライバシーと権限

外部モデル、CLI、APIへ送る前に次を確認する。

- private code、顧客データ、秘密、token、credentials、private logsを送ってよいか。
- 必要最小限のscopeは何か。
- 読み取り、テスト実行、network accessのどこまで許可されるか。
- push、deploy、削除、課金、公開など不可逆操作を禁止できているか。

機密性により外部委譲できない場合は `solo_red_team` またはローカル決定的検証へ劣化し、その影響を報告する。

## 標準プロトコル

### 0. フレームと予算

質問、制約、成功条件、既知事実、未確認事項、許可されたtools、副作用、出力形式を自己完結したtask packetにする。`$cost-aware-subagents` の予算と停止条件を適用する。

### 1. 独立回答

各参加者は、他者の回答を見ずに次を返す。

- recommendation。
- reasoning summary。
- assumptions。
- evidence used。
- uncertainties。
- what would change my mind。
- concrete falsification conditions。

### 2. Validation gate

status文字列、tool error、timeout、空回答を参加者の意見として扱わない。機械的失敗は1回だけ原因を変えて再試行し、失敗が続けば参加者を落として劣化モードを報告する。

### 3. 主張と証拠

重要な主張をatomic claimへ分解し、コード、テスト、ログ、一次資料、計算で確認する。モデル間の合意より決定的検証を優先する。詳細は `references/protocol.md` を読む。

### 4. 相互反証

他者の具体的な主張を引用し、反例、再現、欠けた証拠、隠れた前提、実装リスクを攻撃する。称賛、要約、同意の水増しは禁止する。

### 5. 改訂

各参加者は、正当な批判を理由付きで受理し、残る主張を理由付きで防御する。最終見解、残存不確実性、確信度、反証条件を返す。理由のない全面転向はsycophancy flagとする。

### 6. 裁定と統合

可能なら候補の出所を匿名化し、正確性、証拠、実現可能性、リスク、単純性、制約適合で判定する。平均や多数決ではなく、証拠の強さで争点を裁定する。

## 外部CLI

CodexからClaude Codeを呼ぶ具体的なpreflight、bounded/open reviewの区別、timeout、output保存、context budget、失敗分類は `references/codex-claude-cli.md` に従う。CLIのversionとhelpを確認せず、古いflagを推測しない。

## 失敗モード

- `ghost panelist`: errorやstatusを回答扱いする。
- `sycophantic convergence`: 新しい証拠なしに全員が同意する。
- `diversity illusion`: 同一モデルの人格名を独立参加者とみなす。
- `facilitator capture`: 統合役の先入観をパネルの権威として出す。
- `confidence theater`: 数字だけの確信度で反証条件がない。
- `consensus laundering`: 共通幻覚を合意で正当化する。
- `context blow-up`: 生の長大な入出力を親コンテキストへ戻し、再実行ループを起こす。

## 停止条件

次のいずれかで停止する。

- 重要主張が決定的証拠で裁定された。
- 追加ラウンドが新しい証拠または有効な反例を生まない。
- 予算、runtime、tool、privacy境界に達した。
- 残る争点が技術ではなく人間の価値判断である。
- 必要な一次資料または実行環境がなく、これ以上の裁定が不可能である。

## 最終出力

次の順で返す。

1. `合意点` — 合意内容と、その合意がどれだけ強い証拠か。
2. `対立点` — 誰が何を主張し、どの証拠で裁定したか。
3. `結論` — 推奨、確信度、反証条件、次に行う最小検証。
4. `Arena limitations` — 実際の参加者、劣化、失敗、見られなかった証拠。
5. `Audit trail` — 受理・却下した主要批判と理由。

## 他skillとの関係

- `$superpowers`: 重要な設計承認前、または高リスクなmerge前だけArenaを挿入する。
- `$evidence-gated-investigation`: root causeや履歴調査の一次証拠を作る。
- `$cost-aware-subagents`: 参加者数、wave、モデルtier、停止条件を管理する。
- `$claim-calibration`: 最終主張を確認済み、推定、未確認へ分ける。

## 参照

必要な場合だけ読む。

- `references/protocol.md` — claim ledger、各ラウンド、judge rubric、統合形式。
- `references/codex-claude-cli.md` — CodexからClaude Code CLIを安全に呼ぶ手順。
- `SOURCE.md` — 上流との関係、ローカル差分、更新手順。
