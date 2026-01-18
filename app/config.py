import os


class Config:
    SQLALCHEMY_DATABASE_URI="sqlite:///cafes.db"
    # SQLALCHEMY_DATABASE_URI = os.getenv(
    #     "DATABASE_URL",
    #     "sqlite:///cafes.db"
    # )  # If environment variable exists → use it
    # Else → fall back to SQLite
    SQLALCHEMY_TRACK_MODIFICATION = False


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False
