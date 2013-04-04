CREATE TABLE `users` (
  `user_id` int(10) NOT NULL AUTO_INCREMENT,
  `username` varchar(12) NOT NULL,
  `password` varchar(64) NOT NULL,
  `salt` varchar(64) NOT NULL,
  `email` varchar(64) NOT NULL,
  `role` varchar(32) DEFAULT NULL,
  `allowed_databases` text,
  `invited` int(10) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=1260