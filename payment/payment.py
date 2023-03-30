from flask import Flask, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
from datetime import datetime
from invokes import invoke_http

import stripe



app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

stripe.api_key = environ.get('STRIPE_API_KEY')

account_URL = environ.get('accountURL') or "http://localhost:6000/account/"

class Payment(db.Model):
    __tablename__ = 'payment'

    payment_id = db.Column(db.String(128), primary_key=True)
    account_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float, nullable=False)
    paymentDate = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, payment_id, account_id, status, price, paymentDate):
        self.payment_id = payment_id
        self.account_id = account_id
        self.status = status
        self.price = price
        self.paymentDate = paymentDate
    
    def json(self):
        return {"payment_id": self.payment_id,  
                "account_id": self.account_id, 
                "status": self.status, 
                "price": self.price, 
                "paymentDate": self.paymentDate
            }

with app.app_context():
    db.create_all()

session_id = ""

@app.route('/<int:payment_id>', methods=['GET'])
async def process_payment(payment_id):
    global session_id
    session_id = payment_id

current_user = invoke_http(account_URL, method='GET')

@app.route('/')
def hello():
    return 'Hello from the payment Microservice!'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    global session_id

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                    'price': 'price_1MjeeeExUYBuMhthqO8FblZr',
                    'quantity': 1
                }
            ],
            mode = "payment",
            #success_url and cancel_url leads to the next page depending on payment status (both are built-in to the API)
            success_url = "http://127.0.0.1:6203/retrieve-payment-data",
            cancel_url = ""
        )
        session_id = checkout_session.id
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

# if payment is successful, it will push the relevant data to the db
@app.route('/retrieve-payment-data/<string:session_id>', methods=['POST'])
def retrieve_payment_data():

    global session_id
    global current_user

    session = stripe.checkout.Session.retrieve(session_id)
    payment_status = session.payment_status

    if payment_status == 'paid':
        payment = Payment(payment_id=session_id, account_id=current_user, status=payment_status, price=8, paymentDate=datetime.now())
        db.session.add(payment)
        db.session.commit()

    return session_id

@app.get("/payment")
def get_all():
    paymentList = Payment.query.all()
    if len(paymentList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "payment": [payment.json() for payment in paymentList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no payments."
        }
    ), 404



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6203, debug=True)