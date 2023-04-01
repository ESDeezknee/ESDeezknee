from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

from datetime import datetime

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Account(db.Model):
    __tablename__ = 'accounts'

    account_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(64), nullable=False)
    is_express = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, first_name, last_name, date_of_birth, age, gender, email, phone, is_express, is_active):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.age = age
        self.gender = gender
        self.email = email
        self.phone = phone
        self.is_express = is_express
        self.is_active = is_active

    def json(self):
        return {"account_id": self.account_id, "first_name": self.first_name, "last_name": self.last_name, "date_of_birth": self.date_of_birth, "age": self.age, "gender": self.gender, "email": self.email, "phone": self.phone, "is_express": self.is_express, "is_active": self.is_active, "created": self.created}



with app.app_context():
    db.create_all()
    existing_account_1 = db.session.query(Account).filter(Account.account_id==1).first()
    if not existing_account_1:
      new_account_1 = Account(first_name="Benji", last_name="Ng", date_of_birth="2000-01-01", age=23, gender="M", email="kangting.ng.2021@scis.smu.edu.sg", phone="+6597861048", is_express=0, is_active=1)
      new_account_2 = Account(first_name="Wei Lun", last_name="Teo", date_of_birth="2002-01-01", age=21, gender="F", email="weilun.teo.2021@scis.smu.edu.sg", phone="+6585339293", is_express=0, is_active=1)
      new_account_3 = Account(first_name="Zachary", last_name="Lian", date_of_birth="2000-01-01", age=23, gender="M", email="zacharylian.2021@scis.smu.edu.sg", phone="+6592977881", is_express=0, is_active=1)
      new_account_4 = Account(first_name="Joel", last_name="Tan", date_of_birth="2000-01-01", age=23, gender="M", email="joel.tan.2021@scis.smu.edu.sg", phone="+6590605085", is_express=0, is_active=1)
      new_account_5 = Account(first_name="Keith", last_name="Law", date_of_birth="2000-01-01", age=23, gender="M", email="keith.law.2021@scis.smu.edu.sg", phone="+6594761445", is_express=0, is_active=1)
      new_account_6 = Account(first_name="Vanessa", last_name="Lee", date_of_birth="2002-01-01", age=21, gender="F", email="vanessa.lee.2021@scis.smu.edu.sg", phone="+6597634941", is_express=0, is_active=1)
      db.session.add(new_account_1)
      db.session.add(new_account_2)
      db.session.add(new_account_3)
      db.session.add(new_account_4)
      db.session.add(new_account_5)
      db.session.add(new_account_6)
      db.session.commit()



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
        ), 200
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
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Account not found."
        }
    ), 404


@app.route("/account/email/<email>")
def find_by_email(email):
    account = Account.query.filter_by(email=email).first()
    if account:
        return jsonify(
            {
                "code": 200,
                "data": account.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Account not found."
        }
    ), 404

@app.route("/account/<int:account_id>", methods=['PATCH'])
def update_is_express(account_id):
    account = Account.query.filter_by(account_id=account_id).first()
    if account:
        data = request.get_json()
        account.is_express = data['is_express']
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "Account is_express updated.", 
                "data": data
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Account not found.", 
            "data": data
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6003, debug=True)
