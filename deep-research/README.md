# Deep Research Agent 🔬

複数のメディアソース（YouTube、Reddit、ArXiv、Medium）から情報を収集・統合する、Claude Agent SDK ベースのリサーチエージェントです。

## 特徴

- 🔍 **マルチソース検索**: YouTube、Reddit、ArXiv、Mediumから情報を収集
- 🤖 **AI駆動分析**: Claude による高度な情報統合と分析
- 📊 **包括的レポート**: 収集した情報を論理的に整理して提示
- ⚡ **非同期処理**: 複数のソースから並列で情報を取得
- 💬 **対話型モード**: インタラクティブなリサーチセッション

## 現在の実装状況

| ソース | 状態 | 説明 |
|--------|------|------|
| Reddit | ✅ 実装済み | Reddit公開APIを使用 |
| ArXiv | ✅ 実装済み | ArXiv公開APIを使用 |
| YouTube | 🚧 要実装 | YouTube Data API v3キーが必要 |
| Medium | 🚧 要実装 | RSSフィードまたはスクレイピング |

## インストール

### 前提条件

- Python 3.11 以上
- [uv](https://github.com/astral-sh/uv) パッケージマネージャー
- Anthropic APIキー

### セットアップ

1. **依存関係のインストール**

```bash
cd deep-research
uv sync
```

2. **環境変数の設定**

`.env.example` を `.env` にコピーして、APIキーを設定します：

```bash
cp .env.example .env
```

`.env` ファイルを編集：

```env
ANTHROPIC_API_KEY=your_actual_api_key_here
```

APIキーは [Anthropic Console](https://console.anthropic.com/) で取得できます。

## 使い方

### 対話型モード

```bash
uv run deep-research
```

または

```bash
uv run python -m deep_research.main
```

対話型セッションが起動し、複数のトピックについてリサーチできます：

```
🔬 Deep Research Agent - マルチソースリサーチアシスタント
============================================================
YouTube、Reddit、ArXiv、Mediumから情報を収集・統合します。
終了するには 'exit' または 'quit' と入力してください。
============================================================

💭 リサーチトピック: 機械学習の最新動向

🔍 調査中: 機械学習の最新動向
------------------------------------------------------------
📊 データ収集中...
🤖 分析中...
------------------------------------------------------------
[AIによる分析結果が表示されます]
```

### シングルクエリモード

コマンドライン引数でクエリを指定すると、1回だけリサーチを実行します：

```bash
uv run deep-research "量子コンピューティングの応用例"
```

### Pythonコードから使用

```python
import asyncio
from deep_research.main import research_query, create_research_agent

async def main():
    # データ収集のみ
    results = await research_query("自然言語処理")
    print(results)

    # エージェントを使った分析
    agent = await create_research_agent()
    response = await agent.query("機械学習について教えて")
    print(response)

asyncio.run(main())
```

## プロジェクト構造

```
deep-research/
├── src/
│   └── deep_research/
│       ├── __init__.py       # パッケージ初期化
│       ├── main.py           # メインエントリーポイント
│       └── tools.py          # リサーチツール実装
├── pyproject.toml            # プロジェクト設定
├── .env.example              # 環境変数テンプレート
├── .gitignore                # Git除外設定
└── README.md                 # このファイル
```

## 各ソースの詳細

### Reddit (実装済み ✅)

Reddit の公開 JSON API を使用して、投稿を検索します。認証不要で使用できます。

```python
results = await tools.search_reddit("machine learning", subreddit="MachineLearning", limit=10)
```

### ArXiv (実装済み ✅)

ArXiv の公開 API を使用して、学術論文を検索します。認証不要で使用できます。

```python
results = await tools.search_arxiv("neural networks", max_results=10)
```

### YouTube (要実装 🚧)

YouTube Data API v3 の実装が必要です。

**セットアップ手順:**
1. [Google Cloud Console](https://console.developers.google.com/) でプロジェクトを作成
2. YouTube Data API v3 を有効化
3. APIキーを取得
4. `.env` に `YOUTUBE_API_KEY` を設定

### Medium (要実装 🚧)

Medium には無料の公開APIがありません。以下の方法が考えられます：

- **RSSフィード**: `https://medium.com/feed/tag/{tag}` を使用
- **Webスクレイピング**: Medium の利用規約を確認してください
- **サードパーティAPI**: 有料サービスを利用

## カスタマイズ

### システムプロンプトの変更

`src/deep_research/main.py` の `create_research_agent()` 関数内の `system_prompt` を編集することで、エージェントの動作をカスタマイズできます。

### 新しいソースの追加

1. `src/deep_research/tools.py` に新しいメソッドを追加
2. `src/deep_research/main.py` の `research_query()` 関数を更新
3. 必要に応じて環境変数を `.env.example` に追加

## トラブルシューティング

### `ANTHROPIC_API_KEY not found`

`.env` ファイルが正しく設定されているか確認してください：

```bash
# .env ファイルの存在確認
ls -la .env

# 内容確認（APIキーは表示されません）
cat .env
```

### インポートエラー

依存関係が正しくインストールされているか確認：

```bash
uv sync
uv pip list | grep claude-agent-sdk
```

### ネットワークエラー

Reddit や ArXiv の API がタイムアウトする場合、リトライロジックを追加するか、タイムアウト値を増やしてください。

## 今後の改善案

- [ ] YouTube Data API の完全実装
- [ ] Medium RSS フィード統合
- [ ] 結果のキャッシング機能
- [ ] エクスポート機能（Markdown、PDF、JSON）
- [ ] Web UI の追加
- [ ] より高度な情報フィルタリング
- [ ] 複数言語サポート
- [ ] 検索結果のランキング機能

## ライセンス

MIT License

## 関連リンク

- [Claude Agent SDK ドキュメント](https://docs.claude.com/en/api/agent-sdk/python)
- [Anthropic API リファレンス](https://docs.anthropic.com/)
- [Reddit API](https://www.reddit.com/dev/api/)
- [ArXiv API](https://arxiv.org/help/api/)
