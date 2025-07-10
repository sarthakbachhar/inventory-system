import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    DATABASE_URL = os.environ.get("DATABASE_URL")

    # Explicitly set driver to psycopg (v3)
    if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
        SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://")
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
