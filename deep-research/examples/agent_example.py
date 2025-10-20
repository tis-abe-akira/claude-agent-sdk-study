"""Example of using the Deep Research Agent."""

import asyncio
from deep_research.main import analyze_with_claude, research_query_sources


async def main():
    """Demonstrate the research agent capabilities."""

    # Example 1: Collect data from multiple sources
    print("📊 Example 1: Data Collection")
    print("=" * 60)

    user_query = "quantum computing"
    print(f"Query: {user_query}\n")

    # Collect data from Reddit and ArXiv
    results = await research_query_sources(user_query, sources=["reddit", "arxiv"])

    print("Results:")
    for source, data in results.items():
        print(f"\n{source.upper()}:")
        print(f"  Total results: {data.get('total_results', 0)}")
        if 'error' in data:
            print(f"  Error: {data['error']}")

    # Example 2: Use the agent to analyze and synthesize
    print("\n\n🤖 Example 2: AI Analysis")
    print("=" * 60)

    user_query2 = "量子コンピューティング"
    print(f"Query: {user_query2}")
    print("\nResponse:")
    print("-" * 60)

    # Collect data and analyze
    research_data = await research_query_sources(user_query2)
    await analyze_with_claude(user_query2, research_data)

    print("\n" + "-" * 60)


if __name__ == "__main__":
    asyncio.run(main())
