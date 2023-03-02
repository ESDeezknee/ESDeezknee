-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Feb 24, 2023 at 17:21 PM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `queueTicket`
--
CREATE DATABASE IF NOT EXISTS `queueTicket` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `queueTicket`;

-- --------------------------------------------------------

--
-- Table structure for table `queueTicket`
--

DROP TABLE IF EXISTS `queueTicket`;
CREATE TABLE IF NOT EXISTS `queueTicket` (
  `queue_id` int(11) NOT NULL AUTO_INCREMENT,
  `is_express` smallint(1) NOT NULL,
  `ride_times` int(11) NOT NULL DEFAULT '0',
  `queue_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(`account_id`) REFERENCES account(`account_id`),
  PRIMARY KEY (`queue_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `queueTicket`
--

INSERT INTO `queueTicket` (`queue_id`, `is_express`, `ride_times`, `queue_created`, `account_id`) VALUES
(1, '1', '2', '2023-02-24 18:00:00', '1');

-- --------------------------------------------------------

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
