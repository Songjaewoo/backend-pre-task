CREATE SCHEMA `contact_db` DEFAULT CHARACTER SET utf8mb4 ;

CREATE TABLE `contact` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `profile_image_url` varchar(255) NOT NULL DEFAULT '',
  `name` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL DEFAULT '',
  `phone` varchar(30) NOT NULL DEFAULT '',
  `company` varchar(100) NOT NULL DEFAULT '',
  `job_title` varchar(100) NOT NULL DEFAULT '',
  `memo` longtext DEFAULT NULL,
  `address` varchar(255) NOT NULL DEFAULT '',
  `birthday` date DEFAULT NULL,
  `website` varchar(200) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `label` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `contact_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `label_contact_id_fk_contact_id` (`contact_id`),
  CONSTRAINT `label_contact_id_fk_contact_id` FOREIGN KEY (`contact_id`) REFERENCES `contact` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


