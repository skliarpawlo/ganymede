drop database if exists ganymede;
create database ganymede;

use ganymede;

CREATE TABLE `gany_jobs` (
  `name` varchar(80),
  `repo` varchar(255),
  `branch` varchar(80),
  `env` text,
  `tests` text,
  primary key(`name`)
) default charset=utf8;

CREATE TABLE `gany_tasks` (
  `task_id` int(11) not null auto_increment,
  `job_name` varchar(80),
  `status` enum('waiting', 'running', 'fail', 'success') not null default 'waiting',
  `add_time` TIMESTAMP,
  `end_time` TIMESTAMP,
  `log` TEXT not null default "",
  `artifacts` TEXT not null default "[]",
  primary key(`task_id`),
  foreign key(`job_name`) references `gany_jobs`(`name`)
) default charset=utf8;

CREATE TABLE `gany_tests` (
  `test_id` int(11) not null auto_increment,
  `code` text,
  `status` enum('new', 'accepted') not null default 'new',
  primary key(`test_id`)
) default charset=utf8;