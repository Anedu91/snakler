import pytest
from app.app import create_app

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def test_client(app):
    return app.test_client()

async def test_connect_endpoint(test_client):
    response = await test_client.get('/connect')
    assert response.status_code == 200

    data = await response.get_json()
    assert 'status' in data
    assert 'websocket_url' in data
    assert data['status'] == 'ready'
    assert data['websocket_url'] == 'ws://127.0.0.1:5000/ws'
