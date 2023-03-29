from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os, sys
from os import environ

from invokes import invoke_http
import requests
import json
# import pika
# import amqp_setup

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

verification_URL = environ.get('verificationURL') or "http://localhost:6001/verification/"
payment_URL = environ.get('paymentURL') or "http://localhost:6203/payment/"
loyalty_URL = environ.get('loyaltyURL') or "http://localhost:6301/loyalty/"
promo_URL = environ.get('promoURL') or "http://localhost:6204/promo/"

# @app.route("/generateTicket", methods=['POST'])
# def generateTicket():

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6202, debug=True)
