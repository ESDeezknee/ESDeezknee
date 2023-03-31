from flask import Flask, request, jsonify, abort, Response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
import sys, os
import asyncio

import requests
from invokes import invoke_http
import pika
import amqp_setup
import json

from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

verification_URL = environ.get('verificationURL') or "http://localhost:6001/verification/"
account_URL = environ.get('accountURL') or "http://localhost:6003/account/"
payment_URL = environ.get('paymentURL') or "http://localhost:6203/payment/"
loyalty_URL = environ.get('loyaltyURL') or "http://localhost:6301/loyalty/"
promo_URL = environ.get('promoURL') or "http://localhost:6204/promo/"
queue_URL = environ.get('queueURL') or "http://localhost:6202/queueticket/"
redemption_URL = environ.get('redemptionURL') or "http://localhost:6304/redemption_URL/"

# is verification needed here?
@app.get('/order/retrieve_account/<int:account_id>')
def verify_account(account_id):
    url = verification_URL + "account/" + str(account_id)
    account_status = invoke_http(url, method='GET')
    if account_status["code"] == 200:
        return account_status
    else:
        abort(404)

async def confirm_order(account_id):
    # logic for confirmation
    # if person presses "express ticket button",
    # return this True, if not nothing will happen
    express_button = request.form.get('button_pressed', False)
    if express_button:
        return True
    else:
        await asyncio.sleep(1)

@app.route('/order/get_payment_method/<int:account_id>', methods=['POST'])
async def select_payment_method(account_id):
    # buttons to allow user to input what payment method they want to use
    # data = await request.get_json()
    # payment_method = data['payment_method']
    account_id = str(account_id)
    payment_method = request.form.get('payment_method')
    # payment_method = "external" # temporary 
    data = {
        "account_id": account_id,
        "payment_method": payment_method
    } 
    p_method = data["payment_method"]
    if (p_method == "external"):
        return jsonify({"redirect_url": payment_URL})
    elif (p_method == "promo"):
        return jsonify({"redirect_url": promo_URL})
    else:
        return jsonify({"redirect_url": redemption_URL})

@app.post("/order")
def post_order():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            orderRequest = request.get_json()
            print("\nReceived an order in JSON:", orderRequest)

            # do the actual work
            result = place_order(orderRequest)
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "order.py internal error: " + ex_str
            }), 500

    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

# def place_order(orderRequest):
    

@app.patch("/order/<int:account_id>/paid")
def update_order(account_id):
    # this function is being invoked by post queue ticket
    # needs call/message/code from simple microservice to indicate its paid x
    # call amqp to update that queue ticket is paid 
    # gives queue id from queue ticket 
    # updates is_express to true x
    # invoke post in a separate function 
    if (not request.is_json):
        return jsonify({
            "code": 404,
            "message": "Invalid JSON input: " + str(request.get_data())
        }), 404
    
    data = request.get_json()
    print(data)

    update_account = invoke_http(
        account_URL + str(account_id), method='PATCH', json=data)
    
    if update_account["code"] == 200:

        account_result = invoke_http(
            verification_URL + "account/" + str(data["account_id"]), method='GET')

        notification_message = {
            "type": "queueticket",
            "account_id": data["account_id"],
            "first_name": account_result["data"]["first_name"],
            "phone_number": account_result["data"]["phone"],
            "payment_method": data["payment_method"],
            "queue_id": data["queue_id"],
            "message": "You have successfully created a queueticket."
        }
        message = json.dumps(notification_message)
        # generateTicket.generate_queue_tickets(data, message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notification.sms",
                                        body=message, properties=pika.BasicProperties(delivery_mode=2))


        return jsonify({
            "code": 200,
            "message": "Account updated successfully (is express)"
        }), 200
    else:
        return jsonify({
            "code": 405,
            "message": "Order not updated",
            "invoking": update_account["message"],
        }), 405



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6201, debug=True)