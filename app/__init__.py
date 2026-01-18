from flask import Flask
from .config import DevConfig,ProdConfig
from .extensions import db
from .routes import api

def create_app():
    app = Flask(__name__)
    app.config.from_object(ProdConfig)

    db.init_app(app)
    # migrate.init_app(app, db)

    app.register_blueprint(api)

    return app

# export DATABASE_URL="postgresql+psycopg2://postgres:2u8iajlbbn@localhost:5432/cafes_db"
# export FLASK_APP=main.py
