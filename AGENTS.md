# Global AGENTS: 共通統治憲法

全プロジェクトにおけるエージェントの基本動作ルールを定義する。

## 1. 基本指示

- **言語設定:** ユーザーへの回答は常に**日本語**で行うこと。
- **専門スキルの活用:** 必要に応じて`~/.agents/skills/`または`~/.codex/skills/`の共通スキルを活用すること。
- **コミットメッセージ:** コミットメッセージは、prefixをEnglish、メッセージ本体を日本語にすること。

## 2. 公式優先

- 新しいglobal skillを作る前に、Codex組み込み機能、system skill、OpenAI公式marketplace pluginを確認すること。
- 公式機能でユーザー要件を満たせる場合、このrepoに同等skillを作成またはvendorしないこと。
- 公式pluginを拡張する必要がある場合、公式skillと異なるnameの薄いprofileにし、ユーザー固有の差分だけを保持すること。
- 公式skillと同名のcustom global skillを維持しないこと。
- custom skillを保持する理由は、user-specificなprivacy、evidence、cost、approval、rollback、deterministic tooling、domain rule、cross-provider capabilityのいずれかとして説明できなければならない。
- Codex native hookで実現できる処理をmanual hook-emulation skillとして再実装しないこと。
- 詳細は`OFFICIAL_FIRST.md`に従うこと。

## 3. グローバルskillのGit管理

- `~/.codex/skills/`または`~/.agents/skills/`のskillを作成・変更した場合、Git管理外の変更として放置しないこと。
- 汎用的なglobal skillは、Git管理されている`~/.codex/skills/<skill-name>/`を正本とすること。
- 特定projectに依存するskillは、対象repositoryの`.agents/skills/<skill-name>/`を正本とすること。
- `~/.agents/skills/<skill-name>/`は実行環境向けのinstalled copyとして扱い、正本とbyte単位で同期すること。
- plugin由来のskillはplugin managerに所有させ、このrepoへcopyしないこと。
- skillのstructure、YAML、local referenceを検証した後、正本側のGit repositoryで対象skillと直接関係するgovernance fileだけをcommitすること。
- ユーザーがcommitまたはpushを不要と明示した場合を除き、skillの作成・変更、検証、commit、pushを同じ作業単位で完了すること。
- skillを追加、削除、renameした場合は、`refresh-skill-index.yml`が生成indexを更新したことを確認すること。workflowを使えない場合だけ`python3 scripts/generate-chatgpt-global-skill-index.py`を手動実行すること。
