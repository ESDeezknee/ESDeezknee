import json
import pika
import amqp_setup

from notificationapi_python_server_sdk import (notificationapi)

monitorBindingKey = '#'


def receiveNotificationLog():
    amqp_setup.check_setup()

    email_queue_name = 'Email'
    sms_queue_name = 'SMS'

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(
        queue=email_queue_name, on_message_callback=email_callback, auto_ack=True)
    amqp_setup.channel.basic_consume(
        queue=sms_queue_name, on_message_callback=sms_callback, auto_ack=True)
    # an implicit loop waiting to receive messages;
    amqp_setup.channel.start_consuming()
    # it doesn't exit by default. Use Ctrl+C in the command window to terminate it.


# required signature for the callback; no return
def email_callback(channel, method, properties, body):
    print("This is notification.py...", flush=True)
    print("Received email message:", json.loads(body), flush=True)

    data = json.loads(body)

    send_notification_email(data["first_name"], data["email"])


def sms_callback(channel, method, properties, body):
    print("This is notification.py...", flush=True)
    print("Received sms message:", json.loads(body), flush=True)

    data = json.loads(body)

    if data["type"] == "completion":
      send_notification_challenge_complete_sms(data["mission_name"],
          data["first_name"], data["phone_number"], data["award_points"])

    if data["type"] == "redeem":
      send_notification_redemption_redeem_sms(data["reward_name"],
          data["first_name"], data["phone_number"], data["redemption_code"])
      
    if data["type"] == "inform":
        send_notification_handleGroup_sms(data["number_pax"],data["first_name"],data["phone_number"])
    
    if data["type"] == "queueticket":
        send_notification_queueTicket_sms(data["account_id"],data["queue_id"],data["payment_method"],data["phone_number"])

    if data["type"] == "promo":
        send_notification_promo_sms(data["account_id"],data["promo_code"],data["first_name"],data["phone_number"])



def send_notification_email(first_name, email):
    # init
    notificationapi.init("4520cecngqlnq5guo9dbe26dte",
                         "1d1pfufn15hbv31ibs36458t92319pis5lllihcho22b94jai0na")
    # send email
    notificationapi.send({
        "notificationId": "email",
        "templateId": "default",
        "user": {
            "id": email,
            "email": email,   # required for email notifications
        },
        "mergeTags": {"firstName": first_name}
    })

    print("Email successfully sent!", flush=True)


def send_notification_challenge_complete_sms(mission_name, first_name, phone_number, award_points):
    # init
    notificationapi.init("4520cecngqlnq5guo9dbe26dte",
                         "1d1pfufn15hbv31ibs36458t92319pis5lllihcho22b94jai0na")
    # send sms
    notificationapi.send({
        "notificationId": "sms",
        "templateId": "default",
        "user": {
            "id": phone_number,
            "number": phone_number,   # required for sms notifications
        },
        "mergeTags": {"firstName": first_name, "missionName": mission_name, "awardPoints": award_points}
    })

    print("Challenge Completion SMS successfully sent!", flush=True)


def send_notification_redemption_redeem_sms(reward_name, first_name, phone_number, redemption_code):
    # init
    notificationapi.init("4520cecngqlnq5guo9dbe26dte",
                         "1d1pfufn15hbv31ibs36458t92319pis5lllihcho22b94jai0na")
    # send sms
    notificationapi.send({
        "notificationId": "sms",
        "templateId": "6d251e1d-2e4e-45fc-b5d6-dc5f4630fd8a",
        "user": {
            "id": phone_number,
            "number": phone_number,   # required for sms notifications
        },
        "mergeTags": {"firstName": first_name, "rewardName": reward_name, "redemptionCode": redemption_code}
    })

    print("Challenge Completion SMS successfully sent!", flush=True)

def send_notification_handleGroup_sms(number_pax, first_name,phone_number):
    notificationapi.init("f130gmogsmq75oiffj86pj22o",
                         "1m9bajhvi84ssqo49hd97srlg6huer14f2ii7mp1l986tjc74rgv")
    # send sms
    notificationapi.send({
        "notificationId": "inform_full_group",
        "templateId": "default",
        "user": {
            "id": phone_number,
            "number": phone_number,   # required for sms notifications
        },
        "mergeTags": {"firstName": first_name, "numberPax": number_pax}
    })
    print("Notification SMS about full group successfully sent!", flush=True)

def send_notification_queueTicket_sms(account_id, queue_id, payment_method, phone_number):
    notificationapi.init("2asi8se1f8laqltb8fgh9lhmod", 
                        "1288s1b3fiu8aupu7e97qnc34rvh52fejpapfbqiuv6qokhn7esh")
    # send sms
    notificationapi.send({
        "notificationId": "queueticket",
        "templateId": "default",
        "user": {
            "id": phone_number,
            "number": phone_number,   # required for sms notifications
        },
        "mergeTags": {"account_id": account_id, "queue_id": queue_id, "paymentMethod": payment_method}
    })
    print("Notification SMS about queue ticket successfully sent!", flush=True)

def send_notification_promo_sms(account_id, promo_code, first_name, phone_number):
    notificationapi.init('2asi8se1f8laqltb8fgh9lhmod', 
                        '1288s1b3fiu8aupu7e97qnc34rvh52fejpapfbqiuv6qokhn7esh')
    # send sms
    notificationapi.send({
        "notificationId": "promo",
        "templateId": "default",
        "user": {
            "id": phone_number,
            "number": phone_number,   # required for sms notifications
        },
        "mergeTags": {"account_id": account_id, "first_name": first_name,"promo_code": promo_code}
    })
    print("Notification SMS about promo successfully sent!", flush=True)



if __name__ == '__main__':
    receiveNotificationLog()
