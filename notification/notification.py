from flask import Flask, request, jsonify
from flask_cors import CORS
from os import environ

from notificationapi_python_server_sdk import (notificationapi)

app = Flask(__name__)

CORS(app)


@app.route("/notification", methods=['POST'])
def send_notification():
    data = request.get_json()

    print(data["first_name"])

    try:
        # init
        notificationapi.init("4520cecngqlnq5guo9dbe26dte",
                             "1d1pfufn15hbv31ibs36458t92319pis5lllihcho22b94jai0na")

        # send
        notificationapi.send({
          "notificationId": "esdeezknee", 
          "user": {
            "id": data["account_id"],
            "email": data["email"],   # required for email notifications
            "number": data["number"]    # required for SMS/Call
          }, 
          "mergeTags": {"firstName": data["first_name"]}
        })

    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred during sending of notification."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": "Notification successfully sent!"
        }
    ), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6002, debug=True)
