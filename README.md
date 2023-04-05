# ESDeezknee

Theme Park Application

## Requirements

- Docker v4.17.0

## Project Setup

### Running Backend
To run the project in development environment, access the parent folder directory and run docker compose

```sh
cd ESDeezknee
docker-compose up
```
*Frontend will also be containerised*



## Microservices

- Verification: [http://localhost:6001](http://localhost:6001)
- Notification: [http://localhost:6002](http://localhost:6002)
- Account: [http://localhost:6003](http://localhost:6003)
- Icebreaker: [http://localhost:6101](http://localhost:6101)
- Broadcast: [http://localhost:6102](http://localhost:6102)
- Group: [http://localhost:6103](http://localhost:6103)
- HandleGroup: [http://localhost:6104](http://localhost:6104)
- Order: [http://localhost:6201](http://localhost:6201)
- QueueTicket: [http://localhost:6202](http://localhost:6202)
- Payment: [http://localhost:6203](http://localhost:6203)
- Promo: [http://localhost:6204](http://localhost:6204)
- Mission: [http://localhost:6300](http://localhost:6300)
- Loyalty: [http://localhost:6301](http://localhost:6301)
- Challenge: [http://localhost:6302](http://localhost:6302)
- Reward: [http://localhost:6303](http://localhost:6303)
- Redemption: [http://localhost:6304](http://localhost:6304)

## External Microservices

- Stripe
- NotificationsAPI

## phpMyAdmin

- Server Name: mysql-database
- Username: root
- Password: root

## User Scenarios

### Customer Finding People to Enter a Ride
![User Scenario 1 Interaction Diagram-Scenario 1A (1)](https://user-images.githubusercontent.com/73370403/230024888-214b7369-0c42-47ad-a592-4a2c06007574.jpg)
This Scenario shows the Visitor creating a group and thereafter creates a Broadcast Message that everyone is able to view.
![User Scenario 1 Interaction Diagram-Scenario 1B](https://user-images.githubusercontent.com/73370403/230024931-458b7b0f-27b5-44e7-ac00-f296482f8564.jpg)
This Scenario shows the Visitor creating a group and then joins an already Broadcasted Message.
<hr>

### Customer Wishes to Jump Queue



<hr>
### Customer Participates in Challenges
![User Scenario 3 Diagram-Scenario 3A](https://user-images.githubusercontent.com/73370403/230024553-a3ca8f31-94aa-41a9-930d-8b1dbfe84a8c.jpg)
![User Scenario 3 Diagram-Scenario 3B](https://user-images.githubusercontent.com/73370403/230024617-df74c9a9-29dd-46ff-a003-b1fa013b0cd7.jpg)
![User Scenario 3 Diagram-Scenario 3C](https://user-images.githubusercontent.com/73370403/230024676-5a10ba4f-9ab7-483a-88b8-74340891dc18.jpg)

<hr>
<hr>
