from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
import sys
import os

from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

verification_URL = environ.get('verificationURL') or "http://localhost:6001/verification/"
payment_URL = environ.get('paymentURL') or "http://localhost:6203/payment/"
loyalty_URL = environ.get('loyaltyURL') or "http://localhost:6301/loyalty/"
promo_URL = environ.get('promoURL') or "http://localhost:6204/promo/"



@app.post("/order")
def get_order():
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

def place_order(orderRequest):
    


if __name__ == '__main__':
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host='0.0.0.0', port=6201, debug=True)