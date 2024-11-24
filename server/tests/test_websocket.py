import asyncio
import pytest
from quart.testing.connections import TestWebsocketConnection as _TestWebsocketConnection

from chat import app

@pytest.mark.asyncio
async def test_websocket() -> None:
    test_client = app.test_client()
    async with test_client.websocket("/ws") as test_websocket:
        message = {
            "type": "message",
            "payload": "test message"
        }
        await test_websocket.send_json(message)
        try:
            result = await asyncio.wait_for(test_websocket.receive(), timeout=2.0)
            assert result is not None
        except asyncio.TimeoutError:
            pytest.fail("Websocket test timed out waiting for response")

@pytest.mark.asyncio
async def test_multiple_clients() -> None:
    test_client = app.test_client()
    async with test_client.websocket("/ws") as test_websocket1:
        async with test_client.websocket("/ws") as test_websocket2:
            message1 = {
                "type": "message",
                "payload": "test message 1"
            }
            message2 = {
                "type": "message",
                "payload": "test message 2"
            }

            await test_websocket1.send_json(message1)
            await test_websocket2.send_json(message2)

            try:
                result1 = await asyncio.wait_for(test_websocket1.receive(), timeout=2.0)
                result2 = await asyncio.wait_for(test_websocket2.receive(), timeout=2.0)
                assert result1 is not None
                assert result2 is not None
            except asyncio.TimeoutError:
                pytest.fail("Websocket test timed out waiting for response")

@pytest.mark.asyncio
async def test_invalid_json_message() -> None:
    test_client = app.test_client()
    async with test_client.websocket("/ws") as test_websocket:
        await test_websocket.send("invalid json{")
        try:
            result = await asyncio.wait_for(test_websocket.receive(), timeout=2.0)
            assert "Invalid JSON format" in result
        except asyncio.TimeoutError:
            pytest.fail("Websocket test timed out waiting for response")


@pytest.mark.asyncio
async def test_missing_required_fields() -> None:
    test_client = app.test_client()
    async with test_client.websocket("/ws") as test_websocket:
        invalid_message = {
            "payload": "test message"
        }
        await test_websocket.send_json(invalid_message)
        try:
            result = await asyncio.wait_for(test_websocket.receive(), timeout=2.0)
            assert "error" in result.lower()
        except asyncio.TimeoutError:
            pytest.fail("Websocket test timed out waiting for response")

@pytest.mark.asyncio
async def test_invalid_message_type() -> None:
    test_client = app.test_client()
    async with test_client.websocket("/ws") as test_websocket:
        invalid_message = {
            "type": "invalid_type",
            "payload": "test message"
        }
        await test_websocket.send_json(invalid_message)
        try:
            result = await asyncio.wait_for(test_websocket.receive(), timeout=2.0)
            assert "error" in result.lower()
        except asyncio.TimeoutError:
            pytest.fail("Websocket test timed out waiting for response")

@pytest.mark.asyncio
async def test_empty_message() -> None:
    test_client = app.test_client()
    async with test_client.websocket("/ws") as test_websocket:
        await test_websocket.send("")
        try:
            result = await asyncio.wait_for(test_websocket.receive(), timeout=2.0)
            assert "error" in result.lower()
        except asyncio.TimeoutError:
            pytest.fail("Websocket test timed out waiting for response")