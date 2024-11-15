
from chat.broker import Broker
from quart import Quart, render_template, websocket
import asyncio



app = Quart(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

broker = Broker()

async def _receive() -> None:
    while True:
        message = await websocket.receive()
        await broker.publish(message)


@app.get("/")
async def index():
    return await render_template("index.html")

@app.websocket("/ws")
async def ws() -> None:
    try:
        task = asyncio.ensure_future(_receive())
        async for message in broker.subscribe():
            print(message)
            await websocket.send(message)
    finally:
        task.cancel()
        await task

def run() -> None:
    app.run()
