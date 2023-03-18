USE `account`;

INSERT INTO `accounts` (`account_id`, `first_name`, `last_name`, `date_of_birth`, `age`, `gender`, `email`, `phone`, `is_express`, `is_active`, `created`) VALUES
(1, 'Benji', 'Ng', '2000-01-01', 23, 'M', 'kangting.ng.2021@scis.smu.edu.sg', '+6597861048', 0, 1, '2023-01-01 18:00:00');
INSERT INTO `accounts` (`account_id`, `first_name`, `last_name`, `date_of_birth`, `age`, `gender`, `email`, `phone`, `is_express`, `is_active`, `created`) VALUES
(2, 'Wei Lun', 'Teo', '1999-01-01', 24, 'F', 'weilun.teo.2021@scis.smu.edu.sg', '+6585339293', 1, 1, '2023-01-01 18:00:00');
INSERT INTO `accounts` (`account_id`, `first_name`, `last_name`, `date_of_birth`, `age`, `gender`, `email`, `phone`, `is_express`, `is_active`, `created`) VALUES
(3, 'Zachary', 'Lian', '2001-01-01', 22, 'M', 'zacharylian.2021@scis.smu.edu.sg', '+6592977881', 0, 1, '2023-01-01 18:00:00');
INSERT INTO `accounts` (`account_id`, `first_name`, `last_name`, `date_of_birth`, `age`, `gender`, `email`, `phone`, `is_express`, `is_active`, `created`) VALUES
(4, 'Joel', 'Tan', '2001-01-01', 22, 'M', 'joel.tan.2021@scis.smu.edu.sg', '+6590605085', 0, 1, '2023-01-01 18:00:00');
INSERT INTO `accounts` (`account_id`, `first_name`, `last_name`, `date_of_birth`, `age`, `gender`, `email`, `phone`, `is_express`, `is_active`, `created`) VALUES
(5, 'Keith', 'Law', '2001-01-01', 22, 'M', 'keith.law.2021@scis.smu.edu.sg', '+6594761445', 0, 1, '2023-01-01 18:00:00');
INSERT INTO `accounts` (`account_id`, `first_name`, `last_name`, `date_of_birth`, `age`, `gender`, `email`, `phone`, `is_express`, `is_active`, `created`) VALUES
(6, 'Vanessa', 'Lee', '2001-01-01', 22, 'F', 'vanessa.lee.2021@scis.smu.edu.sg', '+6597634941', 0, 1, '2023-01-01 18:00:00');

USE `loyalty`;


INSERT INTO `loyaltys` (`account_id`, `available_points`, `redeemed_points`, `total_points`) VALUES
(1, 1000, 0, 1000);
INSERT INTO `loyaltys` (`account_id`, `available_points`, `redeemed_points`, `total_points`) VALUES
(2, 500, 0, 500);
INSERT INTO `loyaltys` (`account_id`, `available_points`, `redeemed_points`, `total_points`) VALUES
(3, 100, 0, 100);

USE `mission`;


INSERT INTO `missions` (`mission_id`, `name`, `description`, `difficulty`, `duration`, `award_points`, `is_active`, `created`, `modified`) VALUES
(1, 'Are you afraid of the mummy?', 'Ride Revenge of the Mummy 5 times to gain 500 points!', 'Medium', 5.0, 500, 1, '2023-01-01 18:00:00', '2023-01-01 18:00:00');
INSERT INTO `missions` (`mission_id`, `name`, `description`, `difficulty`, `duration`, `award_points`, `is_active`, `created`, `modified`) VALUES
(2, 'Get wet at Jurassic Park Rapids Adventure!', 'Ride Jurassic Park Rapids Adventure 10 times to gain 1000 points!', 'Easy', 5.0, 1000, 1, '2023-01-01 18:00:00', '2023-01-01 18:00:00');
INSERT INTO `missions` (`mission_id`, `name`, `description`, `difficulty`, `duration`, `award_points`, `is_active`, `created`, `modified`) VALUES
(3, 'Go on an adventure with Puss in Boots!', 'Ride Puss in Boots Journey 3 times to gain 100 points!', 'Easy', 2.0, 100, 1, '2023-01-01 18:00:00', '2023-01-01 18:00:00');

USE `reward`;


INSERT INTO `rewards` (`reward_id`, `name`, `description`, `quantity`, `exchange_points`, `image_url`, `is_active`, `created`, `modified`) VALUES
(1, 'Singapore Flyer Admission Ticket', 'Exchange 200 points to redeem a pair of Singapore Flyer Admission Tickets!', 2, 200, "https://res.klook.com/images/fl_lossy.progressive,q_65/c_fill,w_1273,h_849/activities/wfkpyhhihrjdztfshifx/SingaporeFlyerTicket.webp", 1, '2023-01-01 18:00:00', '2023-01-01 18:00:00');
INSERT INTO `rewards` (`reward_id`, `name`, `description`, `quantity`, `exchange_points`, `image_url`, `is_active`, `created`, `modified`) VALUES
(2, 'Gardens By The Bay Admission Ticket', 'Exchange 1000 points to redeem a pair of Gardens By The Bay Admission Tickets!', 2, 1000, "https://www.gardensbythebay.com.sg/content/dam/gbb-2021/image/things-to-do/attractions/flower-dome/gallery/flower-dome-05.jpg", 1, '2023-01-01 18:00:00', '2023-01-01 18:00:00');

USE `promo`;


INSERT INTO `promos` (`queue_id`, `account_id`, `promo_code`) VALUES
(1, 1, '123456');
INSERT INTO `promos` (`queue_id`, `account_id`, `promo_code`) VALUES
(2, 2, '123456');

USE `queueticket`;


INSERT INTO `queuetickets` (`queue_id`, `is_express`, `account_id`, `payment_method`) VALUES
(1, 1, 1, 'Promo Code');
INSERT INTO `queuetickets` (`queue_id`, `is_express`, `account_id`, `payment_method`) VALUES
(2, 1, 2, 'Stripe');
INSERT INTO `queuetickets` (`queue_id`, `is_express`, `account_id`, `payment_method`) VALUES
(3, 1, 3, 'Loyalty');