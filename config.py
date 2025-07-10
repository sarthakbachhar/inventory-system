import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    uri = os.environ.get('DATABASE_URL', 'sqlite:///inventory.db')
    if uri.startswith("postgres://"):
    	uri = uri.replace("postgres://", "postgresql+psycopg://", 1)
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
