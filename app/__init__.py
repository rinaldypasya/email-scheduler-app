from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import os
from werkzeug.middleware.proxy_fix import ProxyFix

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=False):
    app = Flask(__name__)

    # Load config
    app.config.from_object(Config)
    
    # Set a secret key for session management and forms
    app.config['SECRET_KEY'] = os.urandom(24)

    if test_config:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import bp as main_bp # type: ignore
    app.register_blueprint(main_bp)
    
    # Ensure the app runs on 0.0.0.0 and port 8080
    app.run(host='0.0.0.0', port=8000)
    
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

    return app
