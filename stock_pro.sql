-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 11, 2024 at 09:43 AM
-- Server version: 10.1.38-MariaDB
-- PHP Version: 7.1.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `stock_pro`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `username` text NOT NULL,
  `password` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `username`, `password`) VALUES
(1, 'admin', '123');

-- --------------------------------------------------------

--
-- Table structure for table `contact_us`
--

CREATE TABLE `contact_us` (
  `sr_no` int(11) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(64) NOT NULL,
  `mo_num` bigint(13) NOT NULL,
  `message` text NOT NULL,
  `submission_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `contact_us`
--

INSERT INTO `contact_us` (`sr_no`, `name`, `email`, `mo_num`, `message`, `submission_timestamp`) VALUES
(1, 'momin kamil', 'mominkamil_123@gmail.com', 1234567895, 'this website is Faaltu boring ', '2024-03-09 03:45:04'),
(2, 'Dipak Gohel', 'Gohel@gmail.com', 9016407069, 'Sala Loss Hi Hota hai Profit Kab Hoga', '2024-03-09 03:45:04'),
(3, 'jay', 'jayvado@gmail.com', 3625149878, 'this website in the multiple bugs are available, Please fix bugs ', '2024-03-09 03:45:04'),
(4, 'jay', 'jayvado@gmail.com', 9634564715, 'the bugs in the website such as refresh time fields empty', '2024-03-09 03:45:04'),
(5, 'fardin', 'fardinmalek733@gmail.com', 9924059579, 'I want to learn stock market analysis..', '2024-03-09 03:45:04');

-- --------------------------------------------------------

--
-- Table structure for table `login_history`
--

CREATE TABLE `login_history` (
  `id` int(11) NOT NULL,
  `f_name` varchar(255) NOT NULL,
  `l_name` varchar(255) NOT NULL,
  `e_id` varchar(255) NOT NULL,
  `mo_num` varchar(255) NOT NULL,
  `login_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `login_history`
--

INSERT INTO `login_history` (`id`, `f_name`, `l_name`, `e_id`, `mo_num`, `login_time`) VALUES
(1, 'fardin', 'malek', 'cawex50555@comsb.com', '7845715668', '2024-03-09 05:17:57'),
(2, 'kadamb', 'parekh', 'mofaga9544@fashlend.com', '8460298402', '2024-03-09 05:18:40'),
(3, 'fardin', 'malek', 'cawex50555@comsb.com', '7845715668', '2024-03-09 06:15:47'),
(4, 'fardin', 'malek', 'mofaga9544@fashlend.com', '846029458402', '2024-03-09 07:20:23'),
(5, 'fardin', 'malek', 'mofaga9544@fashlend.com', '6111111111', '2024-03-09 11:15:45'),
(6, 'fardin', 'malek', 'mofaga9544@fashlend.com', '6111111111', '2024-03-09 11:15:54'),
(7, 'fardin', 'malek', 'mofaga9544@fashlend.com', '6111111111', '2024-03-09 11:17:15'),
(8, 'vihana', 'shah', 'mofaga9544@fashlend.com', '6111111111', '2024-03-09 11:31:23'),
(9, 'kadamb', 'parekh', 'hakimoy158@mcuma.com', '1236547955', '2024-03-11 05:13:19'),
(10, 'kadamb', 'parekh', 'hakimoy158@mcuma.com', '1236547955', '2024-03-11 06:33:09'),
(11, 'kadamb', 'parekh', 'hakimoy158@mcuma.com', '1236547955', '2024-03-11 06:35:24'),
(12, 'kadamb', 'parekh', 'hakimoy158@mcuma.com', '1236547955', '2024-03-11 06:35:38');

-- --------------------------------------------------------

--
-- Table structure for table `registration`
--

CREATE TABLE `registration` (
  `f_name` varchar(20) NOT NULL,
  `l_name` varchar(20) NOT NULL,
  `e_id` varchar(50) NOT NULL,
  `mo_num` bigint(10) NOT NULL,
  `password` varchar(12) NOT NULL,
  `c_password` varchar(12) NOT NULL,
  `registration_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `registration`
--

INSERT INTO `registration` (`f_name`, `l_name`, `e_id`, `mo_num`, `password`, `c_password`, `registration_timestamp`) VALUES
('kadamb', 'parekh', 'hakimoy158@mcuma.com', 1236547955, 'k1@.', 'k1@.', '2024-03-11 05:06:55'),
('vihana', 'shah', 'mofaga9544@fashlend.com', 6111111111, 'ak47@', 'ak47@', '2024-03-09 03:52:57');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `contact_us`
--
ALTER TABLE `contact_us`
  ADD PRIMARY KEY (`sr_no`);

--
-- Indexes for table `login_history`
--
ALTER TABLE `login_history`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `registration`
--
ALTER TABLE `registration`
  ADD PRIMARY KEY (`e_id`),
  ADD UNIQUE KEY `mo_num` (`mo_num`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contact_us`
--
ALTER TABLE `contact_us`
  MODIFY `sr_no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `login_history`
--
ALTER TABLE `login_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
