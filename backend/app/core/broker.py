import asyncio

from contextlib import asynccontextmanager
from enum import Enum
from typing import AsyncGenerator

from typing import Optional

class BrokerMessage:
    class Type(Enum):
        MESSAGE = "message"
        ERROR = "error"
        CLOSE = "close"

    def __init__(self, type: Type, content: Optional[str] = None, error: Optional[Exception] = None):
        self.type = type
        self.content = content
        self.error = error

class Broker:
    def __init__(self) -> None:
        self.connections = set()
        self.active = True

    async def publish(self, message: str) -> None:
        if not self.active:
            raise RuntimeError("Broker is closed")
        broker_message = BrokerMessage(BrokerMessage.Type.MESSAGE, content=message)
        for connection in self.connections:
            await connection.put(broker_message)

    async def close(self) -> None:
        if not self.active:
            return
        self.active = False
        close_message = BrokerMessage(BrokerMessage.Type.CLOSE)
        # send close message to all connections
        for connection in self.connections:
            await connection.put(close_message)

    ## adding the context manager to the subscribe method
    ## because we're returning a async generator
    @asynccontextmanager
    async def subscribe(self) -> AsyncGenerator[str, None]:
        if not self.active:
            raise RuntimeError("Broker is closed")
        connection = asyncio.Queue()
        self.connections.add(connection)
        try:
            # internal generator function to yield messages
            async def message_generator():
                while self.active or not connection.empty():
                    try:
                        message = await connection.get()

                        if message.type == BrokerMessage.Type.MESSAGE:
                            yield message.content
                        elif message.type == BrokerMessage.Type.ERROR:
                            if message.error:
                                raise message.error
                            break
                        elif message.type == BrokerMessage.Type.CLOSE:
                            break

                    # if the task is cancelled, break the loop
                    except asyncio.CancelledError:
                        break
                    # if any other exception occurs, log it and break the loop
                    except Exception as e:
                        await connection.put(BrokerMessage(
                            BrokerMessage.Type.ERROR,
                            error=e
                        ))
                        break

            yield message_generator()
        finally:
            self.connections.remove(connection)