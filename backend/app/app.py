from quart import Quart

from app.core.broker import Broker
from app.core.websocket import WebSocketHandler
from app.routes import register_routes

def create_app() -> Quart:

    app = Quart(__name__)

    app.config.update(
      MAX_CLIENTS=2,
      DEBUG=False
    )

    # Initialize services
    app.Broker = Broker()
    app.ws_handler = WebSocketHandler(app.Broker)

    #register routes
    register_routes(app)
    return app


def run(debug:bool = False) -> None:
    """Run the Quart application."""
    app = create_app()
    app.run(debug=debug)

def run_debug() -> None:
    """Run the Quart application in debug mode."""
    run(debug=True)

if __name__ == "__main__":
    run_debug()

