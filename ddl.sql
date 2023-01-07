-- 주의: UserLogin 생성 후 Ledger 생성할 것

-- payhere.UserLogin definition

CREATE TABLE `UserLogin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(120) NOT NULL,
  `password` varchar(256) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UserLogin_UN` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;

-- payhere.Ledger definition

CREATE TABLE `Ledger` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `price` int(11) NOT NULL,
  `memo` varchar(120) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Ledger_FK` (`user_id`),
  CONSTRAINT `Ledger_FK` FOREIGN KEY (`user_id`) REFERENCES `UserLogin` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

-- UserLogin insert 쿼리 실행 후, Ledger insert 쿼리 실행할 것

INSERT INTO payhere.UserLogin
(id, email, password)
VALUES(1, 'imwoodam@hanmail.net', '$5$rounds=535000$wAZmxrDS5CI5ocSi$a5P7kYvc0bTwdEhXjhjgcAz2NU/IKzoozNOjrOQF0B/');



INSERT INTO payhere.Ledger
(id, price, memo, user_id)
VALUES(1, 100000, 'test', 1);
INSERT INTO payhere.Ledger
(id, price, memo, user_id)
VALUES(2, 3000, 'correct memo without price', 1);
INSERT INTO payhere.Ledger
(id, price, memo, user_id)
VALUES(3, 5000, 'modified memo from ledger id 3', 1);
INSERT INTO payhere.Ledger
(id, price, memo, user_id)
VALUES(9, 100000, 'test', 1);
