use lun_ua_new;

CREATE TABLE `gany_jobs` (
  `job_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) DEFAULT NULL,
  `repo` varchar(255) DEFAULT NULL,
  `branch` varchar(80) DEFAULT NULL,
  `env` text,
  `exec_time` time DEFAULT NULL,
  `users` text,
  PRIMARY KEY (`job_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8

CREATE TABLE `gany_tasks` (
  `task_id` int(11) not null auto_increment,
  `job_id` int(11),
  `status` enum('waiting', 'running', 'fail', 'success') not null default 'waiting',
  `add_time` TIMESTAMP,
  `end_time` TIMESTAMP,
  `total_time` int(11) default -1,
  `log` MEDIUMTEXT not null,
  `result` MEDIUMTEXT not null,
  `artifacts` TEXT not null,
  primary key(`task_id`),
  foreign key(`job_id`) references `gany_jobs`(`job_id`) on delete cascade
) default charset=utf8;

CREATE TABLE `gany_tests` (
  `test_id` int(11) not null auto_increment,
  `code` text,
  `status` enum('new', 'accepted') not null default 'new',
  primary key(`test_id`)
) default charset=utf8;


CREATE TABLE `gany_jobs_to_tests` (
  `job_id` int(11) not null,
  `test_id` int(11) not null,
  primary key (`job_id`, `test_id`),
  foreign key (`job_id`) references `gany_jobs`(`job_id`) on delete cascade,
  foreign key (`test_id`) references `gany_tests`(`test_id`) on delete cascade
) default charset=utf8;