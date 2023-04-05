```
    ___________ ____                  __ __
   / ____/ ___// __ \___  ___  ____  / //_/____  ___  ___
  / __/  \__ \/ / / / _ \/ _ \/_  / / ,<  / __ \/ _ \/ _ \
 / /___ ___/ / /_/ /  __/  __/ / /_/ /| |/ / / /  __/  __/
/_____//____/_____/\___/\___/ /___/_/ |_/_/ /_/\___/\___/

```

# ESDeezknee

ESDeezKnee is a thrilling and immersive theme park that offers a range of exciting rides and attractions. From adrenaline-pumping roller coasters to family-friendly experiences, ESDeezKnee has something for everyone, including ways to jump queues, find new group mates, and participate in fun challenges and get rewarded!

## Requirements

- Docker v4.17.0

## Project Setup

The application has been dockerised to include MySQL, phpMyAdmin, Kong API Gateway, RabbitMQ, Frontend application and the Microservices to provide seamless set up with Docker Compose.

To run the project in development environment, access the parent folder directory and run docker compose

```sh
cd ESDeezknee
docker-compose up
```

## MySQL + phpMyAdmin

To access

- Server Name: mysql-database
- Username: root
- Password: root

## Kong API Gateway (Konga)

## Microservices

- Verification: [http://127.0.0.1:6001](http://127.0.0.1:6001)
- Notification: [http://127.0.0.1:6002](http://127.0.0.1:6002)
- Account: [http://127.0.0.1:6003](http://127.0.0.1:6003)
- Icebreaker: [http://127.0.0.1:6101](http://127.0.0.1:6101)
- Broadcast: [http://127.0.0.1:6102](http://127.0.0.1:6102)
- Group: [http://127.0.0.1:6103](http://127.0.0.1:6103)
- HandleGroup: [http://127.0.0.1:6104](http://127.0.0.1:6104)
- Order: [http://127.0.0.1:6201](http://127.0.0.1:6201)
- QueueTicket: [http://127.0.0.1:6202](http://127.0.0.1:6202)
- Payment: [http://127.0.0.1:6203](http://127.0.0.1:6203)
- Promo: [http://127.0.0.1:6204](http://127.0.0.1:6204)
- Mission: [http://127.0.0.1:6300](http://127.0.0.1:6300)
- Loyalty: [http://127.0.0.1:6301](http://127.0.0.1:6301)
- Challenge: [http://127.0.0.1:6302](http://127.0.0.1:6302)
- Reward: [http://127.0.0.1:6303](http://127.0.0.1:6303)
- Redemption: [http://127.0.0.1:6304](http://127.0.0.1:6304)

## External Microservices

- Stripe
- NotificationsAPI

## User Scenarios (Diagrams)

### Scenario 1 - Customer Participates in Challenges

<img src="https://user-images.githubusercontent.com/73370403/230126026-079c6d4d-2bdf-4a3a-a55a-1a338ea99f99.jpg" alt="User Scenario 1 Diagram-Scenario 1A"  width="60%">

<img src="https://user-images.githubusercontent.com/73370403/230126006-527edcea-9e7d-495d-9849-c308b558ae73.jpg" alt="User Scenario 1 Diagram-Scenario 1B"  width="60%">

<img src="https://user-images.githubusercontent.com/73370403/230125997-472d6cda-b3ba-45f0-aa80-80c8101574da.jpg" alt="User Scenario 1 Diagram-Scenario 1C"  width="60%">

<hr>

### Scenario 2 - Customer Finding People to Enter a Ride

<img src="https://user-images.githubusercontent.com/93701568/230126466-2f36ce8b-c263-49da-992e-1590630c8085.jpg" alt="User Scenario 2 Interaction Diagram-Scenario 2A"  width="60%">

This Scenario shows the Visitor creating a group and thereafter creates a Broadcast Message that everyone is able to view.

<img src="https://user-images.githubusercontent.com/93701568/230126777-c92f0c74-2588-4d78-9557-d650d2018f99.jpg" alt="User Scenario 2 Interaction Diagram-Scenario 2B"  width="60%">

This Scenario shows the Visitor creating a group and then joins an already Broadcasted Message.

<hr>

### Customer Wishes to Jump Queue

<img src="https://user-images.githubusercontent.com/90820000/230129315-15035d12-63dd-4fb1-b299-de90687c9887.jpg" alt="User Scenario 3 Diagram-Scenario 3A"  width="60%">

<img src="https://user-images.githubusercontent.com/90820000/230129379-d469fe57-bcb3-4f81-b64f-69c01bb2ab45.png" alt="User Scenario 3 Diagram-Scenario 3B"  width="60%">

<img src="https://user-images.githubusercontent.com/90820000/230129444-3a10fe92-a775-41f1-b98a-c80673051127.png" alt="User Scenario 3 Diagram-Scenario 3C"  width="60%">

<hr>
<hr>
