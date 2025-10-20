"""Simple example of using the research tools directly."""

import asyncio
import json
from deep_research.tools import ResearchTools


async def main():
    """Run a simple search across Reddit and ArXiv."""
    tools = ResearchTools()

    try:
        # Search for "artificial intelligence" on Reddit
        print("🔍 Searching Reddit for 'artificial intelligence'...")
        print("=" * 60)
        reddit_results = await tools.search_reddit(
            query="artificial intelligence",
            subreddit="artificial",
            limit=5
        )
        print(json.dumps(reddit_results, ensure_ascii=False, indent=2))

        print("\n" + "=" * 60)
        print("🔍 Searching ArXiv for 'machine learning'...")
        print("=" * 60)
        arxiv_results = await tools.search_arxiv(
            query="machine learning",
            max_results=5
        )
        print(json.dumps(arxiv_results, ensure_ascii=False, indent=2))

    finally:
        await tools.close()


if __name__ == "__main__":
    asyncio.run(main())
