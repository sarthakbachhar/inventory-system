import os

uri = os.getenv("DATABASE_URL", "sqlite:///inventory.db")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql+psycopg://", 1)

SQLALCHEMY_DATABASE_URI = uri
SQLALCHEMY_TRACK_MODIFICATIONS = False
