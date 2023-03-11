import json
import pika
import amqp_setup

from notificationapi_python_server_sdk import (notificationapi)

monitorBindingKey = '#'


def receiveNotificationLog():
    amqp_setup.check_setup()

    queue_name = 'Notification'

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    # an implicit loop waiting to receive messages;
    amqp_setup.channel.start_consuming()
    # it doesn't exit by default. Use Ctrl+C in the command window to terminate it.


# required signature for the callback; no return
def callback(channel, method, properties, body):
    print("This is notification.py...", flush=True)
    print("Received message:", json.loads(body), flush=True)

    data = json.loads(body)

    if data["type"] == "sms":
      send_notification_sms(data["first_name"], data["phone_number"])

    if data["type"] == "email":
      send_notification_email(data["first_name"], data["email"])


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


def send_notification_sms(first_name, phone_number):
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
        "mergeTags": {"firstName": first_name}
    })

    print("SMS successfully sent!", flush=True)


if __name__ == '__main__':
    receiveNotificationLog()
