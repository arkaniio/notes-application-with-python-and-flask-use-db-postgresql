from flask import Flask
from .config import connection_db, Config
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
jwt_flask = JWTManager()

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
    jwt_flask.init_app(app)

    #define the models from db
    from app.models import user
    from app.models import notes

    #define the routes for an api
    from app.routes.base_routes import base
    app.register_blueprint(base, url_prefix="/")

    #define the routes for register user 
    from app.routes.auth_routes import register_bp
    app.register_blueprint(register_bp, url_prefix="/api/v1/register")

    #define the routes for login user
    from app.routes.auth_routes import login_bp
    app.register_blueprint(login_bp, url_prefix="/api/v1/login")

    #define the routes for get profile identity user
    from app.routes.user_routes import getIdUser_bp
    app.register_blueprint(getIdUser_bp, url_prefix="/api/v1/user/profile")

    #define the routes for update user
    from app.routes.user_routes import updateIdUser_bp
    app.register_blueprint(updateIdUser_bp, url_prefix="/api/v1/user/update")

    #define the routes for file user (profile image and thumbnail image)
    from app.routes.file_routes import file_routes_bp
    app.register_blueprint(file_routes_bp, url_prefix="/uploads")

    #define the routes for notes 
    from app.routes.note_routes import note_bp
    app.register_blueprint(note_bp, url_prefix="/api/v1/note")

    #define the route for like toggle
    from app.routes.like_routes import like_bp
    app.register_blueprint(like_bp, url_prefix="/api/v1/like")


    return app