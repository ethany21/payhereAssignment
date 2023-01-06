CREATE TABLE `Ledger` (
  `id` int NOT NULL AUTO_INCREMENT,
  `price` int NOT NULL,
  `memo` varchar(120) NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Ledger_FK` (`user_id`),
  CONSTRAINT `Ledger_FK` FOREIGN KEY (`user_id`) REFERENCES `UserLogin` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `UserLogin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(120) NOT NULL,
  `password` varchar(256) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UserLogin_UN` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;