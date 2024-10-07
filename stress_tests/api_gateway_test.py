import asyncio
import httpx

async def send_request(client):
    response = await client.post("http://api-gateway-url/generate", json={
        "messages": [{"role": "user", "content": "Hello"}]
    })
    print(f"Response: {response.status_code}")

async def main():
    async with httpx.AsyncClient() as client:
        tasks = [send_request(client) for _ in range(500)]
        await asyncio.gather(*tasks)

asyncio.run(main())
