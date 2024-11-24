
from chat.broker import Broker
from chat.helpers import message_from_client, message_to_client
from chat.typedef import MessageFromClient
from quart import Quart, render_template, websocket
import asyncio



app = Quart(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

broker = Broker()
connected_clients = 0
MAX_CLIENTS = 2

async def _receive() -> None:
    while True:
        try:
            message = await websocket.receive()
            try:
                parsed_message = message_from_client(message)
                message_to_broker = message_to_client(parsed_message)
                await broker.publish(message_to_broker)

            except ValueError as e:

                error_response = message_to_client(MessageFromClient(
                    type="error",
                    payload={"message": str(e)}
                ))
                await websocket.send(error_response)

            except Exception as e:
                # Otros errores inesperados durante el procesamiento
                error_response = message_to_client(MessageFromClient(
                    type="error",
                    payload={"message": "Internal server error"}
                ))
                await websocket.send(error_response)
                print(f"Unexpected error processing message: {str(e)}")

        except asyncio.CancelledError:
            # El websocket está siendo cerrado normalmente
            try:
                close_message = message_to_client(MessageFromClient(
                    type="system",
                    payload={"message": "Connection closing"}
                ))
                await websocket.send(close_message)
            except:
                pass  # Ignoramos errores al enviar el mensaje de cierre
            raise

        except Exception as e:
            # Error en la conexión del websocket
            print(f"Websocket error: {str(e)}")
            raise

AREA = 500
SNAKE_POSITION = {"x": 0, "y": 0}

@app.get("/")
async def index():
    return await render_template("index.html", area=AREA, snake_position=SNAKE_POSITION)

@app.websocket("/ws")
async def ws() -> None:
    global connected_clients

    if connected_clients >= MAX_CLIENTS:
        await websocket.close(1008, "Max clients reached")
        return
    try:
        connected_clients += 1
        task = asyncio.create_task(_receive())
        async for message in broker.subscribe():
            await websocket.send(message)
    except asyncio.CancelledError:
        print("Websocket connection cancelled")
        raise
    except Exception as e:
        print(f"Error in websocket connection: {str(e)}")
        raise
    finally:
        connected_clients -= 1
        if task and not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            except Exception as e:
                print(f"Error during task cleanup: {str(e)}")

def run() -> None:
    app.run()
