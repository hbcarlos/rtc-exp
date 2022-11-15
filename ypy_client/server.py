import asyncio
from websockets import serve
from ypy_websocket import WebsocketServer

async def server():
    websocket_server = WebsocketServer()
    async with serve(websocket_server.serve, "localhost", 8888):
        await asyncio.Future()  # run forever

asyncio.run(server())
