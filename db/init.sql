CREATE DATABASE movie_player_users;

use movie_player_users;

CREATE TABLE users (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `surname` VARCHAR(45) NULL,
  `phone_number` VARCHAR(45) NULL,
  `email` VARCHAR(100) NOT NULL,
  `password` LONGTEXT NOT NULL,
  PRIMARY KEY (`id`));
