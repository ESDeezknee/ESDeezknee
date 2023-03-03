from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/reward'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)


class Reward(db.Model):
    __tablename__ = 'reward'

    reward_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(256))
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False,
                         default=datetime.now, onupdate=datetime.now)

    def __init__(self, name, description, quantity, image_url, is_active):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.image_url = image_url
        self.is_active = is_active

    def json(self):
        return {"reward_id": self.reward_id, "name": self.name, "description": self.description, "quantity": self.quantity, "image_url": self.image_url, "is_active": self.is_active, "created": self.created, "modified": self.modified}

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6303, debug=True)
