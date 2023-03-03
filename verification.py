from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from invokes import invoke_http

app = Flask(__name__)

CORS(app)

account_URL = "http://localhost:6000/account/"
mission_URL = "http://localhost:6300/mission/"


@app.route("/verification/account/<account_id>")
def verify_account(account_id):
    return invoke_http(
        account_URL + str(account_id), method='GET')

@app.route("/verification/mission/<mission_id>")
def verify_mission(mission_id):
    return invoke_http(
        mission_URL + str(mission_id), method='GET')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001, debug=True)
