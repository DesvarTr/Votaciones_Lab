-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: votaciones
-- ------------------------------------------------------
-- Server version	8.0.37

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
-- Table structure for table `estudiantes_info`
--

DROP TABLE IF EXISTS `estudiantes_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estudiantes_info` (
  `id_estudiante` int NOT NULL AUTO_INCREMENT,
  `CUI` varchar(15) NOT NULL,
  `nombres` varchar(100) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `fecha_creacion` date NOT NULL,
  `fecha_vencimiento` date NOT NULL,
  `genero` char(1) NOT NULL,
  `grado_id` int NOT NULL,
  `edad` int NOT NULL,
  `ya_voto` tinyint(1) NOT NULL,
  PRIMARY KEY (`id_estudiante`),
  KEY `estudiantes_info_id_estudiante_IDX` (`id_estudiante`,`CUI`,`nombres`,`apellidos`,`grado_id`,`fecha_nacimiento`,`edad`,`genero`,`fecha_creacion`,`fecha_vencimiento`) USING BTREE,
  KEY `estudiantes_info_grados_FK` (`grado_id`),
  CONSTRAINT `estudiantes_info_grados_FK` FOREIGN KEY (`grado_id`) REFERENCES `grados` (`grado_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estudiantes_info`
--

LOCK TABLES `estudiantes_info` WRITE;
/*!40000 ALTER TABLE `estudiantes_info` DISABLE KEYS */;
INSERT INTO `estudiantes_info` VALUES (1,'2829-93424-1155','José Fernando Emmanuel','Oliva Hernández','2007-12-30','2024-08-20','2024-09-20','M',27,16,1),(2,'3355-99798-2795','Daniela Aranza','Rosales Pocón','2007-02-04','2024-08-20','2024-09-20','F',28,17,1),(3,'6749-64157-3425','Rony Alejandro Rafael','Quiñonez Hernández','2006-12-26','2024-08-20','2024-09-20','M',26,17,1);
/*!40000 ALTER TABLE `estudiantes_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grados`
--

DROP TABLE IF EXISTS `grados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grados` (
  `grado_id` int NOT NULL AUTO_INCREMENT,
  `grado` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`grado_id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grados`
--

LOCK TABLES `grados` WRITE;
/*!40000 ALTER TABLE `grados` DISABLE KEYS */;
INSERT INTO `grados` VALUES (1,'Prepa_1'),(2,'Prepa_2'),(3,'Primero_Primaria_1'),(4,'Primero_Primaria_2'),(5,'Segundo_Primaria_1'),(6,'Segundo_Primaria_2'),(7,'Tercero_Primaria_1'),(8,'Tercero_Primaria_2'),(9,'Cuarto_Primaria_1'),(10,'Cuarto_Primaria_2'),(11,'Quinto_Primaria_1'),(12,'Quinto_Primaria_2'),(13,'Sexto_Primaria_1'),(14,'Sexto_Primaria_2'),(15,'Primero_Basico_1'),(16,'Primero_Basico_2'),(17,'Segundo_Basico_1'),(18,'Segundo_Basico_2'),(19,'Tercero_Basico_1'),(20,'Tercero_Basico_2'),(21,'Cuarto_CCLL_1'),(22,'Cuarto_CCLL_2'),(23,'Cuarto_BACO'),(24,'Cuarto_BADI'),(25,'Quinto_CCLL_1'),(26,'Quinto_CCLL_2'),(27,'Quinto_BACO'),(28,'Quinto_BADI');
/*!40000 ALTER TABLE `grados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `partidos`
--

DROP TABLE IF EXISTS `partidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `partidos` (
  `partido_id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `presidente` varchar(100) NOT NULL,
  `vice_presidente` varchar(100) NOT NULL,
  `No_Votos` int NOT NULL,
  PRIMARY KEY (`partido_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partidos`
--

LOCK TABLES `partidos` WRITE;
/*!40000 ALTER TABLE `partidos` DISABLE KEYS */;
INSERT INTO `partidos` VALUES (1,'Partido I','Presidente I','Vice I',1),(2,'Partido II','Presidente II','Vice II',1),(3,'Partido III','Presidente III','Vice III',1);
/*!40000 ALTER TABLE `partidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `votos`
--

DROP TABLE IF EXISTS `votos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `votos` (
  `id_voto` int NOT NULL AUTO_INCREMENT,
  `id_estudiante` int NOT NULL,
  PRIMARY KEY (`id_voto`),
  KEY `votaciones_estudiantes_info_FK` (`id_estudiante`),
  CONSTRAINT `votaciones_estudiantes_info_FK` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes_info` (`id_estudiante`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `votos`
--

LOCK TABLES `votos` WRITE;
/*!40000 ALTER TABLE `votos` DISABLE KEYS */;
INSERT INTO `votos` VALUES (1,1),(2,2),(3,3);
/*!40000 ALTER TABLE `votos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'votaciones'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-26  0:21:12
