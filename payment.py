from flask import Flask, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import relationship
import stripe
import time
import uuid

stripe.api_key = "sk_test_51Mje25ExUYBuMhthy0bqpXVWnlkZCIaXAXYGZnywGjHeaXHJt10zluQUIdouAkoTDwPGhl5qgFJjStOUJODO1uyH00nseC9g53"

from datetime import datetime

app = Flask(__name__, static_url_path="", static_folder="paymenttest")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/payment'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

class Payment(db.Model):
    __tablename__ = 'payment'

    payment_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String, nullable=False)
    account_id = db.Column(db.Integer, nullable=False)
    paid = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Float, nullable=False)
    paymentDate = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, payment_id, order_id, account_id, paid, price, paymentDate):
        self.payment_id = payment_id
        self.order_id = order_id
        self.account_id = account_id
        self.paid = paid
        self.price = price
        self.paymentDate = datetime.now()
    
    def json(self):
        return {"payment_id": self.payment_id, 
                "order_id": self.order_id, 
                "account_id": self.account_id, 
                "paid": self.paid, 
                "price": self.price, 
                "paymentDate": self.paymentDate
            }

#Our domain url
YOUR_DOMAIN = "http://127.0.0.1:6203"

session_ids = []

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items = [
                {
                    'price': 'price_1MjeeeExUYBuMhthqO8FblZr',
                    'quantity': 1
                }
            ],
            mode = "payment",
            success_url = YOUR_DOMAIN + "/retrieve-payment-data",
            cancel_url = YOUR_DOMAIN + "/cancel.html"
        )
        session_ids.append(checkout_session.id)
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

# able to retrieve paid/unpaid, payment_statuses[0] is first payment
@app.route('/retrieve-payment-data', methods=['GET'])
def retrieve_payment_data():
    payment_statuses = []
    for session_id in session_ids:
    # Retrieve the details of a session with a specific ID
        session = stripe.checkout.Session.retrieve(session_id)
        payment_statuses.append(session.payment_status)

    return payment_statuses


# @app.get("/payment")
# def get_all():
#     paymentList = Payment.query.all()
#     if len(paymentList):
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": {
#                     "payment": [payment.json() for payment in paymentList]
#                 }
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "There are no payments."
#         }
#     ), 404

# @app.get("/payment/<int:payment_id>")
# def get_by_id(payment_id):
#     payment = Payment.query.filter_by(payment_id=payment_id).first()
#     if payment:
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": payment.json()
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "Payment not found."
#         }
#     ), 404

# @app.post("/order")
# def create_order():
#     if request.json is None:
#         raise Exception("No data received.")
#     try:
#         data = request.get_json()
#         new_payment = Payment(**data)
#         db.session.add(new_payment)
#         db.session.commit()
#         db.session.refresh(new_payment)
#     except:
#         return jsonify(
#             {
#                 "code": 500,
#                 "data": {
#                     "order_id": new_payment.payment_id
#                 },
#                 "message": "An error occurred creating the payment."
#             }
#         ), 500
    
#     return jsonify(
#         {
#             "code": 201,
#             "data": new_payment.json()
#         }
#     ), 201

# @app.delete("/payment/<int:payment_id>")
# def delete_payment(payment_id):
#     payment = Payment.query.filter_by(payment_id=payment_id).first()
#     if payment:
#         db.session.delete(payment)
#         db.session.commit()
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": {
#                     "payment_id": payment.payment_id
#                 }
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "Order not found."
#         }
#     ), 404




if __name__ == '__main__':
    app.run(port=6203, debug=True)