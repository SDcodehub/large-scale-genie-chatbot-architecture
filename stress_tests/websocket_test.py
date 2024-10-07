import asyncio
import websockets

async def connect_and_send():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send('{"content": "Hello"}')
        response = await websocket.recv()
        print(f"Received: {response}")

async def main():
    tasks = [connect_and_send() for _ in range(100)]  # 100 concurrent connections
    await asyncio.gather(*tasks)

asyncio.run(main())
