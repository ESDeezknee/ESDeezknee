from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from os import environ

import requests
from invokes import invoke_http
import amqp_setup
import pika
import json

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

verification_URL = environ.get('verificationURL')
group_URL = "http://grouping:6103/grouping"
broadcast_URL = "http://broadcast:6102/broadcast"
icebreakers_URL = environ.get('icebreakersURL')


@app.route("/handleGroup/create", methods=["POST"])
def create_group():
    if request.is_json:
        try:
            group = request.get_json()
            # print("\nReceived a create group request in JSON:", group)

            result = processCreateGroup(group)
            # return jsonify(result), result["code"]

            # For User Scenario 3, Update Challenge Status
            challenge_message = {
                "mission_id": 1,
                "code": result["code"]
            }

            challenge_message.update(result["data"])
            message = json.dumps(challenge_message)

            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename1, routing_key="challenge.challenge_complete", body=message, properties=pika.BasicProperties(delivery_mode=2))

            return result


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

    
## incl if statement for when users click on "broadcast group" after group creation
@app.route("/handleGroup/broadcast", methods=["POST"])
def broadcast(): 
    if request.is_json:
        try:
            broadcast_info = request.get_json()
            # print("\nReceived a broadcast request in JSON:", broadcast_info)

            result = processCreateBroadcast(broadcast_info)
            return result

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


## if a group chooses to join another group on broadcast listing
## first get all broadcast listing (scenario 1B steps 5, 6)
@app.route("/handleGroup/broadcast_listings")
def getAllBroadcasts():
    all = invoke_http(broadcast_URL, method='GET')

    code = all["code"]
    if code not in range(200,300):
        return {
            "code": 500,
            "data": {"getAllBroadcasts_result": all},
            "message": "Broadcast failed."
        }
    
    else:
        return all

## user from group 2 chooses to join group 1 (scenario 1B step 8)
@app.route("/handleGroup/join_group", methods=["POST"])
def join_group(): 
    ## get no_of_pax of group 2 from grouping service
    ## figure out how to get grouping_id from frontend
    data = request.get_json()
    grouping_id = data["grouping_id"]
    broadcasted_id = data["broadcasted_id"]
    url_for_noofpax = group_URL + "/" + str(grouping_id)
    group_details = invoke_http(url_for_noofpax, method='GET')
    code = group_details["code"]
    if code not in range(200,300):
        return {
            "code": 500,
            "data": {"findNoOfPax_result": group_details},
            "message": "findNoOfPax failed."
        }
    
    else:
        no_of_pax_joining = group_details["data"]["no_of_pax"]

        ## get lf_pax of group 1 from broadcast
        url_for_LFpax = broadcast_URL + "/" + str(broadcasted_id)
        broadcast_details = invoke_http(url_for_LFpax, method='GET')
        
        code = broadcast_details["code"]
        if code not in range(200,300):
            return {
                "code": 500,
                "data": {"findLFPax_result": broadcast_details},
                "message": "findNLFPax failed."
            }
        
        else:
            LF_pax = broadcast_details["data"]["lf_pax"]
            
            ## compute new LF_pax
            new_LF_pax = LF_pax - no_of_pax_joining

            ## case 1: joining group with insufficient space
            if new_LF_pax < 0:
                return jsonify(
                    {
                        "code": 500,
                        "data": {
                            "grouping_id": grouping_id,
                            "message": "Number of pax in your group exceeds limit."
                        }
                    }
                ), 500
            
            ## case 2: perfect match
            elif new_LF_pax == 0:
                    new_no_of_pax = LF_pax + no_of_pax_joining
                    ## get account_id of broadcasted group
                    grouping_details_result = getGroupingDetails(broadcasted_id)
                    code = grouping_details_result["code"]
                    if code not in range(200,300):
                        return jsonify({
                            "code": 500,
                            "data": {"joinGroup_result": grouping_details_result,
                                     "message": "Failed to join group as collection of broadcasted group details failed."}
                            
                    })

                    else: 
                        account_list = grouping_details_result["data"]["list_account"]
                        ## need to get acct id of joining group from frontend
                        joining_group_details = getGroupingDetails(grouping_id)
                        code = joining_group_details["code"]
                        if code not in range(200,300):
                            return jsonify({
                                "code": 500,
                                "data": {"joinGroup_result": joining_group_details,
                                         "message": "Failed to join group as collection of joining group details failed."
                                            }
                            })

                        else: 
                            joining_acct_id = joining_group_details["data"]["list_account"]
                            for acc in joining_acct_id:
                                account_list.append(acc)

                            merged_group_details = {
                                "grouping_id": broadcasted_id,
                                "list_account": account_list,
                                "description": "Complete group!",
                                "no_of_pax": new_no_of_pax,
                                "status": "Complete"
                            }
                            update_group_result = processUpdateGrouping(merged_group_details)
                            code = update_group_result["code"]
                            if code not in range(200,300):
                                return jsonify({
                                    "code": 500,
                                    "data": {"joinGroup_result": update_group_result,
                                             "message": "Failed to join group as group update failed."
                                    }
                            })

                            else: 
                                delete_broadcast_result = processDeleteBroadcast(broadcasted_id)
                                for account in update_group_result["data"]["list_account"]:
                                        account_details = invoke_http(verification_URL + "account/" + str(account), method='GET')
                                        notification_message = {"type":"inform","number_pax":update_group_result["data"]["no_of_pax"],"first_name":account_details["data"]["first_name"], "phone_number":account_details["data"]["phone"]}
                                        message = json.dumps(notification_message)
                                        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notification.sms",
                                                    body=message, properties=pika.BasicProperties(delivery_mode=2))
                                        
                                        icebreaker_details = invoke_http(icebreakers_URL, method="GET")
                                        notification_message_2 = {"type":"icebreakers","icebreakers":icebreaker_details,"first_name":account_details["data"]["first_name"],"phone_number":account_details["data"]["phone"]}

                                        icebreaker_message = json.dumps(notification_message_2)
                                        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notification.sms",
                                                    body=icebreaker_message, properties=pika.BasicProperties(delivery_mode=2))
                                code = delete_broadcast_result["code"]
                                if code not in range (200,300):
                                    return jsonify({
                                        "code": 500,
                                        "data": {"joinGroup_result": delete_broadcast_result,
                                                 "message": "Failed to join group as group deletion failed."
                                                 }
                                    })
                                
                                else: 
                                    ## get group number from frontend
                                    delete_joining_group_result = processDeleteGroup(grouping_id)
                                    code = delete_joining_group_result["code"]
                                    if code not in range (200,300):
                                        return jsonify({
                                            "code": 500,
                                            "data": {"joinGroup_result": delete_joining_group_result,
                                                     "message": "Failed to join group as group deletion failed."
                                            }
                                        })
                                    else:
                                    ## get group number from frontend
                                        grouping_id = str(broadcasted_id)
                                        return jsonify(
                                            {
                                                "code": 200,
                                                "message": "Congratulations! You are now part of Group " + grouping_id
                                            }
                                        ), 200
            
            ## case 3: still need more people 
            elif new_LF_pax > 0:
                new_no_of_pax = LF_pax + no_of_pax_joining
                ## get account_id of broadcasted group, get grouping_id frm frontend
                grouping_details_result = getGroupingDetails(broadcasted_id)
                code = grouping_details_result["code"]
                if code not in range(200,300):
                    return jsonify({
                        "code": 500,
                        "data": {"joinGroup_result": grouping_details_result,
                                 "message": "Failed to join group as collection of broadcasted group details failed."
                        }
                })

                else: 
                    account_list = grouping_details_result["data"]["list_account"]
                    ## need to get acct id of joining group from frontend
                    joining_group_details = getGroupingDetails(grouping_id)
                    code = joining_group_details["code"]
                    if code not in range(200,300):
                        return jsonify({
                            "code": 500,
                            "data": {"joinGroup_result": joining_group_details,
                                     "message": "Failed to join group as collection of joining group details failed."
                            }
                        })

                    else: 
                        joining_acct_id = joining_group_details["data"]["list_account"]
                        account_list.append(joining_acct_id)
                        new_grouping_info = {
                            "grouping_id": broadcasted_id,
                            "list_account": account_list,
                            "no_of_pax": new_no_of_pax,
                            "description": "looking for more members",
                            "status": "In Progress",
                        }
                        updateGrouping_result = processUpdateGrouping(new_grouping_info)
                        code = updateGrouping_result["code"]
                        if code not in range(200,300):
                            return jsonify({
                                "code": 500,
                                "data": {"updateGrouping_result": updateGrouping_result},
                                "message": "Failed to join group as group update failed."
                            }), 500
                        
                        new_broadcast_info = {
                            "grouping_id": broadcasted_id,
                            "lf_pax": new_LF_pax,
                        }
                        updateBroadcast_result = processUpdateBroadcast(new_broadcast_info)
                        code = updateBroadcast_result["code"]
                        if code not in range(200,300):
                                return jsonify({
                                    "code": 500,
                                    "data": {"updateBroadcast_result": updateBroadcast_result,
                                             "message": "Failed to join group as broadcast update failed."
                                            }
                            }), 500
                        else: 
                            delete_joining_group_result = processDeleteGroup(grouping_id)
                            code = delete_joining_group_result["code"]
                            if code not in range (200,300):
                                return jsonify({
                                    "code": 500,
                                    "data": {"joinGroup_result": delete_joining_group_result,
                                             "message": "Failed to join group as group deletion failed."
                                    }
                                })
                            else: 
                                new_LF_pax = str(new_LF_pax)
                                return jsonify(
                                    {
                                        "code": 200,
                                        "message": f"Join group success! You are now part of group {broadcasted_id}. We are in the midst of finding " + new_LF_pax + " more people to complete your group."
                                    }
                                ), 200
                    
def processCreateGroup(group):
    createGroup_result = invoke_http(group_URL, method='POST', json=group)

    code = createGroup_result["code"]
    if code not in range(200,300):
        return {
            "code": 500,
            "data": {"createGroup_result": createGroup_result},
            "message": "New group creation failed."
        }

    else: 
        return createGroup_result        

## need to figure out how to link to frontend to get group_id 
def processCreateBroadcast(broadcast_info):
    url = broadcast_URL + "/" + str(broadcast_info["broadcasted_id"])
    createBroadcast_result = invoke_http(url, method='POST', json=broadcast_info)

    code = createBroadcast_result["code"]
    if code not in range(200,300):
        return {
            "code": 500,
            "data": {"createBroadcast_result": createBroadcast_result},
            "message": "Broadcast failed."
        }
    
    else:
        return createBroadcast_result        
    
def getGroupingDetails(grouping_id):
    url = group_URL + "/" + str(grouping_id)
    groupingDetails_result = invoke_http(url, method="GET", json=grouping_id)
    code = groupingDetails_result["code"]
    if code not in range(200,300):
        return {
            "code": 500,
            "data": {"groupingDetails_result": groupingDetails_result},
            "message": "Failure to join group as broadcast update failed."
        }
    
    else:
        return groupingDetails_result

def processUpdateBroadcast(info):
    url = broadcast_URL + "/" + str(info["grouping_id"])
    updateBroadcast_result = invoke_http(url, method='PATCH', json=info)

    code = updateBroadcast_result["code"]
    if code not in range(200,300):
        return {
            "code": 500,
            "data": {"updateBroadcast_result": updateBroadcast_result},
            "message": "Failure to join group as broadcast update failed."
        }
    
    else:
        return updateBroadcast_result

def processUpdateGrouping(info):
    url = group_URL + "/" + str(info["grouping_id"])
    updateGrouping_result = invoke_http(url, method='PATCH', json=info)

    code = updateGrouping_result["code"]
    if code not in range(200,300):
        return {
            "code": 500,
            "data": {"updateGrouping_result": updateGrouping_result},
            "message": "Failure to join group as group update failed."
        }
    
    else:
        return updateGrouping_result
    
def processDeleteGroup(grouping_id):
    url = group_URL + "/" + str(grouping_id)
    deleteGrouping_result = invoke_http(url, method="DELETE", json=grouping_id)
    code = deleteGrouping_result["code"]
    if code not in range(200,300):
        return {
            "code": 500,
            "data": {"deleteGrouping_result": deleteGrouping_result},
            "message": "Failure to join group as group deletion failed."
        }
    
    else:
        return deleteGrouping_result
    
def processDeleteBroadcast(grouping_id):
    url = broadcast_URL + "/" + str(grouping_id)
    deleteBroadcast_result = invoke_http(url, method="DELETE", json=grouping_id)
    code = deleteBroadcast_result["code"]
    if code not in range(200,300):
        return {
            "code": 500,
            "data": {"deleteBroadcast_result": deleteBroadcast_result},
            "message": "Failure to join group as broadcast deletion failed."
        }
    
    else:
        return deleteBroadcast_result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6104, debug=True)