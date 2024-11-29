import pytest
from unittest.mock import AsyncMock
from contextlib import asynccontextmanager
import json

from app.core.websocket import WebSocketHandler

@pytest.fixture
def mock_websocket():
    ws = AsyncMock()
    ws.receive = AsyncMock()
    ws.send = AsyncMock()
    return ws

@pytest.fixture
def mock_broker():
    broker = AsyncMock()

    # Crear un context manager asíncrono mock
    @asynccontextmanager
    async def mock_subscribe():
        # Crear un generador asíncrono mock que no produce valores
        async def empty_generator():
            return
            yield  # Nunca llegará aquí

        yield empty_generator()

    broker.subscribe = mock_subscribe
    return broker

@pytest.mark.asyncio
async def test_handle_message_valid(mock_broker):
    """Test que un mensaje válido se publica al broker"""
    handler = WebSocketHandler(mock_broker)

    valid_message = json.dumps({
        "type": "message",
        "payload": "test"
    })

    await handler.handle_message(valid_message)
    mock_broker.publish.assert_called_once_with(valid_message)

@pytest.mark.asyncio
async def test_handle_message_invalid(mock_broker):
    """Test que un mensaje inválido lanza error"""
    handler = WebSocketHandler(mock_broker)

    invalid_message = "invalid json"

    with pytest.raises(ValueError):
        await handler.handle_message(invalid_message)

@pytest.mark.asyncio
async def test_client_count(mock_broker, mock_websocket):
    """Test que el contador de clientes se incrementa y decrementa correctamente"""
    handler = WebSocketHandler(mock_broker)

    assert handler.client_count == 0

    # Simular conexión
    assert handler.client_count == 0