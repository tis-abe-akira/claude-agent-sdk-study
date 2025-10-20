# Deep Research Agent 🔬

複数のメディアソース（YouTube、Reddit、ArXiv、Medium）から情報を収集・統合する、Claude Agent SDK ベースのリサーチエージェントです。

## クイックスタート

```bash
# 1. プロジェクトルートからdeep-researchディレクトリに移動
cd /Users/akiraabe/practice/claude-agent-sdk-study/deep-research

# 2. 依存関係をインストール
uv sync

# 3. .envファイルを作成してAPIキーを設定
cp .env.example .env
# エディタで .env を開いて ANTHROPIC_API_KEY=your_api_key_here を設定

# 4. 実行
uv run deep-research "あなたの調べたいトピック"
```

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

**重要**: このプロジェクトのルートディレクトリは `/Users/akiraabe/practice/claude-agent-sdk-study` です。

以下のコマンドは、**プロジェクトルートから**実行してください。

1. **deep-researchディレクトリに移動**

```bash
# プロジェクトルートにいることを確認
pwd
# 出力: /Users/akiraabe/practice/claude-agent-sdk-study

# deep-researchディレクトリに移動
cd deep-research
```

2. **依存関係のインストール**

```bash
uv sync
```

3. **環境変数の設定**

`.env.example` を `.env` にコピーして、APIキーを設定します：

```bash
# deep-researchディレクトリ内で実行
cp .env.example .env
```

`.env` ファイルを編集：

```env
ANTHROPIC_API_KEY=your_actual_api_key_here
```

APIキーは [Anthropic Console](https://console.anthropic.com/) で取得できます。

## 使い方

**重要**: 以下のコマンドはすべて `deep-research` ディレクトリ内で実行してください。

### ディレクトリ構造の確認

```bash
# プロジェクトルートから
cd deep-research

# 現在のディレクトリを確認
pwd
# 出力: /Users/akiraabe/practice/claude-agent-sdk-study/deep-research
```

### 対話型モード

```bash
# deep-researchディレクトリ内で実行
uv run deep-research
```

または

```bash
# deep-researchディレクトリ内で実行
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
# deep-researchディレクトリ内で実行
uv run deep-research "量子コンピューティングの応用例"
```

### Pythonコードから使用

```python
import asyncio
from deep_research.main import research_query_sources, analyze_with_claude

async def main():
    # データ収集
    results = await research_query_sources("自然言語処理")
    print(results)

    # Claude による分析
    await analyze_with_claude("自然言語処理", results)

asyncio.run(main())
```

**実行方法**:

```bash
# deep-researchディレクトリ内で実行
uv run python your_script.py
```

## プロジェクト構造

```
/Users/akiraabe/practice/claude-agent-sdk-study/  # プロジェクトルート
└── deep-research/                                # ← このディレクトリで作業
    ├── src/
    │   └── deep_research/
    │       ├── __init__.py       # パッケージ初期化
    │       ├── main.py           # メインエントリーポイント
    │       └── tools.py          # リサーチツール実装
    ├── examples/
    │   ├── simple_search.py      # シンプルな検索例
    │   └── agent_example.py      # Claude Agent統合例
    ├── pyproject.toml            # プロジェクト設定
    ├── .env.example              # 環境変数テンプレート
    ├── .env                      # 環境変数（作成する必要あり）
    ├── .gitignore                # Git除外設定
    └── README.md                 # このファイル
```

**重要**: すべてのコマンドは `deep-research` ディレクトリ内で実行してください。

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

### コマンドが見つからない / ModuleNotFoundError

**症状**: `uv run deep-research` を実行すると「コマンドが見つかりません」または「ModuleNotFoundError」が出る

**原因**: 間違ったディレクトリで実行している可能性があります

**解決策**:

```bash
# 現在のディレクトリを確認
pwd

# 正しいディレクトリに移動
cd /Users/akiraabe/practice/claude-agent-sdk-study/deep-research

# 再度確認
pwd
# 出力: /Users/akiraabe/practice/claude-agent-sdk-study/deep-research

# 依存関係が正しくインストールされているか確認
uv sync

# 実行
uv run deep-research "test"
```

### `ANTHROPIC_API_KEY not found`

**症状**: API分析が実行されず、「ANTHROPIC_API_KEY not found」エラーが表示される

**解決策**: `.env` ファイルが正しく設定されているか確認：

```bash
# deep-researchディレクトリ内で実行
# .env ファイルの存在確認
ls -la .env

# 内容確認（APIキーの最初の数文字だけ確認）
head -c 30 .env

# .envファイルがない場合は作成
cp .env.example .env
# エディタで開いて ANTHROPIC_API_KEY=your_actual_api_key_here を設定
```

### AI分析結果が空

**症状**: データは収集されるが、AI分析結果が何も表示されない

**原因**: APIキーが設定されていないか、無効です

**解決策**:

1. `.env` ファイルを確認
2. APIキーが正しいか [Anthropic Console](https://console.anthropic.com/) で確認
3. APIキーに課金設定がされているか確認

### インポートエラー

依存関係が正しくインストールされているか確認：

```bash
# deep-researchディレクトリ内で実行
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
