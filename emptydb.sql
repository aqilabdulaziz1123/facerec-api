-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 18, 2021 at 01:06 PM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.2.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `face_recognition`
--

-- --------------------------------------------------------

--
-- Table structure for table `encoding`
--

CREATE TABLE `encoding` (
  `FaceID` int(11) NOT NULL,
  `SubGroupID` int(11) NOT NULL,
  `FaceOwner` char(50) DEFAULT NULL,
  `EncodingBLOB` blob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `groups`
--

CREATE TABLE `groups` (
  `GroupID` int(11) NOT NULL,
  `GroupName` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `pengguna`
--

CREATE TABLE `pengguna` (
  `Id` int(11) NOT NULL,
  `Username` varchar(50) DEFAULT NULL,
  `Role` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `subgroups`
--

CREATE TABLE `subgroups` (
  `SubGroupID` int(11) NOT NULL,
  `GroupID` int(11) NOT NULL,
  `SubGroupName` char(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `userinsubgroup`
--

CREATE TABLE `userinsubgroup` (
  `Id` int(11) NOT NULL,
  `GroupID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `encoding`
--
ALTER TABLE `encoding`
  ADD PRIMARY KEY (`FaceID`),
  ADD KEY `SubGroupID` (`SubGroupID`);

--
-- Indexes for table `groups`
--
ALTER TABLE `groups`
  ADD PRIMARY KEY (`GroupID`);

--
-- Indexes for table `pengguna`
--
ALTER TABLE `pengguna`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `subgroups`
--
ALTER TABLE `subgroups`
  ADD PRIMARY KEY (`SubGroupID`),
  ADD KEY `GroupID` (`GroupID`);

--
-- Indexes for table `userinsubgroup`
--
ALTER TABLE `userinsubgroup`
  ADD KEY `Id` (`Id`),
  ADD KEY `GroupID` (`GroupID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `encoding`
--
ALTER TABLE `encoding`
  ADD CONSTRAINT `encoding_ibfk_1` FOREIGN KEY (`SubGroupID`) REFERENCES `subgroups` (`SubGroupID`);

--
-- Constraints for table `subgroups`
--
ALTER TABLE `subgroups`
  ADD CONSTRAINT `subgroups_ibfk_1` FOREIGN KEY (`GroupID`) REFERENCES `groups` (`GroupID`);

--
-- Constraints for table `userinsubgroup`
--
ALTER TABLE `userinsubgroup`
  ADD CONSTRAINT `userinsubgroup_ibfk_1` FOREIGN KEY (`Id`) REFERENCES `pengguna` (`Id`),
  ADD CONSTRAINT `userinsubgroup_ibfk_2` FOREIGN KEY (`GroupID`) REFERENCES `subgroups` (`SubGroupID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
