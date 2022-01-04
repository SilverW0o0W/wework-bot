CREATE TABLE `project` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL DEFAULT '',
  `url` varchar(256) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
)DEFAULT CHARSET=utf8mb4;