from flask import Flask

from .config import Config
from .routes.cipher_routes import cipher_bp
from .routes.main import main_bp
from .routes.api_routes import api_bp


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    app.register_blueprint(main_bp)
    app.register_blueprint(cipher_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


# Expose a module-level WSGI application named `app` so servers like gunicorn
# can import `app` directly (e.g. `gunicorn app:app`). This keeps the
# factory function for testing while providing a simple entrypoint for WSGI.
app = create_app()
