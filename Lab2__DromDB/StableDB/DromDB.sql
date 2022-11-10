PRAGMA
foreign_keys=on;

-- -----------------------------------------------------
-- Table `Fuel`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Fuel`;
CREATE TABLE `Fuel`
(
    `FuelType` VARCHAR(20) NOT NULL UNIQUE,
    PRIMARY KEY (`FuelType`)
);

-- -----------------------------------------------------
-- Table `Engine`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Engine`;
CREATE TABLE `Engine`
(
    `IDEngine` VARCHAR(10) NOT NULL UNIQUE,
    `Capacity` DOUBLE      NOT NULL,
    `HP`       INTEGER     NOT NULL,
    `FuelType` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`IDEngine`),
    FOREIGN KEY (`FuelType`)
        REFERENCES `Fuel` (`FuelType`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
);


-- -----------------------------------------------------
-- Table `Country`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Country`;
CREATE TABLE `Country`
(
    `CountryName` VARCHAR(30) NOT NULL UNIQUE,
    PRIMARY KEY (`CountryName`)
);

-- -----------------------------------------------------
-- Table `Brand`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Brand`;
CREATE TABLE `Brand`
(
    `BrandName`   VARCHAR(50) NOT NULL UNIQUE,
    `CountryName` VARCHAR(30) NOT NULL,
    PRIMARY KEY (`BrandName`),
    FOREIGN KEY (`CountryName`)
        REFERENCES `Country` (`CountryName`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
);


-- -----------------------------------------------------
-- Table `Model`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Model`;
CREATE TABLE `Model`
(
    `BrandName` VARCHAR(50) NOT NULL,
    `ModelName` VARCHAR(50) NOT NULL,
    UNIQUE (`BrandName`, `ModelName`),
    PRIMARY KEY (`BrandName`, `ModelName`),
    FOREIGN KEY (`BrandName`)
        REFERENCES `Brand` (`BrandName`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
);


-- -----------------------------------------------------
-- Table `Drive`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Drive`;
CREATE TABLE `Drive`
(
    `DriveType` VARCHAR(10) NOT NULL UNIQUE,
    PRIMARY KEY (`DriveType`)
);


-- -----------------------------------------------------
-- Table `Transmission`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Transmission`;
CREATE TABLE `Transmission`
(
    `TransmissionType` VARCHAR(20) NOT NULL UNIQUE,
    PRIMARY KEY (`TransmissionType`)
);


-- -----------------------------------------------------
-- Table `City`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `City`;
CREATE TABLE `City`
(
    `CityName`    VARCHAR(50) NOT NULL,
    `CountryName` VARCHAR(30) NOT NULL,
    UNIQUE (`CityName`, `CountryName`),
        PRIMARY KEY (`CityName`),
    FOREIGN KEY (`CountryName`)
        REFERENCES `Country` (`CountryName`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
);


-- -----------------------------------------------------
-- Table `User`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `User`;
CREATE TABLE `User`
(
    `IDUser`       INT          NOT NULL UNIQUE,
    `Login`        VARCHAR(100) NOT NULL UNIQUE,
    `Password`     VARCHAR(100) NOT NULL,
    `FIO`          VARCHAR(100) NOT NULL,
    `PhoneNumber`  VARCHAR(20)  NOT NULL UNIQUE,
    `EmailAddress` VARCHAR(45) NULL UNIQUE,
    `CityName`     VARCHAR(50)  NOT NULL,
    PRIMARY KEY (`IDUser`),
    FOREIGN KEY (`CityName`)
        REFERENCES `City` (`CityName`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
);


-- -----------------------------------------------------
-- Table `Car`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Car`;
CREATE TABLE `Car`
(
    `IDCar`            INT         NOT NULL UNIQUE,
    `IDUser`           INT         NOT NULL,
    `BodyOrVinNumber`  VARCHAR(45) NOT NULL,
    `StateNumber`      VARCHAR(45) NOT NULL,
    `BrandName`        VARCHAR(50) NOT NULL,
    `ModelName`        VARCHAR(50) NOT NULL,
    `IDEngine`         VARCHAR(10) NOT NULL,
    `ReleaseDate`      DATE        NOT NULL,
    `TransmissionType` VARCHAR(20) NOT NULL,
    `DriveType`        VARCHAR(10) NOT NULL,
    `IDEquip`          VARCHAR(45) NULL,
    PRIMARY KEY (`IDCar`),
    FOREIGN KEY (`IDEngine`)
        REFERENCES `Engine` (`IDEngine`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    FOREIGN KEY (`ModelName`, `BrandName`)
        REFERENCES `Model` (`ModelName`, `BrandName`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    FOREIGN KEY (`DriveType`)
        REFERENCES `Drive` (`DriveType`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    FOREIGN KEY (`TransmissionType`)
        REFERENCES `Transmission` (`TransmissionType`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    FOREIGN KEY (`IDUser`)
        REFERENCES `User` (`IDUser`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
);


-- -----------------------------------------------------
-- Table `Selling`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Selling`;
CREATE TABLE `Selling`
(
    `IDSelling`      INT    NOT NULL UNIQUE,
    `IDCar`          INT    NOT NULL,
    `Actuality`      TINYINT ZEROFILL NOT NULL,
    `Price`          DOUBLE NOT NULL,
    `Description`    VARCHAR(10000) NULL,
    `AdditionDate`   DATE   NOT NULL,
    `ExpirationDate` DATE   NOT NULL,
    PRIMARY KEY (`IDSelling`),
    FOREIGN KEY (`IDCar`)
        REFERENCES `Car` (`IDCar`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
);