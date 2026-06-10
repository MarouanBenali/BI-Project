-- =====================================================
-- Data Integrity & Relationship Validation Queries
-- AdventureWorks Datawarehouse
-- =====================================================

USE `aw_datawarehouse`;

-- =====================================================
-- 1. BASIC ROW COUNT VALIDATION
-- =====================================================
SELECT '=== BASIC ROW COUNT VALIDATION ===' AS 'CHECK_TYPE';
SELECT 'aw_customers_lookup' AS 'TABLE_NAME', COUNT(*) AS 'ROW_COUNT' FROM aw_customers_lookup
UNION ALL
SELECT 'aw_products_lookup', COUNT(*) FROM aw_products_lookup
UNION ALL
SELECT 'aw_calendar_lookup', COUNT(*) FROM aw_calendar_lookup
UNION ALL
SELECT 'aw_territories_lookup', COUNT(*) FROM aw_territories_lookup
UNION ALL
SELECT 'aw_product_category_lookup', COUNT(*) FROM aw_product_category_lookup
UNION ALL
SELECT 'aw_product_subcategory_lookup', COUNT(*) FROM aw_product_subcategory_lookup
UNION ALL
SELECT 'aw_sales', COUNT(*) FROM aw_sales
UNION ALL
SELECT 'aw_returns', COUNT(*) FROM aw_returns;

-- =====================================================
-- 2. CHECK FOR NULL KEYS IN FACT TABLES (CRITICAL!)
-- =====================================================
SELECT '\n=== NULL KEYS IN FACT TABLES ===' AS 'CHECK_TYPE';

-- Check aw_sales for NULL keys
SELECT 
    'aw_sales' AS 'TABLE_NAME',
    SUM(CASE WHEN OrderDate IS NULL THEN 1 ELSE 0 END) AS 'NULL_OrderDate',
    SUM(CASE WHEN ProductKey IS NULL THEN 1 ELSE 0 END) AS 'NULL_ProductKey',
    SUM(CASE WHEN CustomerKey IS NULL THEN 1 ELSE 0 END) AS 'NULL_CustomerKey',
    SUM(CASE WHEN TerritoryKey IS NULL THEN 1 ELSE 0 END) AS 'NULL_TerritoryKey'
FROM aw_sales;

-- Check aw_returns for NULL keys
SELECT 
    'aw_returns' AS 'TABLE_NAME',
    SUM(CASE WHEN ReturnDate IS NULL THEN 1 ELSE 0 END) AS 'NULL_ReturnDate',
    SUM(CASE WHEN ProductKey IS NULL THEN 1 ELSE 0 END) AS 'NULL_ProductKey',
    SUM(CASE WHEN TerritoryKey IS NULL THEN 1 ELSE 0 END) AS 'NULL_TerritoryKey'
FROM aw_returns;

-- =====================================================
-- 3. REFERENTIAL INTEGRITY CHECK: ORPHAN RECORDS IN aw_sales
-- =====================================================
SELECT '\n=== ORPHAN RECORDS IN aw_sales ===' AS 'CHECK_TYPE';

-- Orphan CustomerKeys in Sales
SELECT 'Orphan CustomerKeys' AS 'ISSUE', COUNT(*) AS 'ORPHAN_COUNT'
FROM aw_sales s
LEFT JOIN aw_customers_lookup c ON s.CustomerKey = c.CustomerKey
WHERE c.CustomerKey IS NULL;

-- Orphan ProductKeys in Sales
SELECT 'Orphan ProductKeys' AS 'ISSUE', COUNT(*) AS 'ORPHAN_COUNT'
FROM aw_sales s
LEFT JOIN aw_products_lookup p ON s.ProductKey = p.ProductKey
WHERE p.ProductKey IS NULL;

-- Orphan TerritoryKeys in Sales
SELECT 'Orphan TerritoryKeys' AS 'ISSUE', COUNT(*) AS 'ORPHAN_COUNT'
FROM aw_sales s
LEFT JOIN aw_territories_lookup t ON s.TerritoryKey = t.SalesTerritoryKey
WHERE t.SalesTerritoryKey IS NULL;

-- Orphan OrderDate in Sales (Calendar lookup)
SELECT 'Orphan OrderDate' AS 'ISSUE', COUNT(*) AS 'ORPHAN_COUNT'
FROM aw_sales s
LEFT JOIN aw_calendar_lookup cal ON s.OrderDate = cal.Date
WHERE cal.Date IS NULL;

-- =====================================================
-- 4. REFERENTIAL INTEGRITY CHECK: ORPHAN RECORDS IN aw_returns
-- =====================================================
SELECT '\n=== ORPHAN RECORDS IN aw_returns ===' AS 'CHECK_TYPE';

-- Orphan ProductKeys in Returns
SELECT 'Orphan ProductKeys' AS 'ISSUE', COUNT(*) AS 'ORPHAN_COUNT'
FROM aw_returns r
LEFT JOIN aw_products_lookup p ON r.ProductKey = p.ProductKey
WHERE p.ProductKey IS NULL;

-- Orphan TerritoryKeys in Returns
SELECT 'Orphan TerritoryKeys' AS 'ISSUE', COUNT(*) AS 'ORPHAN_COUNT'
FROM aw_returns r
LEFT JOIN aw_territories_lookup t ON r.TerritoryKey = t.SalesTerritoryKey
WHERE t.SalesTerritoryKey IS NULL;

-- Orphan ReturnDate in Returns (Calendar lookup)
SELECT 'Orphan ReturnDate' AS 'ISSUE', COUNT(*) AS 'ORPHAN_COUNT'
FROM aw_returns r
LEFT JOIN aw_calendar_lookup cal ON r.ReturnDate = cal.Date
WHERE cal.Date IS NULL;

-- =====================================================
-- 5. PRODUCT SUBCATEGORY & CATEGORY RELATIONSHIP CHECK
-- =====================================================
SELECT '\n=== PRODUCT HIERARCHY INTEGRITY ===' AS 'CHECK_TYPE';

-- Orphan ProductSubcategoryKey in Products
SELECT 'Orphan ProductSubcategoryKey in Products' AS 'ISSUE', COUNT(*) AS 'ORPHAN_COUNT'
FROM aw_products_lookup p
LEFT JOIN aw_product_subcategory_lookup sc ON p.ProductSubcategoryKey = sc.ProductSubcategoryKey
WHERE p.ProductSubcategoryKey IS NOT NULL AND sc.ProductSubcategoryKey IS NULL;

-- Orphan ProductCategoryKey in Product Subcategories
SELECT 'Orphan ProductCategoryKey in Subcategories' AS 'ISSUE', COUNT(*) AS 'ORPHAN_COUNT'
FROM aw_product_subcategory_lookup sc
LEFT JOIN aw_product_category_lookup c ON sc.ProductCategoryKey = c.ProductCategoryKey
WHERE c.ProductCategoryKey IS NULL;

-- =====================================================
-- 6. COMPREHENSIVE JOIN VALIDATION - AW_SALES WITH ALL DIMENSIONS
-- =====================================================
SELECT '\n=== AW_SALES FULL JOIN VALIDATION SUMMARY ===' AS 'CHECK_TYPE';

SELECT
    COUNT(*) AS 'Total_Sales_Records',
    SUM(CASE WHEN c.CustomerKey IS NOT NULL THEN 1 ELSE 0 END) AS 'Valid_Customer_Joins',
    SUM(CASE WHEN p.ProductKey IS NOT NULL THEN 1 ELSE 0 END) AS 'Valid_Product_Joins',
    SUM(CASE WHEN t.SalesTerritoryKey IS NOT NULL THEN 1 ELSE 0 END) AS 'Valid_Territory_Joins',
    SUM(CASE WHEN cal.Date IS NOT NULL THEN 1 ELSE 0 END) AS 'Valid_Calendar_Joins',
    SUM(CASE 
        WHEN c.CustomerKey IS NOT NULL 
        AND p.ProductKey IS NOT NULL 
        AND t.SalesTerritoryKey IS NOT NULL 
        AND cal.Date IS NOT NULL 
        THEN 1 ELSE 0 END) AS 'Fully_Valid_Records'
FROM aw_sales s
LEFT JOIN aw_customers_lookup c ON s.CustomerKey = c.CustomerKey
LEFT JOIN aw_products_lookup p ON s.ProductKey = p.ProductKey
LEFT JOIN aw_territories_lookup t ON s.TerritoryKey = t.SalesTerritoryKey
LEFT JOIN aw_calendar_lookup cal ON s.OrderDate = cal.Date;

-- =====================================================
-- 7. COMPREHENSIVE JOIN VALIDATION - AW_RETURNS WITH ALL DIMENSIONS
-- =====================================================
SELECT '\n=== AW_RETURNS FULL JOIN VALIDATION SUMMARY ===' AS 'CHECK_TYPE';

SELECT
    COUNT(*) AS 'Total_Returns_Records',
    SUM(CASE WHEN p.ProductKey IS NOT NULL THEN 1 ELSE 0 END) AS 'Valid_Product_Joins',
    SUM(CASE WHEN t.SalesTerritoryKey IS NOT NULL THEN 1 ELSE 0 END) AS 'Valid_Territory_Joins',
    SUM(CASE WHEN cal.Date IS NOT NULL THEN 1 ELSE 0 END) AS 'Valid_Calendar_Joins',
    SUM(CASE 
        WHEN p.ProductKey IS NOT NULL 
        AND t.SalesTerritoryKey IS NOT NULL 
        AND cal.Date IS NOT NULL 
        THEN 1 ELSE 0 END) AS 'Fully_Valid_Records'
FROM aw_returns r
LEFT JOIN aw_products_lookup p ON r.ProductKey = p.ProductKey
LEFT JOIN aw_territories_lookup t ON r.TerritoryKey = t.SalesTerritoryKey
LEFT JOIN aw_calendar_lookup cal ON r.ReturnDate = cal.Date;

-- =====================================================
-- 8. SAMPLE ORPHAN RECORDS (IF ANY) - FOR DETAILED ANALYSIS
-- =====================================================
SELECT '\n=== SAMPLE ORPHAN RECORDS (IF ANY) ===' AS 'CHECK_TYPE';

-- Sample orphan sales by customer
SELECT 'Sample orphan sales - CustomerKey' AS 'SAMPLE_TYPE', s.* 
FROM aw_sales s
LEFT JOIN aw_customers_lookup c ON s.CustomerKey = c.CustomerKey
WHERE c.CustomerKey IS NULL
LIMIT 5;

-- Sample orphan sales by product
SELECT 'Sample orphan sales - ProductKey' AS 'SAMPLE_TYPE', s.* 
FROM aw_sales s
LEFT JOIN aw_products_lookup p ON s.ProductKey = p.ProductKey
WHERE p.ProductKey IS NULL
LIMIT 5;

-- Sample orphan sales by territory
SELECT 'Sample orphan sales - TerritoryKey' AS 'SAMPLE_TYPE', s.* 
FROM aw_sales s
LEFT JOIN aw_territories_lookup t ON s.TerritoryKey = t.SalesTerritoryKey
WHERE t.SalesTerritoryKey IS NULL
LIMIT 5;

-- =====================================================
-- 9. DATA DISTRIBUTION CHECKS (OPTIONAL BUT USEFUL)
-- =====================================================
SELECT '\n=== DATA DISTRIBUTION CHECKS ===' AS 'CHECK_TYPE';

-- Sales by year
SELECT 'Sales by Year' AS 'METRIC', YEAR(OrderDate) AS 'YEAR', COUNT(*) AS 'COUNT'
FROM aw_sales
GROUP BY YEAR(OrderDate)
ORDER BY YEAR;

-- Returns by year
SELECT 'Returns by Year' AS 'METRIC', YEAR(ReturnDate) AS 'YEAR', COUNT(*) AS 'COUNT'
FROM aw_returns
GROUP BY YEAR(ReturnDate)
ORDER BY YEAR;

-- =====================================================
-- 10. DUPLICATE PRIMARY KEY CHECKS
-- =====================================================
SELECT '\n=== DUPLICATE PRIMARY KEY CHECKS ===' AS 'CHECK_TYPE';

-- Check for duplicate CustomerKeys
SELECT 'Duplicate CustomerKeys' AS 'ISSUE', CustomerKey, COUNT(*) AS 'COUNT'
FROM aw_customers_lookup
GROUP BY CustomerKey
HAVING COUNT(*) > 1;

-- Check for duplicate ProductKeys
SELECT 'Duplicate ProductKeys' AS 'ISSUE', ProductKey, COUNT(*) AS 'COUNT'
FROM aw_products_lookup
GROUP BY ProductKey
HAVING COUNT(*) > 1;

-- Check for duplicate Date in Calendar
SELECT 'Duplicate Dates in Calendar' AS 'ISSUE', Date, COUNT(*) AS 'COUNT'
FROM aw_calendar_lookup
GROUP BY Date
HAVING COUNT(*) > 1;

-- Check for duplicate SalesTerritoryKey
SELECT 'Duplicate SalesTerritoryKeys' AS 'ISSUE', SalesTerritoryKey, COUNT(*) AS 'COUNT'
FROM aw_territories_lookup
GROUP BY SalesTerritoryKey
HAVING COUNT(*) > 1;

-- =====================================================
-- END OF INTEGRITY CHECKS
-- =====================================================
