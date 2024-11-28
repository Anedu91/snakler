import asyncio
import pytest
from unittest.mock import AsyncMock, Mock
from app.core.websocket import WebSocketHandler
from app.core.broker import Broker

@pytest.fixture
def broker():
    return Broker()

@pytest.fixture
def handler(broker):
    return WebSocketHandler(broker)

@pytest.mark.asyncio
async def test_websocket_message_handling(handler):
    # Create a mock websocket with controlled behavior
    mock_ws = AsyncMock()

    # Set up the receive behavior to return one message and then hang
    receive_future = asyncio.Future()
    receive_calls = 0

    async def controlled_receive():
        nonlocal receive_calls
        if receive_calls == 0:
            receive_calls += 1
            return '{"type": "message", "payload": "test message"}'
        # After first call, wait on future (which we'll cancel)
        await receive_future

    mock_ws.receive.side_effect = controlled_receive

    # Create an event to know when our message is processed
    message_processed = asyncio.Event()
    original_send = mock_ws.send

    async def mock_send(message):
        await original_send(message)
        message_processed.set()

    mock_ws.send = mock_send

    # Start handler in background task
    handler_task = asyncio.create_task(handler.handle_connection(mock_ws))

    try:
        # Wait for the message to be processed with a timeout
        await asyncio.wait_for(message_processed.wait(), timeout=1.0)

        # Verify the message was handled correctly
        assert mock_ws.receive.call_count == 1
        assert mock_ws.send.call_count == 1

        sent_message = mock_ws.send.call_args[0][0]
        assert '"type":"message"' in sent_message
        assert '"message":"test message"' in sent_message

    finally:
        # Cleanup
        receive_future.cancel()  # Cancel the hanging receive
        handler_task.cancel()    # Cancel the handler task

        # Wait for the handler to clean up
        try:
            await asyncio.wait_for(handler_task, timeout=1.0)
        except (asyncio.CancelledError, asyncio.TimeoutError):
            pass

# @pytest.mark.asyncio
# async def test_client_count_tracking(handler):
#     mock_ws = AsyncMock()
#     mock_ws.receive.return_value = '{"type": "message", "payload": "test"}'

#     assert handler.client_count == 0

#     # Start handler
#     handler_task = asyncio.create_task(handler.handle_connection(mock_ws))
#     await asyncio.sleep(0.1)

#     assert handler.client_count == 1

#     # Cleanup should decrease count
#     handler_task.cancel()
#     try:
#         await handler_task
#     except asyncio.CancelledError:
#         pass

#     assert handler.client_count == 0

# @pytest.mark.asyncio
# async def test_invalid_message_handling(handler):
    mock_ws = AsyncMock()
    mock_ws.receive.return_value = 'invalid json'

    handler_task = asyncio.create_task(handler.handle_connection(mock_ws))
    await asyncio.sleep(0.1)

    # Verify error handling
    mock_ws.send.assert_not_called()

    # Cleanup
    handler_task.cancel()
    try:
        await handler_task
    except asyncio.CancelledError:
        pass