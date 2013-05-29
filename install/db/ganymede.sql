CREATE TABLE `gany_jobs` (
  `job_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) DEFAULT NULL,
  `whose` varchar(64) DEFAULT NULL,
  `repo` varchar(255) DEFAULT NULL,
  `branch` varchar(80) DEFAULT NULL,
  `deploy` text,
  `exec_time` time DEFAULT NULL,
  `users` text,
  PRIMARY KEY (`job_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

CREATE TABLE `gany_tasks` (
  `task_id` int(11) not null auto_increment,
  `job_id` int(11),
  `status` enum('waiting', 'running', 'fail', 'success') not null default 'waiting',
  `whose` varchar(64) DEFAULT NULL,
  `add_time` TIMESTAMP,
  `end_time` TIMESTAMP,
  `total_time` int(11) default -1,
  `log` MEDIUMTEXT not null,
  `result` MEDIUMTEXT not null,
  `artifacts` TEXT not null,
  primary key(`task_id`),
  foreign key(`job_id`) references `gany_jobs`(`job_id`) on delete cascade
) ENGINE=InnoDB default charset=utf8;

CREATE TABLE `gany_tests` (
  `test_id` int(11) not null auto_increment,
  `whose` varchar(64) DEFAULT NULL,
  `code` text,
  `status` enum('new', 'accepted') not null default 'new',
  primary key(`test_id`)
) ENGINE=InnoDB default charset=utf8;

CREATE TABLE `gany_jobs_to_tests` (
  `job_id` int(11) not null,
  `test_id` int(11) not null,
  primary key (`job_id`, `test_id`),
  foreign key (`job_id`) references `gany_jobs`(`job_id`) on delete cascade,
  foreign key (`test_id`) references `gany_tests`(`test_id`) on delete cascade
) ENGINE=InnoDB  default charset=utf8;

CREATE TABLE `gany_env` (
  `env_id` int(11) NOT NULL AUTO_INCREMENT,
  `job_id` int(11) NOT NULL,
  `path` varchar(255) NOT NULL,
  `lang` varchar(64) NOT NULL,
  `code` text,
  PRIMARY KEY (`env_id`),
  UNIQUE KEY `path_per_job` (`job_id`,`path`),
  CONSTRAINT `gany_env_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `gany_jobs` (`job_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `gany_tags` (
  `tag_id` int(10) NOT NULL AUTO_INCREMENT,
  `value` varchar(64) NOT NULL DEFAULT '',
  PRIMARY KEY (`tag_id`),
  UNIQUE KEY `value` (`value`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `gany_tests_to_tags` (
  `test_id` int(11) NOT NULL,
  `tag_id` int(10) NOT NULL,
  PRIMARY KEY (`test_id`,`tag_id`),
  FOREIGN KEY (`test_id`) REFERENCES gany_tests(`test_id`) ON DELETE CASCADE,
  FOREIGN KEY (`tag_id`) REFERENCES gany_tags(`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8