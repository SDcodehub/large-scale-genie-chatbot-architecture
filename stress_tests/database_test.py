import asyncio
import httpx

async def add_and_retrieve_message(session_id):
    async with httpx.AsyncClient() as client:
        await client.post("http://localhost:8003/add_message", json={
            "session_id": session_id,
            "role": "user",
            "content": "Test message"
        })
        response = await client.get(f"http://localhost:8003/get_history/{session_id}")
        print(f"Retrieved {len(response.json())} messages for session {session_id}")

async def main():
    tasks = [add_and_retrieve_message(f"session_{i}") for i in range(1000)]
    await asyncio.gather(*tasks)

asyncio.run(main())
