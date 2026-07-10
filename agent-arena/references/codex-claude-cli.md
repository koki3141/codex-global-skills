# Codex to Claude Code CLI runbook

このreferenceは、CodexがローカルのClaude Code CLIを異種参加者として使う場合の手順である。実行前に現在のCLI helpを確認し、flagやmodel名を推測しない。

## 1. Preflight

```bash
command -v claude
claude --version
claude --help
```

確認する。

- CLIがinstalled、authenticated、non-interactiveで呼べる。
- sandboxから実行可能。
- 対象データを外部providerへ送ってよい。
- approved repo scopeと除外対象。
- timeout、turn、tool budget。
- output先がGit追跡外である。

秘密、credentials、customer data、private logs、dataset、不要な生成物を無断で送らない。

## 2. Mode classification

### Bounded verification

対象diff、named files、atomic claimsなど証拠集合が閉じている。

- 生のfile path、line、diff、test outputをpacketへ含める。
- Codexの結論や疑いを独立回答前に含めない。
- 原則toolsなし、または必要なreadだけ。
- 小さいturn budgetでよい。

概念例。実際のflagはhelpで確認する。

```bash
packet=/tmp/arena-r1.md
output=/tmp/arena-r1.json

claude -p "$(cat "$packet")" \
  --allowedTools '' \
  --max-turns 2 \
  --output-format json > "$output"
```

### Open design / architecture review

どのfileや制約が重要かを参加者自身が探索する必要がある。

- `Read,Glob,Grep`など広いread-only accessを許可する。
- 必要ならread-onlyなtest、lint、dependency inspectionだけBashを許可する。
- 小さいturn capで探索を飢餓状態にしない。
- orchestratorが選んだexcerptだけに限定すると独立性を損なう。

概念例:

```bash
claude -p "$(cat "$packet")" \
  --allowedTools 'Read,Glob,Grep' \
  --max-turns 12 \
  --output-format stream-json > "$output"
```

大きいrepo、曖昧な設計ではさらに余裕が必要になる。turn数を固定規則にせず、実測で調整する。

## 3. Read versus analyze

bounded taskでは、repo探索と分析を分けると効率がよい。ただし、Codexが選んだ資料だけを渡す場合は次を守る。

- raw excerptを渡し、Codexの結論を混ぜない。
- file pathとlineを付ける。
- 何を省略したかを書く。
- 追加資料を要求できるようにする。
- 証拠集合が閉じていないなら、hard scopeを狭めない。

## 4. Output and context budget

外部callのpacketとraw outputを親会話へ直接貼り続けない。

- packetをfileへ保存し、stdinまたはfile経由で渡す。
- raw JSON/streamをround別fileへ保存する。
- 親へ戻すのは構造化digestだけにする。
- digestにはrecommendation、disagreements、uncertainties、what-would-change-mind、requested-evidence、raw pathを残す。
- 各round後にcheckpointを保存し、compaction後に再開できるようにする。
- raw outputを丸ごと再読して同じArenaを再起動しない。

checkpoint例:

```yaml
round:
participant:
session_id:
raw_output:
recommendation:
key_disagreements:
uncertainties:
requested_evidence:
open_items:
```

checkpointやraw outputをrepoへcommitしない。必要な場合だけ、redactedな最終auditを明示的に保存する。

## 5. Timeouts

non-trivial reviewは数分かかることがある。短い無出力をhangとみなさない。

- timeoutはturn budgetとrepo規模に合わせる。
- non-trivial callではstream outputを使う。
- `-p`欠落によるinteractive待ちを確認する。
- tool permission prompt待ちを確認する。
- duration、turn数、終了理由を記録する。

## 6. Failure classification

失敗を次へ分類する。

- `auth`。
- `model_unavailable`。
- `timeout`。
- `max_turns`。
- `tool_permission`。
- `interactive_stdin_wait`。
- `malformed_output`。
- `refusal`。
- `sandbox_or_network`。

機械的失敗はArenaの意見ではない。

## 7. Retry policy

自動再試行は1回だけで、原因を一つ変える。

安全な変更例:

- 同じsessionをresumeする。
- timeoutまたはturn budgetを増やす。
- task packetの完了条件を明確化する。
- open designをbounded reviewとして誤分類していた場合、read-only探索を戻す。
- 利用不能なmodel overrideを外し、defaultへ戻す。

ユーザー確認なしに行わない変更:

- read accessを外してorchestrator選定excerptだけにする。
- private scopeを広げる。
- network、Bash、write権限を増やす。
- 不完全な参加者を合意として受け入れる。
- external providerへ追加データを送る。

## 8. Degraded mode

Claude CLIが使えない場合:

1. unavailable理由を記録する。
2. Codex subagentを別methodで独立実行する。
3. first-principles、outside-view、disconfirming-evidence、reproductionなど方法を分ける。
4. 同系列であることを最終出力に書く。
5. convergenceを弱い証拠として扱う。
