from imp import reload
import typer
import uvicorn

from .app import app as fast_app

app = typer.Typer()

@app.command()
def start(host: str = "localhost", port: int = 8888):
    config = uvicorn.Config(fast_app, host=host, port=port, reload=True)
    server = uvicorn.Server(config)
    server.run()
