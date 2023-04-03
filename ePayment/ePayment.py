from flask import Flask, redirect, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
from datetime import datetime
import asyncio

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

order_URL = environ.get('orderURL') or "http://localhost:6201/order/"

class epayment(db.Model):
    __tablename__ = 'epayment'

    session_id = db.Column(db.String(128), primary_key=True)
    checkout_url = db.Column(db.String(512), nullable=False)
    account_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float, nullable=False)
    paymentDate = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, session_id, checkout_url, account_id, status, price, paymentDate):
        self.session_id = session_id
        self.checkout_url = checkout_url
        self.account_id = account_id
        self.status = status
        self.price = price
        self.paymentDate = paymentDate
    
    def json(self):
        return {"session_id": self.session_id,  
                "account_id": self.account_id, 
                "status": self.status, 
                "price": self.price, 
                "paymentDate": self.paymentDate
            }

with app.app_context():
    db.create_all()

@app.route('/')
def hello():
    return 'Hello from the epayment Microservice!'

# pls send a POST request to this endpoint to trigger it instantly
@app.route('/epayment/create_checkout_session', methods=['POST'])
def create_checkout_session():
    data = request.get_json()
    try:
        session_id = ''
        checkout = ''
        payment_status = ''
        checkout_session = stripe.checkout.Session.create(
            
            line_items = [
                {
                    'price': 'price_1MjeeeExUYBuMhthqO8FblZr',
                    'quantity': 1
                }
            ],
            mode = "payment",
            #success_url and cancel_url leads to the next page depending on payment status (both are built-in to the API)

            # cancel_url should bring it back to the main page but cancels payment
            success_url = 'http://localhost:6203/epayment/check_payment_status/{CHECKOUT_SESSION_ID}',
            cancel_url = 'http://localhost:5174/payment-mode'
        )
        session_id = checkout_session.id
        session = stripe.checkout.Session.retrieve(session_id)
        checkout = session["url"]
        payment_status = session.payment_status
    except Exception as e:
        return str(e)
    payment = epayment(session_id=session_id, checkout_url = checkout, account_id = data["account_id"], status=payment_status, price=8, paymentDate=datetime.now())
    db.session.add(payment)
    db.session.commit()
    return jsonify({"checkout_url" : checkout }), 303

@app.route('/epayment/check_payment_status/<session_id>', methods=['GET'])
async def check_payment_status(session_id):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        payment_status = session.payment_status
    except stripe.error.InvalidRequestError:
        return f"Invalid session ID: {session_id}"
    except stripe.error.APIConnectionError:
        return "Could not connect to Stripe's API"

    if payment_status == 'paid':
        # Payment has been successfully made
        payment = epayment.query.filter_by(session_id=session_id).first()
        if payment:
            payment.status = 'paid'
            db.session.commit()
            payment_json = {
                "account_id": payment.account_id,
                "session_id": payment.session_id,
                "payment_method": "external"
            }
        create_ticket = invoke_http(
            order_URL + str(payment.account_id) + "/paying", method='POST', json=payment_json
        )
        if create_ticket["code"] in range(500, 600):
            return jsonify(
                {
                    "code": 500,
                    "message": "Oops, something went wrong! Order"
                }
            ), 500
    elif payment_status == 'unpaid':
        # Payment has not yet been made
        await asyncio.sleep(30)
        return await check_payment_status()
    else:
        # Payment has failed or has been refunded
        return "Payment failed or refunded"


@app.get("/epayment")
def get_all():
    paymentList = epayment.query.all()
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