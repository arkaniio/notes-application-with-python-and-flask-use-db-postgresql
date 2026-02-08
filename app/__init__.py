from flask import Flask
from .config import connection_db, Config
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()

def create_app ():
    app = Flask(__name__)

    #connect into a config from flask api
    app.config.from_object(Config)
    #running the connection of the db function
    connection_db()

    #settings the library for models
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    #define the models of the user from db
    from app.models import user

    #define the routes for an api
    from app.routes.base_routes import base

    #define the routes for register user 
    from app.routes.auth_routes import register_bp

    # inisialisasi blueprint dari routes yang udah di create / bikin
    app.register_blueprint(base, url_prefix="/")
    app.register_blueprint(register_bp, url_prefux="/")

    return app