# Global AGENTS: 共通統治憲法

全プロジェクトにおけるエージェントの基本動作ルールを定義する。

## 1. 基本指示
- **言語設定:** ユーザーへの回答は常に**日本語**で行うこと。
- **専門スキルの活用:** 必要に応じて ~/.agents/skills/ に配置された共通スキル（例: self-scoring）を優先的に活用すること。
- **コミットメッセージ:** コミットメッセージの提案は、プレフィックス（feat, fix, docs等）を英語、メッセージ本体を日本語で行うこと。

## 2. グローバル skill の Git 管理

- `~/.codex/skills/` または `~/.agents/skills/` の skill を作成・変更した場合、Git 管理外の変更として放置しないこと。
- 汎用的な global skill は、Git 管理されている `~/.codex/skills/<skill-name>/` を正本とすること。
- 特定プロジェクトに依存する skill は、対象リポジトリの `.agents/skills/<skill-name>/` を正本とすること。
- `~/.agents/skills/<skill-name>/` は実行環境向けのインストールコピーとして扱い、正本とバイト単位で同期すること。
- skill の構造、YAML、参照先を検証した後、正本側の Git リポジトリで対象 skill の変更だけを Conventional Commits 形式でコミットすること。
- ユーザーがコミットまたは push を不要と明示した場合を除き、skill の作成・変更、検証、コミット、push を同じ作業単位で完了すること。
