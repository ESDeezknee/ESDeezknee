```
    ___________ ____                  __ __               
   / ____/ ___// __ \___  ___  ____  / //_/____  ___  ___ 
  / __/  \__ \/ / / / _ \/ _ \/_  / / ,<  / __ \/ _ \/ _ \
 / /___ ___/ / /_/ /  __/  __/ / /_/ /| |/ / / /  __/  __/
/_____//____/_____/\___/\___/ /___/_/ |_/_/ /_/\___/\___/ 
                                                         
```
                                                                                 
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

## User Scenarios (Diagrams)


### Customer Participates in Challenges
![User Scenario 1 Diagram-Scenario 1A](https://user-images.githubusercontent.com/73370403/230126026-079c6d4d-2bdf-4a3a-a55a-1a338ea99f99.jpg)
![User Scenario 1 Diagram-Scenario 1B](https://user-images.githubusercontent.com/73370403/230126006-527edcea-9e7d-495d-9849-c308b558ae73.jpg)
![User Scenario 1 Diagram-Scenario 1C](https://user-images.githubusercontent.com/73370403/230125997-472d6cda-b3ba-45f0-aa80-80c8101574da.jpg)





<hr>

### Customer Finding People to Enter a Ride

![User Scenario 2 Interaction Diagram-Scenario 2A](https://user-images.githubusercontent.com/93701568/230126466-2f36ce8b-c263-49da-992e-1590630c8085.jpg)
This Scenario shows the Visitor creating a group and thereafter creates a Broadcast Message that everyone is able to view.
![User Scenario 2 Interaction Diagram-Scenario 2B (1)](https://user-images.githubusercontent.com/93701568/230126777-c92f0c74-2588-4d78-9557-d650d2018f99.jpg)
This Scenario shows the Visitor creating a group and then joins an already Broadcasted Message.
<hr>

### Customer Wishes to Jump Queue
![User Scenario 3 Diagram-Scenario 3A](https://user-images.githubusercontent.com/90820000/230129315-15035d12-63dd-4fb1-b299-de90687c9887.jpg)
![User Scenario 3 Diagram-Scenario 3B](https://user-images.githubusercontent.com/90820000/230129379-d469fe57-bcb3-4f81-b64f-69c01bb2ab45.png)
![User Scenario 3 Diagram-Scenario 3C](https://user-images.githubusercontent.com/90820000/230129444-3a10fe92-a775-41f1-b98a-c80673051127.png)
<hr>
<hr>
