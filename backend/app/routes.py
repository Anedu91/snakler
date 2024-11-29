from quart import Quart, jsonify, websocket


def register_routes(app: Quart) -> None:
    """Register all application routes."""

    @app.get("/connect")
    async def connect():
        """Initial connection endpoint."""
        return jsonify({
            "status": "ready",
            "websocket_url": "ws://127.0.0.1:5000/ws"
        })

    @app.websocket("/ws")
    async def ws():
        """Handle WebSocket connections."""
        if app.ws_handler.client_count >= app.config["MAX_CLIENTS"]:
            await websocket.close(1008, "Max clients reached")
            return

        try:
            await app.ws_handler.handle_connection(websocket)
        except Exception as e:
            app.logger.error(f"WebSocket error: {str(e)}")
            raise