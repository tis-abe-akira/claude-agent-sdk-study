"""Main entry point for the Deep Research Agent."""

import asyncio
import os
import json
from typing import Optional
from dotenv import load_dotenv
from claude_agent_sdk import query as claude_query, ClaudeAgentOptions
from .tools import ResearchTools


# Load environment variables from .env file
load_dotenv()


def get_api_key() -> str:
    """
    Get API key from environment.

    Returns:
        API key string

    Raises:
        ValueError: If API key is not found
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY not found in environment. "
            "Please set it in your .env file or environment."
        )
    return api_key


def get_system_prompt() -> str:
    """
    Get the system prompt for the research agent.

    Returns:
        System prompt string
    """
    return """あなたは高度なリサーチエージェントです。ユーザーから与えられたトピックについて、
複数のメディアソース（YouTube、Reddit、ArXiv、Medium）から情報を収集し、
それらを統合して包括的なレポートを作成することが使命です。

以下の手順で調査を進めてください：

1. **情報収集フェーズ**
   - ユーザーのクエリを分析し、適切な検索キーワードを決定
   - 各メディアソースから関連情報を収集：
     * Reddit: コミュニティの議論、実体験、トレンド
     * ArXiv: 学術論文、科学的根拠
     * YouTube: 動画コンテンツ、チュートリアル（実装が必要）
     * Medium: 記事、専門家の意見（実装が必要）

2. **分析フェーズ**
   - 収集した情報の信頼性を評価
   - 共通するテーマやパターンを特定
   - 矛盾する情報があれば明示

3. **統合・レポート作成フェーズ**
   - 情報を論理的に整理
   - 各ソースからの重要な洞察をまとめる
   - 日本語で分かりやすく説明
   - 必要に応じて、さらなる調査が必要な領域を提案

収集されたデータを効果的に活用し、ユーザーに価値ある洞察を提供してください。
"""


async def research_query_sources(user_query: str, sources: Optional[list[str]] = None) -> dict:
    """
    Execute a research query across multiple sources.

    Args:
        user_query: The research query
        sources: List of sources to search (default: all)

    Returns:
        Dictionary containing research results from all sources
    """
    if sources is None:
        sources = ["reddit", "arxiv"]  # Default to implemented sources

    tools = ResearchTools()
    results = {}

    try:
        # Execute searches in parallel for efficiency
        tasks = []
        if "reddit" in sources:
            tasks.append(("reddit", tools.search_reddit(user_query)))
        if "arxiv" in sources:
            tasks.append(("arxiv", tools.search_arxiv(user_query)))
        if "youtube" in sources:
            tasks.append(("youtube", tools.search_youtube(user_query)))
        if "medium" in sources:
            tasks.append(("medium", tools.search_medium(user_query)))

        # Wait for all searches to complete
        for source_name, task in tasks:
            results[source_name] = await task

    finally:
        await tools.close()

    return results


async def analyze_with_claude(user_query: str, research_data: dict) -> None:
    """
    Analyze research data using Claude and print results.

    Args:
        user_query: The original user query
        research_data: Dictionary of research results
    """
    # Verify API key is available
    try:
        get_api_key()
    except ValueError as e:
        print(f"\n⚠️  AI分析をスキップ: {e}")
        return

    # Prepare context for Claude
    context = f"""ユーザーのクエリ: {user_query}

収集したデータ:

"""
    for source, data in research_data.items():
        context += f"\n## {source.upper()} からの結果:\n"
        context += json.dumps(data, ensure_ascii=False, indent=2)
        context += "\n"

    # Create the full prompt
    prompt = f"""{get_system_prompt()}

{context}

上記のデータを分析し、以下の形式で包括的なレポートを作成してください：

1. **概要**: トピックの全体像
2. **主要な発見**: 各ソースからの重要な洞察
3. **共通テーマ**: 複数のソースで言及されているパターン
4. **推奨事項**: さらに調査すべき領域や次のステップ

日本語で分かりやすく回答してください。
"""

    # Query Claude with streaming
    options = ClaudeAgentOptions()

    # Import the message types
    from claude_agent_sdk.types import AssistantMessage, TextBlock

    async for event in claude_query(prompt=prompt, options=options):
        # Handle AssistantMessage events (contains the response)
        if isinstance(event, AssistantMessage):
            if hasattr(event, 'content'):
                for block in event.content:
                    if isinstance(block, TextBlock):
                        print(block.text, end="", flush=True)


async def run_interactive_session():
    """Run an interactive research session with the agent."""
    print("🔬 Deep Research Agent - マルチソースリサーチアシスタント")
    print("=" * 60)
    print("YouTube、Reddit、ArXiv、Mediumから情報を収集・統合します。")
    print("終了するには 'exit' または 'quit' と入力してください。")
    print("=" * 60)
    print()

    # Verify API key
    try:
        get_api_key()
    except ValueError as e:
        print(f"❌ エラー: {e}")
        print()
        print("セットアップ手順:")
        print("1. プロジェクトルートに .env ファイルを作成")
        print("2. 以下の内容を追加:")
        print("   ANTHROPIC_API_KEY=your_api_key_here")
        print("3. APIキーは https://console.anthropic.com/ で取得できます")
        return

    try:
        while True:
            # Get user input
            user_query = input("\n💭 リサーチトピック: ").strip()

            if user_query.lower() in ["exit", "quit", "終了"]:
                print("\n👋 セッションを終了します。")
                break

            if not user_query:
                continue

            print(f"\n🔍 調査中: {user_query}")
            print("-" * 60)

            # Collect research data
            print("📊 データ収集中...")
            research_data = await research_query_sources(user_query)

            print("🤖 分析中...")
            print("-" * 60)

            # Analyze with Claude
            await analyze_with_claude(user_query, research_data)

            print("\n" + "-" * 60)

    except KeyboardInterrupt:
        print("\n\n👋 セッションが中断されました。")


async def run_single_query(user_query: str):
    """
    Run a single research query and return results.

    Args:
        user_query: The research query
    """
    print(f"🔍 調査中: {user_query}\n")

    # Collect research data
    research_data = await research_query_sources(user_query)

    # Print results
    for source, data in research_data.items():
        print(f"\n{'='*60}")
        print(f"📊 {source.upper()} からの結果")
        print('='*60)
        print(json.dumps(data, ensure_ascii=False, indent=2))

    # Analyze with Claude
    print(f"\n{'='*60}")
    print("🤖 AI分析")
    print('='*60)

    await analyze_with_claude(user_query, research_data)

    print("\n")


def main():
    """Main entry point for the CLI."""
    import sys

    if len(sys.argv) > 1:
        # Single query mode
        user_query = " ".join(sys.argv[1:])
        asyncio.run(run_single_query(user_query))
    else:
        # Interactive mode
        asyncio.run(run_interactive_session())


if __name__ == "__main__":
    main()
