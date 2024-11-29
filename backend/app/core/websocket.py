from app.helpers import message_from_client, message_to_client
from app.typedef import ClientRole
from quart import Websocket
import asyncio
import json
from app.core.broker import Broker

class WebSocketHandler:
    def __init__(self, broker: Broker):
        self.broker = broker
        self.client_count = 0
        self.client_roles = {}
        self.role_assigned = {
            ClientRole.CLICKER: False,
            ClientRole.MOVER: False
        }
    def _assign_role(self, ws: Websocket) -> ClientRole:
        """Assigns a role to the client."""
        if not self.role_assigned[ClientRole.MOVER]:
            self.role_assigned[ClientRole.MOVER] = True
            return ClientRole.MOVER
        elif not self.role_assigned[ClientRole.CLICKER]:
            self.role_assigned[ClientRole.CLICKER] = True
            return ClientRole.CLICKER
        return ClientRole.VIEWER



    async def handle_connection(self, ws: Websocket) -> None:
        """Handles a new WebSocket connection."""
        self.client_count += 1
        role = self._assign_role(ws)
        self.client_roles[ws] = role

        try:
            # create task to receive messages from the client
            receive_task = asyncio.create_task(self._receive_messages(ws))
            # subscribe to messages from the broker - it also returns the messages to the client
            async with self.broker.subscribe() as messages:
                async for message in messages:
                    await ws.send(message)

        finally:
            # cancel the receive task
            receive_task.cancel()
            try:
                await receive_task
            except asyncio.CancelledError:
                pass
            if self.client_roles[ws] in [ClientRole.MOVER, ClientRole.CLICKER]:
                self.role_assigned[self.client_roles[ws]] = False
            del self.client_roles[ws]
            self.client_count -= 1

    async def _receive_messages(self, ws: Websocket) -> None:
        try:
            while True:
                # receive: wait for new messages
                message = await ws.receive()
                # process: delegate the processing to handle_message
                await self.handle_message(ws,message)
        except asyncio.CancelledError:
            raise
        except Exception as e:
            print(f"Error receiving message: {e}")

    async def handle_message(self, ws: Websocket, message: str) -> None:
        """Procesa y publica un mensaje al broker."""
        try:
            # handle the message and validate it before sending it to the broker
            validated_message = message_from_client(message)

            if self._can_send_message(self.client_roles[ws], validated_message.type):

                response = message_to_client(validated_message)
                # publish the message to the broker
                await self.broker.publish(response)

        except ValueError as e:
            print(f"Error processing message: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def _can_send_message(self, role: ClientRole, message_type: str) -> bool:
        """Checks if a role can send a message type."""
        permissions = {
            ClientRole.CLICKER: ["click", "message"],
        ClientRole.MOVER: ["move", "message"],
        ClientRole.VIEWER: ["message"]
    }
        return message_type in permissions[role]