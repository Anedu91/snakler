import asyncio
import json
from app.typedef import ClientRole
import pytest
from quart import Quart, websocket
from app.core.websocket import WebSocketHandler
from app.core.broker import Broker

@pytest.fixture
def app():
    app = Quart(__name__)

    # Crear el broker y websocket handler
    broker = Broker()
    ws_handler = WebSocketHandler(broker)

    # Registrar la ruta del websocket
    @app.websocket('/ws')
    async def ws():
        await ws_handler.handle_connection(websocket)

    # Guardar las referencias en la app
    app.ws_handler = ws_handler
    app.broker = broker

    return app

@pytest.fixture
def websocket_handler(app):
    return app.ws_handler



@pytest.mark.asyncio
async def test_basic_connection(app, websocket_handler):
    async with app.test_client().websocket('/ws') as _:
        # wait for the connection to be established
        await asyncio.sleep(0.1)

        assert websocket_handler.client_count == 1

    # wait for the connection to be closed
    await asyncio.sleep(0.1)
    assert websocket_handler.client_count == 0


@pytest.mark.asyncio
async def test_role_assignment(app, websocket_handler):
    # first client should be a mover
    async with app.test_client().websocket('/ws') as client1:
        task1 = asyncio.create_task(websocket_handler.handle_connection(client1))
        await asyncio.sleep(0.1)
        assert websocket_handler.client_roles[client1] == ClientRole.MOVER

        # second client should be a clicker
        async with app.test_client().websocket('/ws') as client2:
            task2 = asyncio.create_task(websocket_handler.handle_connection(client2))
            await asyncio.sleep(0.1)
            assert websocket_handler.client_roles[client2] == ClientRole.CLICKER

            async with app.test_client().websocket('/ws') as client3:
                task3 = asyncio.create_task(websocket_handler.handle_connection(client3))
                await asyncio.sleep(0.1)
                assert websocket_handler.client_roles[client3] == ClientRole.VIEWER

                await client3.close(1000)
            await client2.close(1000)
        await client1.close(1000)

        try:
            await asyncio.gather(task1, task2, task3)
        except Exception:
            pass
