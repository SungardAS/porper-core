CREATE TABLE `Customer` (
  `id` varchar(50) NOT NULL DEFAULT '',
  `name` varchar(100) NOT NULL DEFAULT '',
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Group` (
  `id` varchar(50) NOT NULL DEFAULT '',
  `name` varchar(100) NOT NULL DEFAULT '',
  `customer_id` varchar(50) NOT NULL DEFAULT '',
  `role_id` varchar(50) DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_idx` (`name`),
  KEY `Group_Role` (`role_id`),
  KEY `Customer_Group` (`customer_id`),
--  CONSTRAINT `Group_Role` FOREIGN KEY (`role_id`) REFERENCES `Role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `User` (
  `id` varchar(100) NOT NULL DEFAULT '',
  `email` varchar(100) NOT NULL DEFAULT '',
  `auth_type` varchar(10) NOT NULL DEFAULT '',
  `name` varchar(100) NOT NULL DEFAULT '',
  `family_name` varchar(50) NOT NULL DEFAULT '',
  `given_name` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Role` (
  `id` varchar(50) NOT NULL DEFAULT '',
  `name` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Function` (
  `id` varchar(50) NOT NULL DEFAULT '',
  `name` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Group_User` (
  `id` varchar(50) NOT NULL DEFAULT '',
  `group_id` varchar(50) NOT NULL DEFAULT '',
  `user_id` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `Group_has_User` (`group_id`),
  KEY `User_in_Group` (`user_id`),
  CONSTRAINT `Group_has_User` FOREIGN KEY (`group_id`) REFERENCES `Group` (`id`),
  CONSTRAINT `User_in_Group` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `InvitedUser` (
  `id` varchar(50) NOT NULL DEFAULT '',
  `email` varchar(100) NOT NULL DEFAULT '',
  `auth_type` varchar(10) NOT NULL DEFAULT '',
  `group_id` varchar(50) NOT NULL DEFAULT '',
  `invited_at` datetime NOT NULL,
  `invited_by` varchar(100) NOT NULL DEFAULT '',
  `state` varchar(10) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `Group_InvitedUser` (`group_id`),
  CONSTRAINT `Group_InvitedUser` FOREIGN KEY (`group_id`) REFERENCES `Group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Token` (
  `id` varchar(50) NOT NULL DEFAULT '',
  `access_token` mediumtext NOT NULL,
  `refresh_token` mediumtext NOT NULL,
  `user_id` varchar(100) NOT NULL DEFAULT '',
  `refreshed_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `User_Token` (`user_id`),
  CONSTRAINT `User_Token` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Permission` (
  `id` varchar(100) NOT NULL DEFAULT '',
  `action` varchar(1) NOT NULL DEFAULT '',
  `res_name` varchar(20) NOT NULL DEFAULT '',
  `value` varchar(36) DEFAULT NULL,
  `group_id` varchar(50) DEFAULT NULL,
  `user_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Group_Index` (`group_id`),
  KEY `User_Index` (`user_id`),
  KEY `Res_Name_Index` (`res_name`),
  CONSTRAINT `Group_Permission` FOREIGN KEY (`group_id`) REFERENCES `Group` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `User_Permission` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Function_Permission` (
  `id` varchar(50) NOT NULL DEFAULT '',
  `function_id` varchar(50) NOT NULL DEFAULT '',
  `permission_id` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `Function_has_Permission` (`function_id`),
  KEY `Permission_in_Function` (`permission_id`),
  CONSTRAINT `Function_has_Permission` FOREIGN KEY (`function_id`) REFERENCES `Function` (`id`),
  CONSTRAINT `Permission_in_Function` FOREIGN KEY (`permission_id`) REFERENCES `Permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Role_Function` (
  `id` varchar(50) NOT NULL DEFAULT '',
  `role_id` varchar(50) NOT NULL DEFAULT '',
  `function_id` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `Role_has_Function` (`role_id`),
  KEY `Function_in_Role` (`function_id`),
  CONSTRAINT `Function_in_Role` FOREIGN KEY (`function_id`) REFERENCES `Function` (`id`),
  CONSTRAINT `Role_has_Function` FOREIGN KEY (`role_id`) REFERENCES `Role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
