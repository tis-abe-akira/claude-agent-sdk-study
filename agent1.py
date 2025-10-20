import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

async def main():

    options = ClaudeAgentOptions(
        allowed_tools=["WebSearch"],
        permission_mode="bypassPermissions",
    )

    async with ClaudeSDKClient(options=options) as client:
        # await client.query("Hello Claude")
        await client.query("Claude Agent SDK について調べて教えて")
        async for message in client.receive_response():
            print(message)

if __name__ == "__main__":
    asyncio.run(main())
