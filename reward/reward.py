from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
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
    exchange_points = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(256))
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False,
                         default=datetime.now, onupdate=datetime.now)

    def __init__(self, name, description, quantity, exchange_points, image_url, is_active):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.exchange_points = exchange_points
        self.image_url = image_url
        self.is_active = is_active

    def json(self):
        return {"reward_id": self.reward_id, "name": self.name, "description": self.description, "quantity": self.quantity, "exchange_points": self.exchange_points, "image_url": self.image_url, "is_active": self.is_active, "created": self.created, "modified": self.modified}


with app.app_context():
    db.create_all()


@app.route("/reward")
def get_all():
    rewardlist = Reward.query.all()
    if len(rewardlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "rewards": [reward.json() for reward in rewardlist]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "There are no rewards."
        }
    ), 404


@app.route("/reward/active")
def get_active_rewards():
    activerewardlist = Reward.query.filter_by(is_active=True).all()
    if len(activerewardlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "rewards": [reward.json() for reward in activerewardlist]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "There are no active rewards."
        }
    ), 404


@app.route("/reward/<reward_id>")
def find_by_reward_id(reward_id):
    reward = Reward.query.filter_by(reward_id=reward_id).first()
    if reward:
        return jsonify(
            {
                "code": 200,
                "data": reward.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Reward not found."
        }
    ), 404


@app.route("/reward", methods=['POST'])
def create_reward():
    data = request.get_json()
    reward = Reward(**data)

    existing_reward = Reward.query.filter_by(name=reward.name).first()

    if (existing_reward):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "reward_id": existing_reward.reward_id
                },
                "message": "Reward already exists."
            }
        ), 400

    try:
        db.session.add(reward)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the reward."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": reward.json()
        }
    ), 201


@app.route("/reward/<reward_id>", methods=['PUT'])
def update_reward(reward_id):
    if (not Reward.query.filter_by(reward_id=reward_id).first()):
        return jsonify(
            {
                "code": 404,
                "data": {
                    "reward_id": reward_id
                },
                "message": "Reward not found."
            }
        ), 404

    reward = Reward.query.filter_by(reward_id=reward_id).first()
    data = request.get_json()

    try:
        reward.name = data['name']
        reward.description = data['description']
        reward.quantity = data['quantity']
        reward.exchange_points = data['exchange_points']
        reward.image_url = data['image_url']
        reward.is_active = data['is_active']
        db.session.commit()

    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "reward_id": reward_id
                },
                "message": "An error occurred updating the reward."
            }
        ), 500

    return jsonify(
        {
            "code": 200,
            "data": reward.json()
        }
    ), 200


@app.route("/reward/<reward_id>", methods=['DELETE'])
def delete_reward(reward_id):
    if (not Reward.query.filter_by(reward_id=reward_id).first()):
        return jsonify(
            {
                "code": 404,
                "data": {
                    "reward_id": reward_id
                },
                "message": "Reward not found."
            }
        ), 404

    reward = Reward.query.filter_by(reward_id=reward_id).first()

    try:
        db.session.delete(reward)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "reward_id": reward_id
                },
                "message": "An error occurred deleting the reward."
            }
        ), 500

    return jsonify(
        {
            "code": 200,
            "message": "Reward with ID " + reward_id + " successfully deleted."
        }
    ), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6303, debug=True)
