import asyncio
import httpx

async def long_conversation(client, session_id):
    for i in range(50):  # 50 messages in a conversation
        response = await client.post("http://localhost:8002/generate", json={
            "messages": [{"role": "user", "content": f"Message {i}"}]
        })
        print(f"Session {session_id}, Message {i}: {response.status_code}")

async def main():
    async with httpx.AsyncClient() as client:
        tasks = [long_conversation(client, f"session_{i}") for i in range(20)]
        await asyncio.gather(*tasks)

asyncio.run(main())
