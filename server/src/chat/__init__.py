
from chat.broker import Broker
from chat.helpers import message_from_client, message_to_client
from quart import Quart, render_template, websocket
import json
import asyncio



app = Quart(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

broker = Broker()

async def _receive() -> None:
    while True:
        message = await websocket.receive()
        message_to_broker = message_to_client(message_from_client(message))
        print(message_to_broker)
        await broker.publish(message)




AREA = 500
SNAKE_POSITION = {"x": 0, "y": 0}

@app.get("/")
async def index():
    return await render_template("index.html", area=AREA, snake_position=SNAKE_POSITION)

@app.websocket("/ws")
async def ws() -> None:
    try:
        task = asyncio.ensure_future(_receive())
        async for message in broker.subscribe():
            await websocket.send(message)
    finally:
        task.cancel()
        await task

def run() -> None:
    app.run()
