-- MySQL dump 10.13  Distrib 8.0.18, for Win64 (x86_64)
--
-- Host: localhost    Database: facerec
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.14-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `encoding`
--

DROP TABLE IF EXISTS `encoding`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `encoding` (
  `groupID` int(11) NOT NULL,
  `subgroupID` int(11) NOT NULL,
  `subsubgroupID` int(11) NOT NULL,
  `faceID` int(11) NOT NULL AUTO_INCREMENT,
  `faceOwner` varchar(50) DEFAULT NULL,
  `encodingblob` blob NOT NULL,
  PRIMARY KEY (`faceID`),
  KEY `subgroupID` (`subgroupID`),
  CONSTRAINT `encoding_ibfk_1` FOREIGN KEY (`subgroupID`) REFERENCES `subgroups` (`subgroupID`),
  KEY `groupID` (`groupID`),
  CONSTRAINT `encoding_ibfk_2` FOREIGN KEY (`groupID`) REFERENCES `groups` (`groupID`),
  KEY `subsubgroupID` (`subsubgroupID`),
  CONSTRAINT `encoding_ibfk_3` FOREIGN KEY (`subsubgroupID`) REFERENCES `subsubgroups` (`subsubgroupID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `encoding`
--

LOCK TABLES `encoding` WRITE;
/*!40000 ALTER TABLE `encoding` DISABLE KEYS */;
/*!40000 ALTER TABLE `encoding` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `groups`
--

DROP TABLE IF EXISTS `groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `groups` (
  `groupID` int(11) NOT NULL AUTO_INCREMENT,
  `groupName` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`groupID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `groups`
--

LOCK TABLES `groups` WRITE;
/*!40000 ALTER TABLE `groups` DISABLE KEYS */;
INSERT INTO `groups` VALUES (1,'youtube'),(2,'twitch');
/*!40000 ALTER TABLE `groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `images`
--

DROP TABLE IF EXISTS `images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `images` (
  `id` int(11) DEFAULT NULL,
  `faceOwner` varchar(100) DEFAULT NULL,
  `path` varchar(200) DEFAULT NULL,
  KEY `id` (`id`),
  CONSTRAINT `images_ibfk_1` FOREIGN KEY (`id`) REFERENCES `encoding` (`faceID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `images`
--

LOCK TABLES `images` WRITE;
/*!40000 ALTER TABLE `images` DISABLE KEYS */;
/*!40000 ALTER TABLE `images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subgroups`
--

DROP TABLE IF EXISTS `subgroups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subgroups` (
  `subgroupID` int(11) NOT NULL AUTO_INCREMENT,
  `groupID` int(11) NOT NULL,
  `subgroupName` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`subgroupID`),
  KEY `groupID` (`groupID`),
  CONSTRAINT `subgroups_ibfk_1` FOREIGN KEY (`groupID`) REFERENCES `groups` (`groupID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subgroups`
--

LOCK TABLES `subgroups` WRITE;
/*!40000 ALTER TABLE `subgroups` DISABLE KEYS */;
INSERT INTO `subgroups` VALUES (1,1,'channelA'),(2,1,'channelB'),(3,1,'channelC');
/*!40000 ALTER TABLE `subgroups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `role` enum('superuser','user') DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','superuser'),(2,'bukanadmin','user');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userinsubgroup`
--

DROP TABLE IF EXISTS `userinsubgroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userinsubgroup` (
  `id` int(11) NOT NULL,
  `groupID` int(11) NOT NULL,
  KEY `id` (`id`),
  KEY `groupID` (`groupID`),
  CONSTRAINT `userinsubgroup_ibfk_1` FOREIGN KEY (`id`) REFERENCES `user` (`id`),
  CONSTRAINT `userinsubgroup_ibfk_2` FOREIGN KEY (`groupID`) REFERENCES `subgroups` (`subgroupID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userinsubgroup`
--

LOCK TABLES `userinsubgroup` WRITE;
/*!40000 ALTER TABLE `userinsubgroup` DISABLE KEYS */;
INSERT INTO `userinsubgroup` VALUES (1,1),(1,2),(1,3),(1,4),(2,1),(2,2),(2,3),(2,4);
/*!40000 ALTER TABLE `userinsubgroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subsubgroups`
--

DROP TABLE IF EXISTS `subsubgroups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subsubgroups` (
  `subsubgroupID` int(11) NOT NULL AUTO_INCREMENT,
  `groupID` int(11) NOT NULL,
  `subgroupID` int(11) NOT NULL,
  `subsubgroupName` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`subsubgroupID`),
  KEY `groupID` (`groupID`),
  CONSTRAINT `subsubgroups_ibfk_1` FOREIGN KEY (`groupID`) REFERENCES `groups` (`groupID`),
  KEY `subgroupID` (`subgroupID`),
  CONSTRAINT `subsubgroups_ibfk_2` FOREIGN KEY (`subgroupID`) REFERENCES `subgroups` (`subgroupID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subgroups`
--

LOCK TABLES `subsubgroups` WRITE;
/*!40000 ALTER TABLE `subgroups` DISABLE KEYS */;
INSERT INTO `subsubgroups` VALUES (1,1,1,'vid1'),(2,1,1,'vid2'),(3,1,2,'vid3');
/*!40000 ALTER TABLE `subgroups` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-26 15:37:47
