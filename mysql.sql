-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: smartscreen
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `ai_training_plans`
--

DROP TABLE IF EXISTS `ai_training_plans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ai_training_plans` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '目标学生ID',
  `plan_content` json NOT NULL COMMENT '培养方案详情 (包含学习路径、资源推荐等)',
  `generated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '生成时间',
  `status` enum('进行中','已完成') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '进行中' COMMENT '方案状态',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `ai_training_plans_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI个性化培养方案表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ai_training_plans`
--

LOCK TABLES `ai_training_plans` WRITE;
/*!40000 ALTER TABLE `ai_training_plans` DISABLE KEYS */;
INSERT INTO `ai_training_plans` VALUES (1,4,'{\"goal\": \"成为一名优秀的嵌入式硬件工程师\", \"path\": [{\"stage\": 1, \"content\": \"学习电路基础与PCB设计\"}, {\"stage\": 2, \"content\": \"掌握STM32单片机开发\"}, {\"stage\": 3, \"content\": \"进阶Linux驱动开发\"}], \"resources\": [\"《电路分析》\", \"Altium Designer教程\"]}','2025-07-20 15:55:11','进行中');
/*!40000 ALTER TABLE `ai_training_plans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `announcements`
--

DROP TABLE IF EXISTS `announcements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `announcements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '标题',
  `content` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '内容',
  `author_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '发布者名称',
  `type` enum('通知','新闻','动态','安全提示','天气提示','名言金句') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '公告类型',
  `is_important` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否为重要通知',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '发布时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='通知公告表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `announcements`
--

LOCK TABLES `announcements` WRITE;
/*!40000 ALTER TABLE `announcements` DISABLE KEYS */;
INSERT INTO `announcements` VALUES (1,'实验室安全培训通知','本周五下午2点将进行全体成员安全培训，请务必参加。','黄老师','通知',1,'2025-07-18 03:00:00'),(2,'设备维护通知','信号发生器（Keysight E8257D）正在维修中，暂停使用。','系统管理员','安全提示',0,'2025-07-19 01:00:00'),(3,'科技创新，青春正当时','鼓励大家积极参与科创项目，勇攀科技高峰。','基地管委会','名言金句',0,'2025-07-20 00:00:00');
/*!40000 ALTER TABLE `announcements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendance_logs`
--

DROP TABLE IF EXISTS `attendance_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `check_in_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '签到时间',
  `check_out_time` timestamp NULL DEFAULT NULL COMMENT '签出时间 (可选)',
  `method` enum('人脸识别','扫码','手动') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '考勤方式',
  `emotion_status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'AI情绪检测结果 (可选)',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `attendance_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考勤记录表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance_logs`
--

LOCK TABLES `attendance_logs` WRITE;
/*!40000 ALTER TABLE `attendance_logs` DISABLE KEYS */;
INSERT INTO `attendance_logs` VALUES (1,3,'2025-07-20 00:55:12',NULL,'人脸识别','开心'),(2,4,'2025-07-20 00:58:03',NULL,'人脸识别','平静'),(3,5,'2025-07-20 01:01:45',NULL,'扫码','平静');
/*!40000 ALTER TABLE `attendance_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_categories`
--

DROP TABLE IF EXISTS `device_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device_categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '分类名称 (如 ''测量仪器'', ''开发平台'')',
  PRIMARY KEY (`id`),
  UNIQUE KEY `category_name` (`category_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='设备分类表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_categories`
--

LOCK TABLES `device_categories` WRITE;
/*!40000 ALTER TABLE `device_categories` DISABLE KEYS */;
INSERT INTO `device_categories` VALUES (3,'动手实践'),(2,'开发平台'),(1,'测量仪器');
/*!40000 ALTER TABLE `device_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_usage_logs`
--

DROP TABLE IF EXISTS `device_usage_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device_usage_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` int NOT NULL COMMENT '设备ID',
  `user_id` int DEFAULT NULL COMMENT '使用者ID',
  `checkout_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '借出时间',
  `checkin_time` timestamp NULL DEFAULT NULL COMMENT '归还时间 (可为空)',
  `notes` text COLLATE utf8mb4_unicode_ci COMMENT '备注',
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `device_usage_logs_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `device_usage_logs_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='设备使用记录表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_usage_logs`
--

LOCK TABLES `device_usage_logs` WRITE;
/*!40000 ALTER TABLE `device_usage_logs` DISABLE KEYS */;
INSERT INTO `device_usage_logs` VALUES (1,2,4,'2025-07-20 01:30:00',NULL,NULL),(2,5,3,'2025-07-20 02:00:00',NULL,NULL),(3,1,6,'2025-07-19 06:00:00','2025-07-19 10:00:00',NULL);
/*!40000 ALTER TABLE `device_usage_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devices`
--

DROP TABLE IF EXISTS `devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `devices` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '设备名称 (如 ''矢量网络分析仪'')',
  `category_id` int NOT NULL COMMENT '设备分类ID',
  `model` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '型号',
  `status` enum('可用','使用中','维修中','报废') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '可用' COMMENT '设备当前状态',
  `location` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '存放位置',
  `image_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '设备图片地址',
  `purchase_date` date DEFAULT NULL COMMENT '购置日期',
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `devices_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `device_categories` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='设备表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices`
--

LOCK TABLES `devices` WRITE;
/*!40000 ALTER TABLE `devices` DISABLE KEYS */;
INSERT INTO `devices` VALUES (1,'频谱分析仪',1,'R&S FSW26','可用','A区-01柜','/images/devices/fsw26.png',NULL),(2,'矢量网络分析仪',1,'Keysight E5071C','使用中','B区-02柜','/images/devices/e5071c.png',NULL),(3,'示波器',1,'Tektronix MSO4','可用','A区-03柜','/images/devices/mso4.png',NULL),(4,'信号发生器',1,'Keysight E8257D','维修中','维修间','/images/devices/e8257d.png',NULL),(5,'Linux开发套件',2,'自研平台 v2.0','使用中','C区-实验台1','/images/devices/linux_kit.png',NULL),(6,'FPGA开发套件',2,'Xilinx Zynq-7000','可用','C区-实验台2','/images/devices/zynq7000.png',NULL),(7,'电烙铁',3,'HAKKO FX-888D','可用','工具墙','/images/devices/fx888d.png',NULL),(8,'热风枪',3,'QUICK 861DW','可用','工具墙','/images/devices/861dw.png',NULL);
/*!40000 ALTER TABLE `devices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `environmental_logs`
--

DROP TABLE IF EXISTS `environmental_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `environmental_logs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sensor_type` enum('温度','湿度','光照','CO2') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '传感器类型',
  `value` decimal(10,2) NOT NULL COMMENT '监测数值',
  `unit` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '单位 (如 ''°C'', ''%'', ''lux'', ''ppm'')',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录时间',
  `lab_id` int NOT NULL COMMENT '所属实验室ID',
  PRIMARY KEY (`id`),
  KEY `lab_id` (`lab_id`),
  CONSTRAINT `environmental_logs_ibfk_1` FOREIGN KEY (`lab_id`) REFERENCES `labs` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='环境监测日志表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `environmental_logs`
--

LOCK TABLES `environmental_logs` WRITE;
/*!40000 ALTER TABLE `environmental_logs` DISABLE KEYS */;
INSERT INTO `environmental_logs` VALUES (1,'温度',25.50,'°C','2025-07-20 15:55:11',1),(2,'湿度',60.20,'%','2025-07-20 15:55:11',1),(3,'光照',800.00,'lux','2025-07-20 15:55:11',1),(4,'CO2',450.00,'ppm','2025-07-20 15:55:11',1);
/*!40000 ALTER TABLE `environmental_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `labs`
--

DROP TABLE IF EXISTS `labs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `labs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lab_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '实验室名称 (如 ''通信电子创新基地'')',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '基地简介',
  `culture_info` json DEFAULT NULL COMMENT '文化理念 (如 ''五大文化'', ''四个YU之道'')',
  `logo_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Logo图片地址',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='实验室信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `labs`
--

LOCK TABLES `labs` WRITE;
/*!40000 ALTER TABLE `labs` DISABLE KEYS */;
INSERT INTO `labs` VALUES (1,'通信电子创新基地','一个集物联网感知、智能交互与信息化管理于一体的实验室智能终端系统。','{\"values\": \"四个YU之道\", \"main_culture\": \"不忘初心，砥砺前行\"}','/images/lab_logo.png');
/*!40000 ALTER TABLE `labs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_members`
--

DROP TABLE IF EXISTS `project_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_members` (
  `project_id` int NOT NULL,
  `user_id` int NOT NULL,
  `role_in_project` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '在项目中的角色 (如 ''负责人'', ''组员'')',
  PRIMARY KEY (`project_id`,`user_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `project_members_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `project_members_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='项目成员表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_members`
--

LOCK TABLES `project_members` WRITE;
/*!40000 ALTER TABLE `project_members` DISABLE KEYS */;
INSERT INTO `project_members` VALUES (1,3,'负责人'),(1,4,'硬件组'),(1,5,'软件组'),(1,6,'算法组');
/*!40000 ALTER TABLE `project_members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '项目名称',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '项目描述',
  `achievement_type` enum('获奖','专利','软著') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '成果类型',
  `achievement_details` text COLLATE utf8mb4_unicode_ci COMMENT '成果详情 (如 ''XX大赛一等奖'')',
  `start_date` date DEFAULT NULL COMMENT '项目开始日期',
  `end_date` date DEFAULT NULL COMMENT '项目结束日期',
  `image_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '项目展示图片/证书地址',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='项目成果表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES (1,'基于物联网技术的智慧蔬菜大棚监测系统','该系统利用多种传感器实时监测大棚环境，并通过云平台进行数据分析和远程控制，实现蔬菜种植的智能化管理。','获奖','2024年（第17届）中国大学生计算机设计大赛江西省级赛 一等奖','2023-09-01','2024-06-01','/images/projects/cert_vege.png');
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `role_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色名称 (如 ''学生'', ''教师'', ''管理员'')',
  `permissions` json DEFAULT NULL COMMENT '角色的权限列表',
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'学生','{\"read\": true, \"write_self\": true}'),(2,'教师','{\"read\": true, \"write_all\": true, \"manage_courses\": true}'),(3,'管理员','{\"read\": true, \"write_all\": true, \"manage_all\": true}');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `safety_guidelines`
--

DROP TABLE IF EXISTS `safety_guidelines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `safety_guidelines` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '类别 (如 ''电气安全'', ''应急处置'')',
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '标题',
  `content` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '详细内容',
  `version` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '版本号',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='安全须知表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `safety_guidelines`
--

LOCK TABLES `safety_guidelines` WRITE;
/*!40000 ALTER TABLE `safety_guidelines` DISABLE KEYS */;
INSERT INTO `safety_guidelines` VALUES (1,'电气安全','使用设备前检查线路完整性','1. 确保电源线无破损、裸露。\n2. 严禁湿手触摸电源开关。\n3. 发现电气故障立即断电并报告管理员。','1.0'),(2,'应急处置','火灾应急','1. 立即按下火警报警器。\n2. 拨打119报警。\n3. 使用灭火器初期灭火。\n4. 有序疏散。','1.1');
/*!40000 ALTER TABLE `safety_guidelines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedules`
--

DROP TABLE IF EXISTS `schedules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schedules` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '课程/活动名称',
  `teacher_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '授课教师',
  `class_date` date NOT NULL COMMENT '上课日期',
  `start_time` time NOT NULL COMMENT '开始时间',
  `end_time` time NOT NULL COMMENT '结束时间',
  `location` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '上课地点',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='课程表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedules`
--

LOCK TABLES `schedules` WRITE;
/*!40000 ALTER TABLE `schedules` DISABLE KEYS */;
INSERT INTO `schedules` VALUES (1,'嵌入式系统开发','黄老师','2025-07-21','14:00:00','16:30:00','德育楼305'),(2,'信号与系统','李教授','2025-07-22','09:00:00','11:30:00','德育楼305');
/*!40000 ALTER TABLE `schedules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_roles`
--

DROP TABLE IF EXISTS `user_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_roles` (
  `user_id` int NOT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`role_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `user_roles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_roles_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户角色关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_roles`
--

LOCK TABLES `user_roles` WRITE;
/*!40000 ALTER TABLE `user_roles` DISABLE KEYS */;
INSERT INTO `user_roles` VALUES (3,1),(4,1),(5,1),(6,1),(2,2),(1,3);
/*!40000 ALTER TABLE `user_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户名/学号',
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '加密后的密码',
  `full_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '真实姓名',
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '电子邮箱',
  `phone_number` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '电话号码',
  `face_data` blob COMMENT '用于人脸识别的生物特征数据 (可选)',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '账号创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone_number` (`phone_number`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','$2a$12$R.gJb/U9jT.C2.X.Y.Z.a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p.q.r','系统管理员','admin@example.com','13800138000',NULL,'2025-07-20 15:55:11'),(2,'2024001','$2a$12$R.gJb/U9jT.C2.X.Y.Z.a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p.q.r','黄老师','teacher.huang@example.com','13800138001',NULL,'2025-07-20 15:55:11'),(3,'2024101','$2a$12$R.gJb/U9jT.C2.X.Y.Z.a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p.q.r','吴文静','wuwenjing@example.com','13800138101',NULL,'2025-07-20 15:55:11'),(4,'2024102','$2a$12$R.gJb/U9jT.C2.X.Y.Z.a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p.q.r','黄旺','huangwang@example.com','13800138102',NULL,'2025-07-20 15:55:11'),(5,'2024103','$2a$12$R.gJb/U9jT.C2.X.Y.Z.a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p.q.r','朱海月','zhuhaiyue@example.com','13800138103',NULL,'2025-07-20 15:55:11'),(6,'2024104','$2a$12$R.gJb/U9jT.C2.X.Y.Z.a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p.q.r','张祖宁','zhangzuning@example.com','13800138104',NULL,'2025-07-20 15:55:11');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-20 23:56:53
