CREATE TABLE `robot` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL DEFAULT '',
  `webhook` varchar(1024) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
)DEFAULT CHARSET=utf8mb4;