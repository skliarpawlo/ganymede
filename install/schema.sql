CREATE TABLE `gany_jobs` (
  `name` varchar(80),
  `repo` varchar(255),
  `branch` varchar(80),
  `env` text,
  `tests` text,
  primary key(`name`)
);

CREATE TABLE `gany_tasks` (
  `id` int(11) not null auto_increment,
  `job_name` varchar(80),
  `status` enum('WAITING', 'RUNNING', 'ERROR', 'FINISHED') not null default 'WAITING',
  `add_time` TIMESTAMP,
  `end_time` TIMESTAMP,
  `log` TEXT,
  primary key(`id`),
  foreign key(`job_name`) references `gany_jobs`(`name`)
);