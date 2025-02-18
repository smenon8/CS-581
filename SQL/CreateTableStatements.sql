-- MySQL Script generated by MySQL Workbench
-- Mon Apr 18 23:28:27 2016
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema ParkingProject
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `ParkingProject` ;

-- -----------------------------------------------------
-- Schema ParkingProject
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `ParkingProject` DEFAULT CHARACTER SET latin1 ;
USE `ParkingProject` ;

-- -----------------------------------------------------
-- Table `ParkingProject`.`availability`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ParkingProject`.`availability` ;

CREATE TABLE IF NOT EXISTS `ParkingProject`.`availability` (
  `block_id` INT(11) NULL DEFAULT NULL,
  `available` INT(11) NULL DEFAULT NULL,
  `datetimestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

CREATE INDEX `idx_availability_id` USING HASH ON `ParkingProject`.`availability` (`block_id` ASC);

CREATE INDEX `idx_availability_ts` USING HASH ON `ParkingProject`.`availability` (`datetimestamp` ASC);


-- -----------------------------------------------------
-- Table `ParkingProject`.`edges`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ParkingProject`.`edges` ;

CREATE TABLE IF NOT EXISTS `ParkingProject`.`edges` (
  `block_id` INT(11) NULL DEFAULT NULL,
  `block_name` VARCHAR(128) NULL DEFAULT NULL,
  `latitude_1` CHAR(20) NULL DEFAULT NULL,
  `longitude_1` CHAR(20) NULL DEFAULT NULL,
  `latitude_2` CHAR(20) NULL DEFAULT NULL,
  `longitude_2` CHAR(20) NULL DEFAULT NULL,
  `node_id_1` INT(11) NULL DEFAULT NULL,
  `node_id_2` INT(11) NULL DEFAULT NULL,
  `no_blocks` INT(11) NULL DEFAULT NULL,
  `operational` INT(11) NULL DEFAULT NULL,
  `latitude` CHAR(20) NULL DEFAULT NULL,
  `longitude` CHAR(20) NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `ParkingProject`.`nodes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ParkingProject`.`nodes` ;

CREATE TABLE IF NOT EXISTS `ParkingProject`.`nodes` (
  `node_id` INT(11) NULL DEFAULT NULL,
  `latitude` CHAR(20) NULL DEFAULT NULL,
  `longitude` CHAR(20) NULL DEFAULT NULL,
  `node_name` VARCHAR(128) NULL DEFAULT NULL,
  `coordinate` POINT NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `ParkingProject`.`preComputeMatrixWalk`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ParkingProject`.`preComputeMatrixWalk` ;

CREATE TABLE IF NOT EXISTS `ParkingProject`.`preComputeMatrixWalk` (
  `block_id` INT(11) NOT NULL,
  `source_lat` CHAR(20) NULL DEFAULT NULL,
  `source_long` CHAR(20) NULL DEFAULT NULL,
  `node_id` INT(11) NOT NULL,
  `dest_lat` CHAR(20) NULL DEFAULT NULL,
  `dest_long` CHAR(20) NULL DEFAULT NULL,
  `distance` INT(11) NULL DEFAULT NULL,
  `time` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`block_id`, `node_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `ParkingProject`.`preComputeWalk`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ParkingProject`.`preComputeWalk` ;

CREATE TABLE IF NOT EXISTS `ParkingProject`.`preComputeWalk` (
  `block_id` INT(11) NOT NULL,
  `node_id` INT(11) NOT NULL,
  `distance` INT(11) NULL DEFAULT NULL,
  `time` INT(11) NULL DEFAULT NULL,
  `source_lat` CHAR(20) NULL DEFAULT NULL,
  `source_long` CHAR(20) NULL DEFAULT NULL,
  `dest_lat` CHAR(20) NULL DEFAULT NULL,
  `dest_long` CHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (`block_id`, `node_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `ParkingProject`.`precomputeMatrix`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ParkingProject`.`precomputeMatrix` ;

CREATE TABLE IF NOT EXISTS `ParkingProject`.`precomputeMatrix` (
  `start_block` INT(11) NOT NULL,
  `source_lat` CHAR(20) NULL DEFAULT NULL,
  `source_long` CHAR(20) NULL DEFAULT NULL,
  `end_block` INT(11) NOT NULL DEFAULT '0',
  `dest_lat` CHAR(20) NULL DEFAULT NULL,
  `dest_long` CHAR(20) NULL DEFAULT NULL,
  `distance` INT(11) NULL DEFAULT NULL,
  `time` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`start_block`, `end_block`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

CREATE INDEX `idx1_precomputeMatrix` ON `ParkingProject`.`precomputeMatrix` (`source_lat` ASC, `source_long` ASC);

CREATE INDEX `idx2_precomputeMatrix` ON `ParkingProject`.`precomputeMatrix` (`dest_lat` ASC, `dest_long` ASC);


-- -----------------------------------------------------
-- Table `ParkingProject`.`probabilisticData`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ParkingProject`.`probabilisticData` ;

CREATE TABLE IF NOT EXISTS `ParkingProject`.`probabilisticData` (
  `block_id` INT(11) NULL DEFAULT NULL,
  `avg_avail` INT(11) NULL DEFAULT NULL,
  `dayname` CHAR(100) NULL DEFAULT NULL,
  `hour_of_day` INT(11) NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

CREATE INDEX `block_id` ON `ParkingProject`.`probabilisticData` (`block_id` ASC, `dayname` ASC, `hour_of_day` ASC, `avg_avail` ASC);


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
