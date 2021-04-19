-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 19, 2021 at 11:31 AM
-- Server version: 10.4.18-MariaDB
-- PHP Version: 8.0.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `facerec_subsub`
--

-- --------------------------------------------------------

--
-- Table structure for table `encoding`
--

CREATE TABLE `encoding` (
  `groupID` int(11) NOT NULL,
  `subgroupID` int(11) NOT NULL,
  `subsubgroupID` int(11) NOT NULL,
  `faceID` int(11) NOT NULL,
  `faceOwner` varchar(50) DEFAULT NULL,
  `encodingBlob` blob DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `groups`
--

CREATE TABLE `groups` (
  `groupID` int(11) NOT NULL,
  `groupName` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `groups`
--

INSERT INTO `groups` (`groupID`, `groupName`) VALUES
(1, 'youtube'),
(2, 'twitch');

-- --------------------------------------------------------

--
-- Table structure for table `subgroups`
--

CREATE TABLE `subgroups` (
  `groupID` int(11) NOT NULL,
  `subgroupID` int(11) NOT NULL,
  `subgroupName` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `subgroups`
--

INSERT INTO `subgroups` (`groupID`, `subgroupID`, `subgroupName`) VALUES
(1, 1, 'channelA'),
(1, 2, 'channelB'),
(1, 3, 'channelC'),
(1, 4, 'channelD');

-- --------------------------------------------------------

--
-- Table structure for table `subsubgroups`
--

CREATE TABLE `subsubgroups` (
  `groupID` int(11) NOT NULL,
  `subgroupID` int(11) NOT NULL,
  `subsubgroupID` int(11) NOT NULL,
  `subsubgroupName` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `subsubgroups`
--

INSERT INTO `subsubgroups` (`groupID`, `subgroupID`, `subsubgroupID`, `subsubgroupName`) VALUES
(1, 1, 1, 'vid1'),
(1, 1, 2, 'vid2'),
(1, 1, 3, 'vid3'),
(1, 1, 4, 'vid4'),
(1, 2, 5, 'vid1'),
(1, 2, 6, 'vid2');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `role` enum('superuser','user') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `role`) VALUES
(1, 'admin', 'superuser'),
(2, 'bukanadmin', 'user');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `encoding`
--
ALTER TABLE `encoding`
  ADD PRIMARY KEY (`faceID`),
  ADD KEY `groupID` (`groupID`),
  ADD KEY `subgroupID` (`subgroupID`),
  ADD KEY `subsubgroupID` (`subsubgroupID`);

--
-- Indexes for table `groups`
--
ALTER TABLE `groups`
  ADD PRIMARY KEY (`groupID`);

--
-- Indexes for table `subgroups`
--
ALTER TABLE `subgroups`
  ADD PRIMARY KEY (`subgroupID`),
  ADD KEY `groupID` (`groupID`);

--
-- Indexes for table `subsubgroups`
--
ALTER TABLE `subsubgroups`
  ADD PRIMARY KEY (`subsubgroupID`),
  ADD KEY `groupID` (`groupID`),
  ADD KEY `subgroupID` (`subgroupID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `encoding`
--
ALTER TABLE `encoding`
  MODIFY `faceID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `groups`
--
ALTER TABLE `groups`
  MODIFY `groupID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `subgroups`
--
ALTER TABLE `subgroups`
  MODIFY `subgroupID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `subsubgroups`
--
ALTER TABLE `subsubgroups`
  MODIFY `subsubgroupID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `encoding`
--
ALTER TABLE `encoding`
  ADD CONSTRAINT `encoding_ibfk_1` FOREIGN KEY (`groupID`) REFERENCES `groups` (`groupID`),
  ADD CONSTRAINT `encoding_ibfk_2` FOREIGN KEY (`subgroupID`) REFERENCES `subgroups` (`subgroupID`),
  ADD CONSTRAINT `encoding_ibfk_3` FOREIGN KEY (`subsubgroupID`) REFERENCES `subsubgroups` (`subsubgroupID`);

--
-- Constraints for table `subgroups`
--
ALTER TABLE `subgroups`
  ADD CONSTRAINT `subgroups_ibfk_1` FOREIGN KEY (`groupID`) REFERENCES `groups` (`groupID`);

--
-- Constraints for table `subsubgroups`
--
ALTER TABLE `subsubgroups`
  ADD CONSTRAINT `subsubgroups_ibfk_1` FOREIGN KEY (`groupID`) REFERENCES `groups` (`groupID`),
  ADD CONSTRAINT `subsubgroups_ibfk_2` FOREIGN KEY (`subgroupID`) REFERENCES `subgroups` (`subgroupID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
