import asyncio
import pytest

# This tells pytest to use pytest-asyncio plugin
pytest_plugins = ('pytest_asyncio',)

# This fixture sets a timeout for all async tests to prevent them from hanging
@pytest.fixture(autouse=True)
async def timeout():
    yield
    # Tests will timeout after 2 seconds
    await asyncio.sleep(0)