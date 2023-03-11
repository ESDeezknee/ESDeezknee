from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

group_URL = "http://127.0.0.1:6103/grouping"
broadcast_URL =  "http://127.0.0.1:6102/broadcast/<group_id>"

@app.route("/handleGroup", methods=["POST"])
def create_group():
    if request.is_json:
        try:
            group = request.get_json()
            print("\nReceived a create group request in JSON:", group)

            result = processCreateGroup(group)
            return jsonify(result), result["code"]

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "handleGroup.py internal error: " + ex_str
            }), 500

    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processCreateGroup(group):
    print('\n-----Invoking create microservice-----')
    createGroup_result = invoke_http(group_URL, method='POST', json=group)
    print('createGroup_result:', createGroup_result)

    code = createGroup_result["code"]
    if code not in range(200,300):
        return {
            "code": 500,
            "data": {"createGroup_result": createGroup_result},
            "message": "New group creation failed."
        }
    
## incl if statement for when users click on "broadcast group" after group creation
def broadcast(): 
    if request.is_json:
        try:
            broadcast_info = request.get_json()
            print("\nReceived a broadcast request in JSON:", broadcast_info)

            result = processCreateBroadcast(broadcast_info)
            return jsonify(result), result["code"]

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "handleGroup.py internal error: " + ex_str
            }), 500

    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processCreateBroadcast(broadcast_info):
    print('\n-----Invoking broadcast microservice-----')
    createBroadcast_result = invoke_http(broadcast_URL, method='POST', json=broadcast_info)
    print('createBroadcast_result:', createBroadcast_result)

    code = createBroadcast_result["code"]
    if code not in range(200,300):
        return {
            "code": 500,
            "data": {"createBroadcast_result": createBroadcast_result},
            "message": "Broadcast failed."
        }

## if a group chooses to join another group on broadcast listing
## compute new LF_pax
## if LF_pax == 0: delete broadcast 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6104, debug=True)