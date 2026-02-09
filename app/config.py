import os
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

def postgresql_url () -> str:
    user = os.getenv("DB_USER", "appuser2")
    host = os.getenv("DB_HOST", "localhost")
    password = os.getenv("DB_PASSWORD", "app123")
    name = os.getenv("DB_NAME", "Cuy_Notes")
    port = os.getenv("DB_PORT", "5432")
    return f"postgresql://{user}:{password}@{host}:{port}/{name}"

class Config:
    SQLALCHEMY_DATABASE_URI = postgresql_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "yondaktaukoktanyasaya")
    JWT_ALGORITHMS = "HS256"

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)

def connection_db ():
    try:
        url = Config.SQLALCHEMY_DATABASE_URI
        connect_engine = create_engine(url)
        connect = connect_engine.connect()
        print("Database connection into postgresql has been successfully!")
        connect.close()
        return True
    except OperationalError as e:
        raise RuntimeError(f"Error database connection has been detected: {e}")
