import asyncio
import pytest
from app.core.broker import Broker, BrokerMessage


@pytest.mark.asyncio
async def test_basic_publish_subscribe():
    broker = Broker()
    received = []

    async with broker.subscribe() as messages:
        await broker.publish("test message")
        async for message in messages:
            received.append(message)
            break

    assert received == ["test message"]


@pytest.mark.asyncio
async def test_broker_close():
    broker = Broker()
    received = []

    async with broker.subscribe() as messages:
        await broker.publish("message 1")
        await broker.close()

        async for message in messages:
            received.append(message)

    assert received == ["message 1"]
    assert not broker.active
    assert len(broker.connections) == 0


@pytest.mark.asyncio
async def test_multiple_subscribers_with_error():
    broker = Broker()
    received1, received2 = [], []

    async def subscriber1():
        async with broker.subscribe() as messages:
            async for message in messages:
                received1.append(message)

    async def subscriber2():
        async with broker.subscribe() as messages:
            async for message in messages:
                received2.append(message)

    # Iniciar ambos subscribers
    task1 = asyncio.create_task(subscriber1())
    task2 = asyncio.create_task(subscriber2())

    await asyncio.sleep(0.1)  # Dar tiempo para que se conecten

    # Publicar y cerrar
    await broker.publish("test message")
    await broker.close()

    # Esperar que terminen
    await task1
    await task2

    assert received1 == received2 == ["test message"]
