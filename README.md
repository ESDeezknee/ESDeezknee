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
![User Scenario 1 Diagram-Scenario 1A](https://user-images.githubusercontent.com/73370403/230117241-863a7f2e-cb85-4640-b02e-867058ed665a.jpg)
![User Scenario 1 Diagram-Scenario 1B](https://user-images.githubusercontent.com/73370403/230117266-59599d1c-09cb-4711-a718-1237ee1fc079.jpg)
![User Scenario 1 Diagram-Scenario 1C](https://user-images.githubusercontent.com/73370403/230117288-858d05ad-d4f0-488f-9c4f-1c2a3708a5c8.jpg)




<hr>
### Customer Finding People to Enter a Ride

![User Scenario 2 Interaction Diagram-Scenario 2A](https://user-images.githubusercontent.com/73370403/230115365-344aaf23-16be-49a9-8522-86b9c2afac77.jpg)
This Scenario shows the Visitor creating a group and thereafter creates a Broadcast Message that everyone is able to view.
![User Scenario 2 Interaction Diagram-Scenario 2B](https://user-images.githubusercontent.com/73370403/230115396-2860ec48-1d95-4d52-8bcf-8d1e5dc12fff.jpg)
This Scenario shows the Visitor creating a group and then joins an already Broadcasted Message.
<hr>

### Customer Wishes to Jump Queue
![User Scenario 3 Diagram-Scenario 3A](https://user-images.githubusercontent.com/73370403/230115430-dcc3791c-7c3f-4b1b-af4e-4a1abad66c7e.jpg)
![User Scenario 3 Diagram-Scenario 3B](https://user-images.githubusercontent.com/73370403/230115446-1624b2d1-e225-4889-8daf-0e11037c223b.jpg)
![User Scenario 3 Diagram-Scenario 3C](https://user-images.githubusercontent.com/73370403/230115455-cac5c1b6-3622-46c6-b276-86f6b36b4147.jpg)
<hr>
<hr>
