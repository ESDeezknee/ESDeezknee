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

    send_notification_challenge_complete_sms(data["mission_name"],
        data["first_name"], data["phone_number"], data["award_points"])


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
            "number": phone_number,   # required for email notifications
        },
        "mergeTags": {"firstName": first_name, "missionName": mission_name, "awardPoints": award_points}
    })

    print("SMS successfully sent!", flush=True)


if __name__ == '__main__':
    receiveNotificationLog()
