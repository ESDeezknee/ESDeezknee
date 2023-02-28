-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Feb 27, 2022 at 19:00 PM
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
-- Database: `loyalty`
--
CREATE DATABASE IF NOT EXISTS `loyalty` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `loyalty`;

-- --------------------------------------------------------

--
-- Table structure for table `loyalty`
--

DROP TABLE IF EXISTS `loyalty`;
CREATE TABLE IF NOT EXISTS `loyalty` (
  `account_id` int(11) NOT NULL,
  `available_points` int(11) NOT NULL,
  `redeem_points` int(11) NOT NULL,
  `total_points` int(11) NOT NULL,
  `expiry` timestamp NOT NULL,
  PRIMARY KEY (`account_id`),
  KEY `FK_account_id` (`account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `loyalty`
--

INSERT INTO `loyalty` (`account_id`, `available_points`, `redeem_points`, `total_points`, `expiry`) VALUES
(1, 100, 0, 100, NULL);

-- --------------------------------------------------------

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
