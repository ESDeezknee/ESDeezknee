```
    ___________ ____                  __ __
   / ____/ ___// __ \___  ___  ____  / //_/____  ___  ___
  / __/  \__ \/ / / / _ \/ _ \/_  / / ,<  / __ \/ _ \/ _ \
 / /___ ___/ / /_/ /  __/  __/ / /_/ /| |/ / / /  __/  __/
/_____//____/_____/\___/\___/ /___/_/ |_/_/ /_/\___/\___/

```

# ESDeezknee

ESDeezKnee is a thrilling and immersive theme park that offers a range of exciting rides and attractions. From adrenaline-pumping roller coasters to family-friendly experiences, ESDeezKnee has something for everyone, including ways to jump queues, find new group mates, and participate in fun challenges and get rewarded!

## Problem Statement

Enhancing visitors' experiences by reducing the pains that visitors undergo in theme parks through providing a convenient and seamless solution.

## Team Members

- [Ng Kang Ting](https://www.linkedin.com/in/ngkangting/)
- [Teo Wei Lun](https://www.linkedin.com/in/weilunteo/)
- [Keith Law](https://www.linkedin.com/in/keithlawzk/)
- [Joel Tan](https://www.linkedin.com/in/joeltanec/)
- [Zachary Lian](https://www.linkedin.com/in/zacharylian/)
- [Vanessa Lee](https://www.linkedin.com/in/vanessaleexn/)

## Application Preview

![Application](https://user-images.githubusercontent.com/45414933/230269633-7ec3527b-85c3-4d05-822e-bc74c6fdbf35.gif)

## Requirements

- Docker v4.17.0

## Project Setup

The application has been dockerised to include MySQL, phpMyAdmin, RabbitMQ, Kong API Gateway, Frontend application and the Microservices to provide seamless set up with Docker Compose.

To run the project in development environment, access the parent folder directory and run docker compose.

```sh
cd ESDeezknee
docker-compose up
```

The application will take a few minutes to get everything set up. If the application is not working as expected, stop the terminal and run docker compose again.

```sh
docker-compose up
```

## MySQL + phpMyAdmin

To view and access the database, go to [http://127.0.0.1:5013](http://127.0.0.1:5013) and enter the following credentials.

- Server Name: mysql-database
- Username: root
- Password: root

## RabbitMQ

To view and access RabbitMQ, go to [http://127.0.0.1:15672](http://127.0.0.1:15672) and enter the following credentials.

- Username: guest
- Password: guest

## Kong API Gateway

To view and access Kong API Gateway, go to [http://127.0.0.1:1337](http://127.0.0.1:1337) and enter the following credentials.

- Username: admin
- Password: adminadmin

## Frontend Application

To view the frontend application, go to [http://127.0.0.1:5173](http://127.0.0.1:5173).

## Microservices

The following are the addresses for the microservices. The respective API endspoint can be found in the Postman Collection.

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

- [Stripe](https://stripe.com/docs/api)
- [NotificationsAPI](https://docs.notificationapi.com/)

## Postman Environment + Collections

To test the API endpoints of the microservices, import the following to Postman.

- [ESDeezknee Environment](/ESDeezknee.postman_environment.json)
- [ESDeezknee Collection](/ESDeezknee.postman_collection.json)
- [ESDeezknee API Gateway Collection](/ESDeezkneeAPIGateway.postman_collection.json)

## User Scenarios (Diagrams)

### Scenario 1 - Visitor Participates in Challenges

<img src="https://user-images.githubusercontent.com/73370403/230126026-079c6d4d-2bdf-4a3a-a55a-1a338ea99f99.jpg" alt="User Scenario 1 Diagram-Scenario 1A"  width="75%">

Description: When the visitor comes to the theme park, they can view active missions and participate in a challenge to earn loyalty points.

<img src="https://user-images.githubusercontent.com/73370403/230126006-527edcea-9e7d-495d-9849-c308b558ae73.jpg" alt="User Scenario 1 Diagram-Scenario 1B"  width="75%">

Description: When the visitor completes a challenge, they will then be rewarded with and notifed of additional loyalty points.

<img src="https://user-images.githubusercontent.com/73370403/230125997-472d6cda-b3ba-45f0-aa80-80c8101574da.jpg" alt="User Scenario 1 Diagram-Scenario 1C"  width="75%">

Description: If the visitor decides to redeem their loyalty points, they will be able to view possible rewards available and redeem a reward or redeem it through the purchase of a jump queue ticket.

<hr>

### Scenario 2 - Visitor wants to create a group and search for more Theme-park goers to join his group

<img src="https://user-images.githubusercontent.com/93701568/230126466-2f36ce8b-c263-49da-992e-1590630c8085.jpg" alt="User Scenario 2 Interaction Diagram-Scenario 2A"  width="75%">

Description: This Scenario shows the Visitor creating a group and thereafter creates a Broadcast Message that everyone is able to view.

<img src="https://user-images.githubusercontent.com/93701568/230126777-c92f0c74-2588-4d78-9557-d650d2018f99.jpg" alt="User Scenario 2 Interaction Diagram-Scenario 2B"  width="75%">

Description: This Scenario shows the Visitor creating a group and then joins an already Broadcasted Message.

<hr>

### Scenario 3 - Visitor wants to Purchase a Jump Queue Ticket

<img src="https://user-images.githubusercontent.com/90820000/230129315-15035d12-63dd-4fb1-b299-de90687c9887.jpg" alt="User Scenario 3 Diagram-Scenario 3A"  width="75%">

Description: If the visitor does not want to wait in line for too long, they can opt to purchase a jump queue ticket through three payment methods. Once both loyalty and promo redemption is successful, the user will be notified of it through SMS.

<img src="https://user-images.githubusercontent.com/90820000/230129379-d469fe57-bcb3-4f81-b64f-69c01bb2ab45.png" alt="User Scenario 3 Diagram-Scenario 3B"  width="75%">

Description: Once payment is successful, a new jump queue ticket will be generated and notified to the visitor through SMS and on the UI.

<img src="https://user-images.githubusercontent.com/90820000/230129444-3a10fe92-a775-41f1-b98a-c80673051127.png" alt="User Scenario 3 Diagram-Scenario 3C"  width="75%">

Description: At the point in time before the user enters the ride through queue jumping, the user will redeem their ticket and be notified that the queue ticket is redeemed through SMS and on the UI.

<hr>

## Troubleshooting

### Docker-compose build fails

1. Delete all containers, images and volumes on Docker or Purge/Delete data on Docker
2. Enter the following into your terminal:

```sh
docker-compose build
docker-compose up
```

### Login Error

Please use the following account to navigate through the system:

- Email: kangting.ng.2021@scis.smu.edu.sg
- Password: IS213ESDeezKnee

### MySQL issue when using docker compose

1. On your MAMP/WAMP with your mySQL
2. Ensure that root account password is 'root'
3. Enter the following into your terminal:

```sh
docker-compose -f docker-compose.local.yml build
docker-compose -f docker-compose.local.yml up
```
