from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/loyalty'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)


class Loyalty(db.Model):
    __tablename__ = 'loyalty'

    account_id = db.Column(db.ForeignKey(
        'account.account_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    # account_id = db.Column(db.ForeignKey(
    #     'account.account_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    available_points = db.Column(db.Integer, nullable=False)
    redeem_points = db.Column(db.Integer, nullable=False)
    total_points = db.Column(db.Integer, nullable=False)
    expiry = db.Column(db.DateTime)

    def __init__(self, account_id, available_points, redeem_points, total_points, expiry):
        self.account_id = account_id
        self.available_points = available_points
        self.redeem_points = redeem_points
        self.total_points = total_points
        self.expiry = expiry

    def json(self):
        return {"account_id": self.account_id, "available_points": self.available_points, "redeem_points": self.redeem_points, "total_points": self.total_points, "expiry": self.expiry}


@app.route("/loyalty/<account_id>")
def find_by_account_id(account_id):
    loyalty = Loyalty.query.filter_by(account_id=account_id).first()
    if loyalty:
        return jsonify(
            {
                "code": 200,
                "data": loyalty.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Loyalty not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
