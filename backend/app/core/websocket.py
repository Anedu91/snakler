from quart import Websocket
import asyncio
from app.core.broker import Broker
from app.helpers import message_from_client, message_to_client


class WebSocketHandler:
    def __init__(self, broker: Broker):
        self.broker = broker
        self.client_count = 0

    async def handle_connection(self, ws: Websocket) -> None:
        """Handle a new WebSocket connection."""
        self.client_count += 1
        receive_task = None

        try:
            # Create a task for receiving messages
            receive_task = asyncio.create_task(self._handle_receive(ws))

            # Subscribe to broker messages
            async with self.broker.subscribe() as messages:
                async for message in messages:
                    await ws.send(message)

        except asyncio.CancelledError:
            # Clean cancellation
            if receive_task and not receive_task.done():
                receive_task.cancel()
                try:
                    await receive_task
                except asyncio.CancelledError:
                    pass
            raise

        finally:
            self.client_count -= 1
            if receive_task and not receive_task.done():
                receive_task.cancel()
                try:
                    await receive_task
                except asyncio.CancelledError:
                    pass

    async def _handle_receive(self, ws: Websocket) -> None:
        """Handle incoming messages from the WebSocket."""
        try:
            while True:
                raw_message = await ws.receive()
                message = message_from_client(raw_message)
                response = message_to_client(message)
                await self.broker.publish(response)
        except asyncio.CancelledError:
            # Clean exit on cancellation
            raise

    async def _handle_disconnect(self, ws: Websocket) -> None:
        """Handle WebSocket disconnection."""
        try:
            await ws.send({"type": "system", "message": "Connection closing"})
        except:
            pass

    async def _handle_error(self, ws: Websocket, error: Exception) -> None:
        """Handle WebSocket errors."""
        error_message = {
            "type": "error",
            "message": str(error) if not isinstance(error, asyncio.CancelledError) else "Connection closed"
        }
        try:
            await ws.send(error_message)
        except:
            pass