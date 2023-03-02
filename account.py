from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/account'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Account(db.Model):
    __tablename__ = 'account'

    account_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(64), nullable=False)
    membership_type = db.Column(db.String(64), nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, first_name, last_name, date_of_birth, gender, email, phone, membership_type, is_active):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.email = email
        self.phone = phone
        self.membership_type = membership_type
        self.is_active = is_active

    def json(self):
        return {"account_id": self.account_id, "first_name": self.first_name, "last_name": self.last_name, "date_of_birth": self.date_of_birth, "age": self.age, "gender": self.gender, "email": self.email, "phone": self.phone, "membership_type": self.membership_type, "is_active": self.is_active, "created": self.created}

with app.app_context():
    db.create_all()

@app.route("/account")
def get_all():
    accountlist = Account.query.all()
    if len(accountlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "accounts": [account.json() for account in accountlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no accounts."
        }
    ), 404

@app.route("/account/<account_id>")
def find_by_account_id(account_id):
    account = Account.query.filter_by(account_id=account_id).first()
    if account:
        return jsonify(
            {
                "code": 200,
                "data": account.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Account not found."
        }
    ), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
