from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from db import db  # Импортируем SQLAlchemy
from models import User
import os

app = Flask(__name__)

# Конфигурация базы данных
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "postgresql://appuser:apppassword@db:5432/appdb")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)  # Подключаем Flask-Migrate

@app.route("/")
def home():
    return jsonify({"message": "Flask + PostgreSQL + Docker работает!"})

@app.route("/users")
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.name} for u in users])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

