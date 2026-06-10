-- AdventureWorks Datawarehouse Schema Creation Script
-- Suitable for MySQL / MariaDB

CREATE DATABASE IF NOT EXISTS `aw_datawarehouse`
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_general_ci;

USE `aw_datawarehouse`;

-- 1. aw_customers_lookup
CREATE TABLE IF NOT EXISTS `aw_customers_lookup` (
  `CustomerKey` INT NOT NULL,
  `Prefix` VARCHAR(6) DEFAULT NULL,
  `FirstName` VARCHAR(45) DEFAULT NULL,
  `LastName` VARCHAR(45) DEFAULT NULL,
  `BirthDate` DATE DEFAULT NULL,
  `MaritalStatus` VARCHAR(5) DEFAULT NULL,
  `Gender` VARCHAR(5) DEFAULT NULL,
  `EmailAddress` VARCHAR(45) DEFAULT NULL,
  `AnnualIncome` INT DEFAULT NULL,
  `TotalChildren` INT DEFAULT NULL,
  `EducationLevel` VARCHAR(45) DEFAULT NULL,
  `Occupation` VARCHAR(45) DEFAULT NULL,
  `HomeOwner` VARCHAR(3) DEFAULT NULL,
  `FullName` VARCHAR(70) DEFAULT NULL,
  `UserName` VARCHAR(45) DEFAULT NULL,
  `Domain` VARCHAR(45) DEFAULT NULL,
  `IncomeLevel` VARCHAR(45) DEFAULT NULL,
  `BirthYear` INT DEFAULT NULL,
  `CurrentAge` INT DEFAULT NULL,
  `Parent` VARCHAR(45) DEFAULT NULL,
  `CustomerPriority` VARCHAR(45) DEFAULT NULL,
  PRIMARY KEY (`CustomerKey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. aw_products_lookup
CREATE TABLE IF NOT EXISTS `aw_products_lookup` (
  `ProductKey` INT NOT NULL,
  `ProductSubcategoryKey` INT DEFAULT NULL,
  `ProductSKU` VARCHAR(20) DEFAULT NULL,
  `ProductName` VARCHAR(45) DEFAULT NULL,
  `ModelName` VARCHAR(45) DEFAULT NULL,
  `ProductDescription` LONGTEXT DEFAULT NULL,
  `ProductColor` VARCHAR(45) DEFAULT NULL,
  `ProductStyle` VARCHAR(5) DEFAULT NULL,
  `ProductCost` DECIMAL(10,2) DEFAULT NULL,
  `ProductPrice` DECIMAL(10,2) DEFAULT NULL,
  `SKUType` VARCHAR(25) DEFAULT NULL,
  `DiscountPrice` DECIMAL(10,4) DEFAULT NULL,
  `PricePoint` VARCHAR(25) DEFAULT NULL,
  `SKUCategory` VARCHAR(25) DEFAULT NULL,
  PRIMARY KEY (`ProductKey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. aw_calendar_lookup
CREATE TABLE IF NOT EXISTS `aw_calendar_lookup` (
  `Date` DATE NOT NULL,
  `StartOfMonth` DATE DEFAULT NULL,
  `MonthName` VARCHAR(45) DEFAULT NULL,
  `StartOfYear` DATE DEFAULT NULL,
  `Year` INT DEFAULT NULL,
  `DayOfWeek` INT DEFAULT NULL,
  `Weekend` VARCHAR(45) DEFAULT NULL,
  `ShortMonth` VARCHAR(45) DEFAULT NULL,
  `ShortDay` VARCHAR(45) DEFAULT NULL,
  `DayName` VARCHAR(45) DEFAULT NULL,
  PRIMARY KEY (`Date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. aw_product_category_lookup
CREATE TABLE IF NOT EXISTS `aw_product_category_lookup` (
  `ProductCategoryKey` INT NOT NULL,
  `CategoryName` VARCHAR(45) DEFAULT NULL,
  PRIMARY KEY (`ProductCategoryKey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. aw_product_subcategory_lookup
CREATE TABLE IF NOT EXISTS `aw_product_subcategory_lookup` (
  `ProductSubcategoryKey` INT NOT NULL,
  `SubcategoryName` VARCHAR(45) DEFAULT NULL,
  `ProductCategoryKey` INT NOT NULL,
  PRIMARY KEY (`ProductSubcategoryKey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. aw_territories_lookup
CREATE TABLE IF NOT EXISTS `aw_territories_lookup` (
  `SalesTerritoryKey` INT NOT NULL,
  `Region` VARCHAR(45) DEFAULT NULL,
  `Country` VARCHAR(45) DEFAULT NULL,
  `Continent` VARCHAR(45) DEFAULT NULL,
  PRIMARY KEY (`SalesTerritoryKey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. aw_returns
CREATE TABLE IF NOT EXISTS `aw_returns` (
  `ReturnDate` DATE DEFAULT NULL,
  `TerritoryKey` INT DEFAULT NULL,
  `ProductKey` INT DEFAULT NULL,
  `ReturnQuantity` INT DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. aw_sales
CREATE TABLE IF NOT EXISTS `aw_sales` (
  `OrderDate` DATE DEFAULT NULL,
  `StockDate` DATE DEFAULT NULL,
  `OrderNumber` VARCHAR(45) DEFAULT NULL,
  `ProductKey` INT DEFAULT NULL,
  `CustomerKey` INT DEFAULT NULL,
  `TerritoryKey` INT DEFAULT NULL,
  `OrderLineItem` INT DEFAULT NULL,
  `OrderQuantity` INT DEFAULT NULL,
  `QuantityType` VARCHAR(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
