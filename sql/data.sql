USE `account`;

INSERT INTO `account` (`account_id`, `first_name`, `last_name`, `date_of_birth`, `age`, `gender`, `email`, `phone`, `is_express`, `is_active`, `created`) VALUES
(1, 'John', 'Doe', '2000-01-01', 23, 'M', 'john.doe@mail.com', '98765432', 0, 1, '2023-01-01 18:00:00');
INSERT INTO `account` (`account_id`, `first_name`, `last_name`, `date_of_birth`, `age`, `gender`, `email`, `phone`, `is_express`, `is_active`, `created`) VALUES
(2, 'Jason', 'Smith', '1999-01-01', 24, 'M', 'jason.smith@mail.com', '91234567', 1, 1, '2023-01-01 18:00:00');
INSERT INTO `account` (`account_id`, `first_name`, `last_name`, `date_of_birth`, `age`, `gender`, `email`, `phone`, `is_express`, `is_active`, `created`) VALUES
(3, 'Jane', 'White', '2001-01-01', 22, 'F', 'jane.white@mail.com', '90123456', 0, 1, '2023-01-01 18:00:00');

USE `loyalty`;


INSERT INTO `loyalty` (`account_id`, `available_points`, `redeem_points`, `total_points`) VALUES
(1, 1000, 0, 1000);
INSERT INTO `loyalty` (`account_id`, `available_points`, `redeem_points`, `total_points`) VALUES
(2, 500, 0, 500);
INSERT INTO `loyalty` (`account_id`, `available_points`, `redeem_points`, `total_points`) VALUES
(3, 100, 0, 100);

USE `mission`;


INSERT INTO `mission` (`mission_id`, `name`, `description`, `difficulty`, `duration`, `award_points`, `is_active`, `created`, `modified`) VALUES
(1, 'Are you afraid of the mummy?', 'Ride Revenge of the Mummy 5 times to gain 500 points!', 'Medium', 5.0, 500, 1, '2023-01-01 18:00:00', '2023-01-01 18:00:00');
INSERT INTO `mission` (`mission_id`, `name`, `description`, `difficulty`, `duration`, `award_points`, `is_active`, `created`, `modified`) VALUES
(2, 'Get wet at Jurassic Park Rapids Adventure!', 'Ride Jurassic Park Rapids Adventure 10 times to gain 1000 points!', 'Easy', 5.0, 1000, 1, '2023-01-01 18:00:00', '2023-01-01 18:00:00');
INSERT INTO `mission` (`mission_id`, `name`, `description`, `difficulty`, `duration`, `award_points`, `is_active`, `created`, `modified`) VALUES
(3, 'Go on an adventure with Puss in Boots!', 'Ride Puss in Boots Journey 3 times to gain 100 points!', 'Easy', 2.0, 100, 1, '2023-01-01 18:00:00', '2023-01-01 18:00:00');

USE `reward`;


INSERT INTO `reward` (`reward_id`, `name`, `description`, `quantity`, `exchange_points`, `image_url`, `is_active`, `created`, `modified`) VALUES
(1, 'Singapore Flyer Admission Ticket', 'Exchange 200 points to redeem a pair of Singapore Flyer Admission Tickets!', 2, 200, null, 1, '2023-01-01 18:00:00', '2023-01-01 18:00:00');
INSERT INTO `reward` (`reward_id`, `name`, `description`, `quantity`, `exchange_points`, `image_url`, `is_active`, `created`, `modified`) VALUES
(2, 'Gardens By The Bay Admission Ticket', 'Exchange 1000 points to redeem a pair of Gardens By The Bay Admission Tickets!', 2, 1000, null, 1, '2023-01-01 18:00:00', '2023-01-01 18:00:00');