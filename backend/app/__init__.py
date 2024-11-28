from app.app import create_app, run, run_debug

app = create_app()

__all__ = ['app', 'run', 'run_debug']