CREATE TABLE `contact` (
                           `id` integer PRIMARY KEY AUTO_INCREMENT,
                           `name` varchar(100) NOT NULL,
                           `profile_image_url` varchar(255) NOT NULL DEFAULT '',
                           `email` varchar(255) NOT NULL DEFAULT '',
                           `phone` varchar(30) NOT NULL DEFAULT '',
                           `company` varchar(100) NOT NULL DEFAULT '',
                           `job_title` varchar(100) NOT NULL DEFAULT '',
                           `memo` longtext DEFAULT NULL,
                           `address` varchar(255) NOT NULL DEFAULT '',
                           `birthday` date DEFAULT NULL,
                           `website` varchar(255) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `label_map` (
                             `id` integer PRIMARY KEY AUTO_INCREMENT,
                             `contact_id` integer NOT NULL,
                             `label_id` integer NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `label` (
                         `id` integer PRIMARY KEY AUTO_INCREMENT,
                         `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

ALTER TABLE `label_map` ADD FOREIGN KEY (`contact_id`) REFERENCES `contact` (`id`);
ALTER TABLE `label_map` ADD FOREIGN KEY (`label_id`) REFERENCES `label` (`id`);
