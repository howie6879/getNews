-- MySQL dump 10.13  Distrib 5.5.49, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: howie
-- ------------------------------------------------------
-- Server version	5.5.49-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `get_news`
--

DROP TABLE IF EXISTS `get_news`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `get_news` (
  `news_id` varchar(20) NOT NULL,
  `news_link` varchar(100) DEFAULT NULL,
  `source` varchar(20) DEFAULT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `title` varchar(50) NOT NULL,
  `abstract` varchar(500) NOT NULL,
  `tag` varchar(20) NOT NULL,
  `text_content` mediumtext NOT NULL,
  `html_content` mediumtext NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `keyword` varchar(100) NOT NULL,
  `is_old` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`news_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `get_news`
--

LOCK TABLES `get_news` WRITE;
/*!40000 ALTER TABLE `get_news` DISABLE KEYS */;
/*!40000 ALTER TABLE `get_news` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `n_admin`
--

DROP TABLE IF EXISTS `n_admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `n_admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) NOT NULL,
  `pass` varchar(40) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `n_admin`
--

LOCK TABLES `n_admin` WRITE;
/*!40000 ALTER TABLE `n_admin` DISABLE KEYS */;
INSERT INTO `n_admin` VALUES (1,'admin','b49515ad6e147d962c8696f31694ad8d');
/*!40000 ALTER TABLE `n_admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `news_comment`
--

DROP TABLE IF EXISTS `news_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `news_comment` (
  `news_id` varchar(20) NOT NULL,
  `comment` varchar(20000) DEFAULT NULL,
  KEY `FK_get_news_news_comment` (`news_id`),
  CONSTRAINT `FK_get_news_news_comment` FOREIGN KEY (`news_id`) REFERENCES `get_news` (`news_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news_comment`
--

LOCK TABLES `news_comment` WRITE;
/*!40000 ALTER TABLE `news_comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `news_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `news_mess`
--

DROP TABLE IF EXISTS `news_mess`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `news_mess` (
  `news_id` varchar(20) NOT NULL,
  `tag` varchar(20) NOT NULL,
  `read_times` int(11) NOT NULL DEFAULT '0',
  `love_times` int(11) NOT NULL DEFAULT '0',
  `comment_times` int(11) DEFAULT '0',
  KEY `FK_get_news_news_mess` (`news_id`),
  CONSTRAINT `FK_get_news_news_mess` FOREIGN KEY (`news_id`) REFERENCES `get_news` (`news_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news_mess`
--

LOCK TABLES `news_mess` WRITE;
/*!40000 ALTER TABLE `news_mess` DISABLE KEYS */;
/*!40000 ALTER TABLE `news_mess` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `news_recommend`
--

DROP TABLE IF EXISTS `news_recommend`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `news_recommend` (
  `user_id` varchar(10) NOT NULL,
  `news_score` mediumtext,
  KEY `FK_user_news_recomment` (`user_id`),
  CONSTRAINT `FK_user_news_recomment` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news_recommend`
--

LOCK TABLES `news_recommend` WRITE;
/*!40000 ALTER TABLE `news_recommend` DISABLE KEYS */;
/*!40000 ALTER TABLE `news_recommend` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `news_tag_deep`
--

DROP TABLE IF EXISTS `news_tag_deep`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `news_tag_deep` (
  `news_id` varchar(20) NOT NULL,
  `news_society` double DEFAULT NULL,
  `news_entertainment` double DEFAULT NULL,
  `news_tech` double DEFAULT NULL,
  `news_car` double DEFAULT NULL,
  `news_sports` double DEFAULT NULL,
  `news_finance` double DEFAULT NULL,
  `news_military` double DEFAULT NULL,
  `news_world` double DEFAULT NULL,
  `news_fashion` double DEFAULT NULL,
  `news_travel` double DEFAULT NULL,
  `news_discovery` double DEFAULT NULL,
  `news_baby` double DEFAULT NULL,
  `news_regimen` double DEFAULT NULL,
  `news_story` double DEFAULT NULL,
  `news_essay` double DEFAULT NULL,
  `news_game` double DEFAULT NULL,
  `news_history` double DEFAULT NULL,
  `news_food` double DEFAULT NULL,
  KEY `FK_get_news_news_tag_deep` (`news_id`),
  CONSTRAINT `FK_get_news_news_tag_deep` FOREIGN KEY (`news_id`) REFERENCES `get_news` (`news_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news_tag_deep`
--

LOCK TABLES `news_tag_deep` WRITE;
/*!40000 ALTER TABLE `news_tag_deep` DISABLE KEYS */;
/*!40000 ALTER TABLE `news_tag_deep` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `user_id` varchar(10) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `passwd` varchar(40) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('000001','15767956536','用户15767956536','441ecebf73c4f37ef5112c4629dd4d7c','2016-06-02 08:32:48');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_behavior`
--

DROP TABLE IF EXISTS `user_behavior`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_behavior` (
  `user_id` varchar(10) NOT NULL,
  `news_id` varchar(20) NOT NULL,
  `news_tag` varchar(20) NOT NULL,
  `behavior_type` int(11) NOT NULL DEFAULT '0',
  `weight` double DEFAULT NULL,
  `is_comment` int(11) NOT NULL DEFAULT '0',
  `address` varchar(100) DEFAULT NULL,
  `news_way` int(11) NOT NULL DEFAULT '0',
  `age` varchar(20) DEFAULT NULL,
  `score` int(11) NOT NULL DEFAULT '0',
  KEY `FK_user_user_behavior` (`user_id`),
  KEY `FK_get_news_user_behavior` (`news_id`),
  CONSTRAINT `FK_get_news_user_behavior` FOREIGN KEY (`news_id`) REFERENCES `get_news` (`news_id`),
  CONSTRAINT `FK_user_user_behavior` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_behavior`
--

LOCK TABLES `user_behavior` WRITE;
/*!40000 ALTER TABLE `user_behavior` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_behavior` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_mess`
--

DROP TABLE IF EXISTS `user_mess`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_mess` (
  `user_id` varchar(10) NOT NULL,
  `sex` int(11) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `email` varchar(20) DEFAULT NULL,
  `address` varchar(40) DEFAULT NULL,
  `image` varchar(60) DEFAULT NULL,
  UNIQUE KEY `email` (`email`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `fk_user_mess` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_mess`
--

LOCK TABLES `user_mess` WRITE;
/*!40000 ALTER TABLE `user_mess` DISABLE KEYS */;
INSERT INTO `user_mess` VALUES ('000001',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `user_mess` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_operate`
--

DROP TABLE IF EXISTS `user_operate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_operate` (
  `user_id` varchar(10) NOT NULL,
  `news_id` varchar(20) NOT NULL,
  `comment` varchar(1000) DEFAULT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `FK_get_news_user_operate` (`news_id`),
  KEY `FK_user_user_operator` (`user_id`),
  CONSTRAINT `FK_get_news_user_operate` FOREIGN KEY (`news_id`) REFERENCES `get_news` (`news_id`),
  CONSTRAINT `FK_user_user_operator` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_operate`
--

LOCK TABLES `user_operate` WRITE;
/*!40000 ALTER TABLE `user_operate` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_operate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_tag_deep`
--

DROP TABLE IF EXISTS `user_tag_deep`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_tag_deep` (
  `user_id` varchar(10) NOT NULL,
  `news_society` double DEFAULT NULL,
  `news_entertainment` double DEFAULT NULL,
  `news_tech` double DEFAULT NULL,
  `news_car` double DEFAULT NULL,
  `news_sports` double DEFAULT NULL,
  `news_finance` double DEFAULT NULL,
  `news_military` double DEFAULT NULL,
  `news_world` double DEFAULT NULL,
  `news_fashion` double DEFAULT NULL,
  `news_travel` double DEFAULT NULL,
  `news_discovery` double DEFAULT NULL,
  `news_baby` double DEFAULT NULL,
  `news_regimen` double DEFAULT NULL,
  `news_story` double DEFAULT NULL,
  `news_essay` double DEFAULT NULL,
  `news_game` double DEFAULT NULL,
  `news_history` double DEFAULT NULL,
  `news_food` double DEFAULT NULL,
  KEY `FK_user_user_tag_deep` (`user_id`),
  CONSTRAINT `FK_user_user_tag_deep` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_tag_deep`
--

LOCK TABLES `user_tag_deep` WRITE;
/*!40000 ALTER TABLE `user_tag_deep` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_tag_deep` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_tag_score`
--

DROP TABLE IF EXISTS `user_tag_score`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_tag_score` (
  `user_id` varchar(10) NOT NULL,
  `news_society` double DEFAULT NULL,
  `news_entertainment` double DEFAULT NULL,
  `news_tech` double DEFAULT NULL,
  `news_car` double DEFAULT NULL,
  `news_sports` double DEFAULT NULL,
  `news_finance` double DEFAULT NULL,
  `news_military` double DEFAULT NULL,
  `news_world` double DEFAULT NULL,
  `news_fashion` double DEFAULT NULL,
  `news_travel` double DEFAULT NULL,
  `news_discovery` double DEFAULT NULL,
  `news_baby` double DEFAULT NULL,
  `news_regimen` double DEFAULT NULL,
  `news_story` double DEFAULT NULL,
  `news_essay` double DEFAULT NULL,
  `news_game` double DEFAULT NULL,
  `news_history` double DEFAULT NULL,
  `news_food` double DEFAULT NULL,
  KEY `FK_user_user_tag_score` (`user_id`),
  CONSTRAINT `FK_user_user_tag_score` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_tag_score`
--

LOCK TABLES `user_tag_score` WRITE;
/*!40000 ALTER TABLE `user_tag_score` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_tag_score` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-06-02 16:38:55
