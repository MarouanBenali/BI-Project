-- =============================================
-- FINAL ADVENTUREWORKS STAR SCHEMA FIX
-- =============================================
-- ANALYSIS OF INITIAL ISSUES:
-- 1. NO FOREIGN KEYS EXISTED BEFORE!
-- 2. Column Name Mismatch:
--    - aw_sales & aw_returns use "TerritoryKey"
--    - aw_territories_lookup uses "SalesTerritoryKey"
--    - BUT DATA TYPE IS THE SAME (INT(11)): OKAY!
-- 3. All PK/FK data types match!
-- 4. No orphan records existed (from earlier checks): OKAY!

USE aw_datawarehouse;

-- =============================================
-- FINAL FIX SQL (SAFE TO RUN MULTIPLE TIMES)
-- =============================================

-- 1. Fix Product Hierarchy
ALTER TABLE aw_product_subcategory_lookup 
DROP FOREIGN KEY IF EXISTS fk_subcategory_category, 
ADD CONSTRAINT fk_subcategory_category 
FOREIGN KEY (ProductCategoryKey) 
REFERENCES aw_product_category_lookup (ProductCategoryKey);

ALTER TABLE aw_products_lookup 
DROP FOREIGN KEY IF EXISTS fk_product_subcategory, 
ADD CONSTRAINT fk_product_subcategory 
FOREIGN KEY (ProductSubcategoryKey) 
REFERENCES aw_product_subcategory_lookup (ProductSubcategoryKey);

-- 2. Fix aw_sales Fact Table
ALTER TABLE aw_sales 
DROP FOREIGN KEY IF EXISTS fk_sales_customer, 
ADD CONSTRAINT fk_sales_customer 
FOREIGN KEY (CustomerKey) 
REFERENCES aw_customers_lookup (CustomerKey);

ALTER TABLE aw_sales 
DROP FOREIGN KEY IF EXISTS fk_sales_product, 
ADD CONSTRAINT fk_sales_product 
FOREIGN KEY (ProductKey) 
REFERENCES aw_products_lookup (ProductKey);

ALTER TABLE aw_sales 
DROP FOREIGN KEY IF EXISTS fk_sales_territory, 
ADD CONSTRAINT fk_sales_territory 
FOREIGN KEY (TerritoryKey) 
REFERENCES aw_territories_lookup (SalesTerritoryKey);

ALTER TABLE aw_sales 
DROP FOREIGN KEY IF EXISTS fk_sales_calendar, 
ADD CONSTRAINT fk_sales_calendar 
FOREIGN KEY (OrderDate) 
REFERENCES aw_calendar_lookup (Date);

-- 3. Fix aw_returns Fact Table
ALTER TABLE aw_returns 
DROP FOREIGN KEY IF EXISTS fk_returns_product, 
ADD CONSTRAINT fk_returns_product 
FOREIGN KEY (ProductKey) 
REFERENCES aw_products_lookup (ProductKey);

ALTER TABLE aw_returns 
DROP FOREIGN KEY IF EXISTS fk_returns_territory, 
ADD CONSTRAINT fk_returns_territory 
FOREIGN KEY (TerritoryKey) 
REFERENCES aw_territories_lookup (SalesTerritoryKey);

ALTER TABLE aw_returns 
DROP FOREIGN KEY IF EXISTS fk_returns_calendar, 
ADD CONSTRAINT fk_returns_calendar 
FOREIGN KEY (ReturnDate) 
REFERENCES aw_calendar_lookup (Date);

-- =============================================
-- END OF FIXES
-- =============================================
