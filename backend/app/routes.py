from quart import Quart, render_template, websocket


def register_routes(app: Quart) -> None:
    """Register all application routes."""

    @app.get("/")
    async def index():
        print("index")
        """Render the main game page."""
        return await render_template(
            "index.html",
        )

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