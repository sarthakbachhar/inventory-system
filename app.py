from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Initialize Flask app and load config
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# Example model (you can change this)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

# Example route
@app.route("/")
def home():
    return "Flask app is running!"

# Only create tables when run directly, not during import on Render
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
