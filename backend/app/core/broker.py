import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator, AsyncIterator


class Broker:
    def __init__(self) -> None:
        self.connections = set()

    async def publish(self, message: str) -> None:
        for connection in self.connections:
            await connection.put(message)

    @asynccontextmanager
    async def subscribe(self) -> AsyncIterator[AsyncGenerator[str, None]]:
        connection = asyncio.Queue()
        self.connections.add(connection)
        try:
            async def message_generator():
                while True:
                    try:
                        yield await connection.get()
                    except asyncio.CancelledError:
                        break

            yield message_generator()
        finally:
            self.connections.remove(connection)