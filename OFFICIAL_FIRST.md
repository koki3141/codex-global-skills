# Official-first Codex skill policy

## 目的

グローバルCodex skillは、公式機能を再実装する保管庫ではなく、**公式機能では満たせないユーザー固有の契約、統合、専門知識、安全境界だけを保持する**。

Skill数は発見性と初期コンテキストを消費する。似たskillを増やすことを能力向上とみなさない。

## 優先順位

同じ目的を達成できる場合、次の順で選ぶ。

1. Codex組み込み機能・system skill。
2. OpenAI公式marketplaceのpluginと、そのpluginに含まれるskill。
3. 公式skillを呼び出す薄いユーザープロファイル。
4. 公式で達成できない独自global skill。
5. 特定repository専用skillは、そのrepositoryの`.agents/skills/`。

現在の公式配布元は`openai/plugins`とCodex公式ドキュメントを正本とする。廃止済みの`openai/skills`を、新規vendor元として使わない。

## ユーザーskillを保持できる条件

次のいずれかを満たし、公式機能との差分を説明できる場合だけ保持する。

- 複数の公式機能やpluginを、ユーザー固有の順序・停止条件・安全規則で合成する。
- 公式機能にないprivacy、cost、evidence、approval、rollback、commit境界を強制する。
- ユーザー固有の研究分野、論文、実験、Obsidian、Zotero、組織規則を持つ。
- 決定的なscripts、schemas、templates、検証器など、単なるprompt以上の資産を持つ。
- cross-provider、外部CLI、固有データ形式など、Codex組み込みだけでは実現できない能力を提供する。
- 公式skillの挙動を置き換えるのではなく、明示的なmanual profileまたはfallbackとして価値がある。

「説明が少し違う」「自分向けに言い換えた」「手順を一つの長いSKILL.mdへコピーした」だけでは保持理由にしない。

## 禁止事項

- 公式pluginと同じskill名を、global repo内で再定義しない。
- 公式pluginの内容を、更新追跡なしにcopyして独自skillとして維持しない。
- project名、絶対path、private repository構造に依存するskillをglobalに置かない。
- plugin cache、`.system/`、installed runtime copyを、このrepoの正本として追跡しない。
- 公式機能を確認せずに新しいglobal skillを作らない。
- 公式pluginが未導入の状態で、fallbackを先に削除して能力gapを作らない。

## 新規skillの事前確認

新しいglobal skillを作る前に、次を短く記録する。

```text
job:
official_builtin_checked:
official_plugins_checked:
closest_official_capability:
missing_user_requirements:
why_wrapper_is_insufficient:
global_vs_project_scope:
name_collision_check:
maintenance_owner:
review_date:
```

公式で満たせるなら、`/plugins`から公式pluginを導入し、このrepoに同等skillを作らない。

## 公式pluginを拡張する場合

独自profileは公式skillを置き換えず、別名にする。

例:

```text
official: superpowers plugin
user profile: engineering-review-stack
```

profileには次だけを置く。

- ユーザー固有の起動ゲート。
- 公式skillの選択・組み合わせ。
- ユーザー固有の安全・検証・停止条件。
- 既存global skillとの接続。
- 公式で不足するfallback。

公式内容の全面コピーは避ける。

## project-local判定

次のいずれかを含むskillは、原則として対象repoの`.agents/skills/`へ置く。

- 特定repository名または絶対path。
- repository固有のdirectory layout、commands、equation IDs、protocol、claim boundary。
- 他repoでは意味を持たないcommit順序、artifact policy、submodule構造。

複数repoで本当に再利用する部分だけをglobalへ抽出する。

## lifecycle

各skillを次のいずれかへ分類する。

```text
KEEP_CUSTOM
KEEP_OFFICIAL_WRAPPER
MIGRATE_TO_OFFICIAL
MOVE_PROJECT_LOCAL
CONSOLIDATE
RETIRE
REVIEW
```

`MIGRATE_TO_OFFICIAL`は次の順で行う。

1. 公式pluginをローカルCodexで導入する。
2. 代表タスクで公式skillを検証する。
3. user-specific差分がなければcustom entrypointを削除する。
4. 差分が必要なら別名の薄いprofileへ移す。
5. index、Obsidianノート、auditを更新する。

## 定期監査

少なくとも月次、およびCodex/plugin更新後に確認する。

- 公式pluginに新しい同等機能が追加されていないか。
- 同名skill、近似skill、死んだ参照がないか。
- globalにproject固有skillが混入していないか。
- triggerが広すぎて通常作業を奪っていないか。
- 使われていないskillが初期skill一覧を圧迫していないか。
- upstream pin、license、scripts、referencesが有効か。

現在の判断は`official-first-audit-2026-07-10.md`を参照する。
