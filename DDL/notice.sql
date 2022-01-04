CREATE TABLE `notice` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `project_id` bigint(20) NOT NULL DEFAULT '0',
  `robot_id` bigint(20) NOT NULL DEFAULT '0',
  `type` int(11) NOT NULL DEFAULT '0',
  `sub_type` int(11) NOT NULL DEFAULT '0',
  `notice_time` bigint(20) NOT NULL DEFAULT '0',
  `status` int(11) NOT NULL DEFAULT '0',
  `created_time` bigint(20) NOT NULL DEFAULT '0',
  `updated_time` bigint(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8mb4;