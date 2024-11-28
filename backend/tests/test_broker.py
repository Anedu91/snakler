import asyncio
import pytest
from app.broker import Broker

@pytest.mark.asyncio
async def test_broker_publish_and_subscribe():
    # Setup
    broker = Broker()
    received_messages = []

    # Subscribe to messages
    async def collect_messages():
        async for message in broker.subscribe():
            received_messages.append(message)
            if len(received_messages) == 2:  # Break after receiving 2 messages
                break

    # Start collecting messages in the background
    collect_task = asyncio.create_task(collect_messages())

    # Give the subscriber time to set up
    await asyncio.sleep(0.1)

    # Publish messages
    test_messages = ["Hello", "World"]
    for message in test_messages:
        await broker.publish(message)

    # Wait for messages to be received
    await collect_task

    # Verify the messages were received in order
    assert received_messages == test_messages

@pytest.mark.asyncio
async def test_broker_multiple_subscribers():
    broker = Broker()
    subscriber1_messages = []
    subscriber2_messages = []

    async def subscriber1():
        async for message in broker.subscribe():
            subscriber1_messages.append(message)
            if len(subscriber1_messages) == 2:
                break

    async def subscriber2():
        async for message in broker.subscribe():
            subscriber2_messages.append(message)
            if len(subscriber2_messages) == 2:
                break

    # Start both subscribers
    task1 = asyncio.create_task(subscriber1())
    task2 = asyncio.create_task(subscriber2())

    # Give subscribers time to set up
    await asyncio.sleep(0.1)

    # Publish messages
    test_messages = ["Hello", "World"]
    for message in test_messages:
        await broker.publish(message)

    # Wait for both subscribers to receive messages
    await task1
    await task2

    # Verify both subscribers received all messages
    assert subscriber1_messages == test_messages
    assert subscriber2_messages == test_messages
