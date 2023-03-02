CREATE DATABASE IF NOT EXISTS `account` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `account`;
CREATE DATABASE IF NOT EXISTS `mission` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `mission`;
CREATE DATABASE IF NOT EXISTS `loyalty` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `loyalty`;
CREATE DATABASE IF NOT EXISTS `challenge` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `challenge`;

INSERT INTO `account` (`account_id`, `first_name`, `last_name`, `date_of_birth`, `age`, `gender`, `email`, `phone`, `is_express`, `is_active`, `created`) VALUES
(1, 'John', 'Doe', '2000-01-01', 23, 'M', 'john.doe@mail.com', '98765432', 0, 1, '2023-02-24 18:00:00');