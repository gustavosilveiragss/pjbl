-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: pjbl
-- ------------------------------------------------------
-- Server version	8.0.36-0ubuntu0.22.04.1

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
-- Table structure for table `actuator_model`
--

DROP TABLE IF EXISTS `actuator_model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actuator_model` (
  `actuator_model_id` int NOT NULL AUTO_INCREMENT,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`actuator_model_id`),
  KEY `idx_actuator_model_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actuator_model`
--

LOCK TABLES `actuator_model` WRITE;
/*!40000 ALTER TABLE `actuator_model` DISABLE KEYS */;
INSERT INTO `actuator_model` VALUES (1,'2024-05-01 03:00:00','Button'),(2,'2024-05-01 03:00:00','Buzzer');
/*!40000 ALTER TABLE `actuator_model` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device` (
  `device_id` int NOT NULL AUTO_INCREMENT,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` int NOT NULL,
  `device_name` varchar(255) NOT NULL,
  `password` varchar(3) NOT NULL,
  `permission_state` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`device_id`),
  KEY `idx_device_user_id` (`user_id`),
  CONSTRAINT `device_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
INSERT INTO `device` VALUES (1,'2024-05-01 03:00:00',1,'Halux','',0),(2,'2024-05-01 03:00:00',1,'Test Box','000',0);
/*!40000 ALTER TABLE `device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_actuator`
--

DROP TABLE IF EXISTS `device_actuator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device_actuator` (
  `device_actuator_id` int NOT NULL AUTO_INCREMENT,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `device_id` int NOT NULL,
  `actuator_model_id` int NOT NULL,
  `value` varchar(255) NOT NULL,
  PRIMARY KEY (`device_actuator_id`),
  KEY `idx_device_actuator_device_id` (`device_id`),
  KEY `idx_device_actuator_actuator_model_id` (`actuator_model_id`),
  CONSTRAINT `device_actuator_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `device` (`device_id`),
  CONSTRAINT `device_actuator_ibfk_2` FOREIGN KEY (`actuator_model_id`) REFERENCES `actuator_model` (`actuator_model_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_actuator`
--

LOCK TABLES `device_actuator` WRITE;
/*!40000 ALTER TABLE `device_actuator` DISABLE KEYS */;
INSERT INTO `device_actuator` VALUES (5,'2024-05-01 03:00:00',2,1,'0'),(6,'2024-05-01 03:00:00',2,2,'800');
/*!40000 ALTER TABLE `device_actuator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_sensor`
--

DROP TABLE IF EXISTS `device_sensor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device_sensor` (
  `device_sensor_id` int NOT NULL AUTO_INCREMENT,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `device_id` int NOT NULL,
  `sensor_model_id` int NOT NULL,
  `value` varchar(255) NOT NULL,
  PRIMARY KEY (`device_sensor_id`),
  KEY `idx_device_sensor_device_id` (`device_id`),
  KEY `idx_device_sensor_sensor_model_id` (`sensor_model_id`),
  CONSTRAINT `device_sensor_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `device` (`device_id`),
  CONSTRAINT `device_sensor_ibfk_2` FOREIGN KEY (`sensor_model_id`) REFERENCES `sensor_model` (`sensor_model_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_sensor`
--

LOCK TABLES `device_sensor` WRITE;
/*!40000 ALTER TABLE `device_sensor` DISABLE KEYS */;
INSERT INTO `device_sensor` VALUES (7,'2024-05-01 03:00:00',2,1,'25'),(8,'2024-05-01 03:00:00',2,2,'50'),(9,'2024-05-01 03:00:00',2,3,'1');
/*!40000 ALTER TABLE `device_sensor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mqtt_logs`
--

DROP TABLE IF EXISTS `mqtt_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mqtt_logs` (
  `mqtt_log_id` int NOT NULL AUTO_INCREMENT,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `topic` varchar(255) NOT NULL,
  `subtopic` varchar(255) NOT NULL,
  `device_id` int NULL,
  `operation` varchar(255) NOT NULL,
  `payload` varchar(255) NOT NULL,
  PRIMARY KEY (`mqtt_log_id`),
  KEY `idx_mqtt_logs_device_id` (`device_id`),
  KEY `idx_mqtt_logs_topic` (`topic`),
  KEY `idx_mqtt_logs_subtopic` (`subtopic`),
  CONSTRAINT `mqtt_logs_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `device` (`device_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mqtt_logs`
--

LOCK TABLES `mqtt_logs` WRITE;
/*!40000 ALTER TABLE `mqtt_logs` DISABLE KEYS */;
INSERT INTO `mqtt_logs` VALUES (1,'2024-05-01 03:00:00','PERMISSION_STATE','REQ',2,'W','1'),(2,'2024-05-01 03:00:00','IR_STATE','REQ',2,'W','1'),(3,'2024-05-01 03:00:00','PASSWORD','REQ',2,'W','000'),(4,'2024-05-01 03:00:00','FREQUENCY','REQ',2,'W','100'),(5,'2024-05-01 03:00:00','TEMPERATURE','REQ',2,'W','25'),(6,'2024-05-01 03:00:00','HUMIDITY','REQ',2,'W','30');
/*!40000 ALTER TABLE `mqtt_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor_model`
--

DROP TABLE IF EXISTS `sensor_model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensor_model` (
  `sensor_model_id` int NOT NULL AUTO_INCREMENT,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`sensor_model_id`),
  KEY `idx_sensor_model_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor_model`
--

LOCK TABLES `sensor_model` WRITE;
/*!40000 ALTER TABLE `sensor_model` DISABLE KEYS */;
INSERT INTO `sensor_model` VALUES (1,'2024-05-01 03:00:00','DHT22 - Temperature'),(2,'2024-05-01 03:00:00','DHT22 - Humidity'),(3,'2024-05-01 03:00:00','TCRT5000');
/*!40000 ALTER TABLE `sensor_model` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `role` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`),
  KEY `idx_user_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'2024-05-01 03:00:00','admin','admin','admin'),(2,'2024-05-01 03:00:00','operator','operator','operator'),(3,'2024-05-01 03:00:00','statistics','statistics','statistics');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-27 21:04:17
