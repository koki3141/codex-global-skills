---
name: orchestrator
description: このskillは、ユーザーが明示的にOrchestratorを指定した場合、またはCodex標準subagentだけでは満たせないcross-provider、background、durable、resume可能な複数エージェント実行が必要な場合に使う。通常のコーディング、同一Codex内の並列調査、通常のコードレビューには使わない。
license: BUSL-1.1
metadata:
  version: "0.1.0-hardened.1"
  upstream_repo: "backnotprop/orchestrator"
  upstream_commit: "d841c7342061f81221d709bed041da79644c5067"
  cli_package: "@backnotprop/orchestrator-cli@0.1.0"
  profile: "manual-read-only-pilot"
---

# Orchestrator for Codex

## 目的

Orchestrator CLIを、複数providerのエージェントをバックグラウンドで起動・監視・停止・再開する**実行制御層**として使う。

判断、分解、品質基準、証拠評価、最終統合は親Codexが担当する。Orchestratorのタスク成功や複数モデルの合意を、正しさの証拠として扱わない。

## 起動ゲート

次の順で最小の手段を選ぶ。

1. 単一Codexで十分なら、そのまま実行する。
2. 同一harness内の独立したread-heavy作業なら、Codex標準subagentを使う。
3. 通常の差分レビューなら、Codex標準の`/review`を使う。
4. 異種モデルによる反証が必要なら、`$agent-arena`でプロトコルを定義する。
5. cross-provider、長時間background、durable task ID、resume、interrupt、永続ログのいずれかが必要な場合だけ、このskillでOrchestratorを使う。

次では起動しない。

- 小さく可逆な修正。
- 単一provider内で完了する通常の探索やレビュー。
- 並列化しても共有write setを分離できない作業。
- 明示的な検証経路がない作業。
- private codeを外部providerへ渡す許可がない作業。

## 事前確認

1. 同じディレクトリの`PREFERENCES.md`を読む。
2. `command -v orchestrator && orchestrator --version`でCLIを確認する。
3. CLIがない場合は**自動インストールしない**。必要条件と固定コマンドを提示して停止する。

```bash
npm install -g @backnotprop/orchestrator-cli@0.1.0
```

4. Node.js 24以上を必要条件として報告する。現在のruntimeやNix環境を勝手に変更しない。
5. 次を実行し、実際に利用可能なruntimeだけを使う。

```bash
orchestrator help --json --compact
orchestrator doctor --json --compact
orchestrator models --json --compact
orchestrator limits --json --compact
```

6. workspace内の`orchestrator.config.json`または`.orchestrator/config.json`を、実行コードと同じ信頼レベルで事前レビューする。未確認のrepo-local custom runtimeを起動しない。
7. `references/safety-profile.md`のprivacy、環境変数、task store、writer隔離を確認する。

## 既定の安全プロファイル

初期pilotでは次を固定する。

- 許可runtimeは`codex`と`claude-code`だけ。
- `shell`、`copilot`、`grok`、`pi`、repo-local/custom runtimeは、ユーザーが今回明示的に許可しない限り使わない。
- 子タスクは原則read-only。実装、deploy、削除、認証変更、外部書き込みを委譲しない。
- 同時実行数は最大3であり、埋めるべき目標ではない。
- private repositoryのファイルを別providerへ渡す前に、対象、目的、provider、保存され得るログを提示して明示承認を得る。
- task packetは必要最小限にし、会話履歴、秘密情報、無関係なディレクトリを渡さない。
- task storeのraw logを親コンテキストへ丸ごと読み込まず、構造化した短い結果だけを読む。
- `failed`、`cancelled`、`timed_out`、`lost`を参加者の回答や合意として扱わない。

## 標準フロー

### 1. 委譲契約を固定する

各タスクに次を与える。

```text
task_id:
objective:
non_goals:
runtime:
model_requirement:
read_or_write: read-only
allowed_paths:
forbidden_paths:
expected_result:
verification:
timeout:
privacy_boundary:
```

`$cost-aware-subagents`を使う場合、委譲価値、並列数、モデルtier、停止条件を先に決める。

### 2. 利用可能runtimeとmodelを解決する

モデル名を記憶から推測しない。厳密なモデル指定が必要な場合だけ、次で返されたIDを使う。

```bash
orchestrator models <runtime> --json --compact
```

指定モデルが利用不能なら、ユーザー指示または`PREFERENCES.md`にfallbackがある場合だけ切り替える。

### 3. 独立タスクを起動する

一件の場合:

```bash
orchestrator launch codex \
  --name "<short task name>" \
  --json --compact --brief \
  "<bounded read-only task>"
```

複数の独立タスクはmanifestでまとめる。依存関係のある処理を同時起動しない。

### 4. pollingせず待つ

次工程が結果を必要とする場合は、短い間隔のpollingを行わず`read --wait`を使う。

```bash
orchestrator read <task-id> --wait --json --compact
```

必要に応じて`ps`、`watch`、`events`を使い、raw logは診断時だけ読む。

### 5. 結果を検証する

- statusが`succeeded`か確認する。
- `outputTruncated`、`stdoutTruncated`、`stderrTruncated`を確認する。
- 子の主張をコード、テスト、一次資料、ログで親が検証する。
- 相互反証が目的なら、`$agent-arena`の独立回答、claim抽出、evidence gate、cross-critique、synthesisに従う。
- 多数決で結論を選ばない。

### 6. 不要な作業を止める

重複、stale、前提が崩れた、または受理済み結果で不要になったタスクは、正確なtask IDを使って停止する。

```bash
orchestrator interrupt <task-id> --json --compact --reason "no longer needed"
```

workspace全体または全machineのcleanupは、ユーザーが明示的に要求した場合だけ行う。

## 書き込みタスク

現行pilotでは並列writerを既定で禁止する。書き込み委譲が必要な場合は、次をすべて満たすまでOrchestratorを使わない。

- ユーザーが書き込み委譲を明示承認した。
- 論理的write setが完全に分離している。
- 各writerに専用branchまたはworktreeがある。
- generated file、lockfile、migration、共有設定のownerが一つである。
- merge、競合解消、最終diff、統合テストを親が担当する。

worktreeがあるだけでは、同じ論理的write setへの並列書き込みを安全とみなさない。

## 完了報告

最低限、次を報告する。

- Orchestratorが必要だった理由と、Codex標準subagentでは不足した点。
- runtime、実モデル、task ID、status。
- 読み取り範囲とprivacy boundary。
- 結果の要約と、親が実行した検証。
- 失敗、timeout、truncation、停止したタスク。
- 未確認事項と残存リスク。
- raw transcriptまたはtask storeの場所。ただし秘密情報を本文へ複製しない。

## 参照

必要な場合だけ読む。

- `PREFERENCES.md` — user-level routingとfallback。
- `references/safety-profile.md` — runtime、secret、task store、writerの安全境界。
- `SOURCE.md` — upstream pin、ローカル差分、更新手順。
