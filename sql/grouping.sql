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
-- Database: `grouping`
--
CREATE DATABASE IF NOT EXISTS `grouping` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `grouping`;

-- --------------------------------------------------------

--
-- Table structure for table `grouping`
--

DROP TABLE IF EXISTS `grouping`;
CREATE TABLE IF NOT EXISTS `grouping` (
    `grouping_id` int(11) NOT NULL AUTO_INCREMENT,
    `list_account` JSON NOT NULL,
    `no_of_pax` int(2) NOT NULL,
    `description` varchar(256) NOT NULL,
    `status` varchar(256) NOT NULL,
    PRIMARY KEY (`grouping_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;




-- --------------------------------------------------------

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;