from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from ypy_websocket.websocket_server import WebsocketServer  # type: ignore

app_dir = Path(__file__).parent.parent / "app" / "dist"
print(app_dir)

app = FastAPI()
app.mount("/app", StaticFiles(directory=app_dir, html=True), name="app")

websocket_server = WebsocketServer(auto_clean_rooms=False)

@app.get("/", response_class=RedirectResponse)
async def root():
    return "/app"

@app.websocket("/doc/{path:path}")
async def doc(websocket: WebSocket, path: str):
    print("[DOC] path:", path)
    await websocket.accept()

    print("[DOC] rooms:")
    for path, room in  websocket_server.rooms.items():
        print("Room:", path, room.ready)
        for client in room.clients:
            print(client)

    room = websocket_server.get_room(path)
    source = room.ydoc.get_text('source')
    idSource = source.observe(callbackText)
    todo = room.ydoc.get_array('todo')
    idTodo = todo.observe(callbackArray)
    print("[DOC] room ready:", room.ready)
    print("[DOC] todo:", todo.to_json())

    print("[DOC] serve")
    await websocket_server.serve(WebsocketAdapter(websocket, path))

def callbackText(event):
    print(str(event.target))

def callbackArray(event):
    print(event.target.to_json())

class WebsocketAdapter:
    """An adapter to make a Starlette's WebSocket look like a ypy-websocket's WebSocket"""

    def __init__(self, websocket, path: str):
        self._websocket = websocket
        self._path = path

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, value: str) -> None:
        self._path = value

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            message = await self._websocket.receive_bytes()
        except WebSocketDisconnect:
            raise StopAsyncIteration()
        return message

    async def send(self, message):
        await self._websocket.send_bytes(message)

    async def recv(self):
        return await self._websocket.receive_bytes()
