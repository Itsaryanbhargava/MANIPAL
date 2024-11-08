import asyncio
import websockets

from directkeys import A, D, S, ReleaseKey,PressKey

currentKey = list()
async def handle_connection(websocket, path):
    print("Client connected.")
    try:
        async for message in websocket:
            if message=="Center":
                if currentKey:
                    for current in currentKey:
                        ReleaseKey(current)
            elif message=="Turn Right":
                PressKey(D)
                currentKey.append(D)
            elif message=="Turn Left":
                PressKey(A)
                currentKey.append(A)
                pass
            print(f"Received direction: {message}")

            
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected.")

async def main():
    async with websockets.serve(handle_connection, "192.168.202.3", 6789):
        print("WebSocket server started on ws://192.168.1.10")
        await asyncio.Future()  

asyncio.run(main())
