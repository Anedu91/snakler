
from chat.broker import Broker
from chat.functions.move import move
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
        try:
            data = json.loads(message)
            print(data)
            if data['type'] == 'move':
                move_result = move(data, AREA)
                message = json.dumps(move_result)
                await broker.publish(message)
            else:
                await broker.publish(message)
        except json.JSONDecodeError:
            print("Non-JSON message:", message)




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
