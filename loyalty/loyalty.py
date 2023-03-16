from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

from datetime import datetime

from invokes import invoke_http

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

verification_URL = environ.get('verificationURL') or "http://localhost:6001/verification/"


class Loyalty(db.Model):
    __tablename__ = 'loyaltys'
    account_id = db.Column(db.Integer, nullable=False,
                           primary_key=True, unique=True)
    available_points = db.Column(db.Integer, nullable=False, default=0)
    redeemed_points = db.Column(db.Integer, nullable=False, default=0)
    total_points = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, account_id, available_points, redeemed_points, total_points):
        self.account_id = account_id
        self.available_points = available_points
        self.redeemed_points = redeemed_points
        self.total_points = total_points

    def json(self):
        return {"account_id": self.account_id, "available_points": self.available_points, "redeemed_points": self.redeemed_points, "total_points": self.total_points}


with app.app_context():
    db.create_all()


@app.route("/loyalty")
def get_all():
    loyaltylist = Loyalty.query.all()
    if len(loyaltylist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "loyalties": [loyalty.json() for loyalty in loyaltylist]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "There are no loyalties."
        }
    ), 404


@app.route("/loyalty/<account_id>")
def find_loyalty_by_account_id(account_id):
    loyalty = Loyalty.query.filter_by(account_id=account_id).first()
    if loyalty:
        return jsonify(
            {
                "code": 200,
                "data": loyalty.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Loyalty not found."
        }
    ), 404


@app.route("/loyalty", methods=['POST'])
def create_loyalty():
    data = request.get_json()
    loyalty = Loyalty(**data)

    existing_loyalty = Loyalty.query.filter_by(
        account_id=loyalty.account_id).first()

    if (existing_loyalty):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "account_id": existing_loyalty.account_id
                },
                "message": "Loyalty already exists."
            }
        ), 400

    account_result = invoke_http(
        verification_URL + "account/" + str(loyalty.account_id), method='GET')

    if account_result["code"] in range(500, 600):
        return jsonify(
            {
                "code": 500,
                "message": "Oops, something went wrong!"
            }
        ), 500

    if account_result["code"] in range(300, 500):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "account_id": loyalty.account_id
                },
                "message": "Account does not exist."
            }
        ), 400

    try:
        db.session.add(loyalty)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred during creation of loyalty."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": loyalty.json()
        }
    ), 201


@app.route("/loyalty/<account_id>/earn", methods=['PATCH'])
def update_loyalty_earn(account_id):
    if (not Loyalty.query.filter_by(account_id=account_id).first()):
        return jsonify(
            {
                "code": 404,
                "data": {
                    "account_id": account_id
                },
                "message": "Loyalty not found."
            }
        ), 404

    loyalty = Loyalty.query.filter_by(account_id=account_id).first()
    data = request.get_json()

    try:
        loyalty.total_points += data['points']
        loyalty.available_points += data['points']
        db.session.commit()

    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "account_id": account_id
                },
                "message": "An error occurred updating the loyalty."
            }
        ), 500

    return jsonify(
        {
            "code": 200,
            "data": loyalty.json()
        }
    ), 200


@app.route("/loyalty/<account_id>/redeem", methods=['PATCH'])
def update_loyalty_redeem(account_id):
    if (not Loyalty.query.filter_by(account_id=account_id).first()):
        return jsonify(
            {
                "code": 404,
                "data": {
                    "account_id": account_id
                },
                "message": "Loyalty not found."
            }
        ), 404

    loyalty = Loyalty.query.filter_by(account_id=account_id).first()
    data = request.get_json()

    if data["points"] > loyalty.available_points:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "account_id": loyalty.account_id,
                    "available_points": loyalty.available_points
                },
                "message": "Insufficient available points to redeem."
            }
        ), 400

    try:
        loyalty.redeemed_points += data['points']
        loyalty.available_points -= data['points']
        db.session.commit()

    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "account_id": account_id
                },
                "message": "An error occurred updating the loyalty."
            }
        ), 500

    return jsonify(
        {
            "code": 200,
            "data": loyalty.json()
        }
    ), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6301, debug=True)
