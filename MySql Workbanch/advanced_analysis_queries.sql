-- =============================================
-- ADVANCED ADVENTUREWORKS ANALYSIS QUERIES
-- FOR POWER BI PROFESSIONAL DASHBOARD
-- =============================================

USE aw_datawarehouse;

-- 1. KEY PERFORMANCE INDICATORS (KPIs)
SELECT 
    'Total Sales (Records)' AS KPI,
    COUNT(*) AS Value
FROM aw_sales
UNION ALL
SELECT 
    'Total Returns',
    COUNT(*)
FROM aw_returns
UNION ALL
SELECT 
    'Total Customers',
    COUNT(*)
FROM aw_customers_lookup
UNION ALL
SELECT 
    'Total Products',
    COUNT(*)
FROM aw_products_lookup;

-- 2. TOP 10 PRODUCTS BY SALES COUNT
SELECT 
    p.ProductName,
    COUNT(s.ProductKey) AS TotalSales,
    SUM(s.OrderQuantity) AS TotalQuantity
FROM aw_sales s
LEFT JOIN aw_products_lookup p ON s.ProductKey = p.ProductKey
GROUP BY p.ProductName
ORDER BY TotalSales DESC
LIMIT 10;

-- 3. SALES BY YEAR & MONTH
SELECT 
    YEAR(c.Date) AS Year,
    MONTH(c.Date) AS Month,
    MONTHNAME(c.Date) AS MonthName,
    COUNT(s.OrderQuantity) AS MonthlySales
FROM aw_sales s
LEFT JOIN aw_calendar_lookup c ON s.OrderDate = c.Date
GROUP BY YEAR(c.Date), MONTH(c.Date), MONTHNAME(c.Date)
ORDER BY Year, Month;

-- 4. SALES BY TERRITORY
SELECT 
    t.Region,
    t.Country,
    t.Continent,
    COUNT(s.SalesTerritoryKey) AS SalesCount
FROM aw_sales s
LEFT JOIN aw_territories_lookup t ON s.TerritoryKey = t.SalesTerritoryKey
GROUP BY t.Region, t.Country, t.Continent
ORDER BY SalesCount DESC;

-- 5. RETURNS BY PRODUCT
SELECT 
    p.ProductName,
    COUNT(r.ProductKey) AS ReturnCount
FROM aw_returns r
LEFT JOIN aw_products_lookup p ON r.ProductKey = p.ProductKey
GROUP BY p.ProductName
ORDER BY ReturnCount DESC
LIMIT 10;

-- 6. CUSTOMER DEMOGRAPHICS - INCOME LEVEL DISTRIBUTION
SELECT 
    IncomeLevel,
    COUNT(*) AS CustomerCount
FROM aw_customers_lookup
GROUP BY IncomeLevel
ORDER BY CustomerCount DESC;

-- 7. SALES BY PRODUCT CATEGORY
SELECT 
    c.CategoryName,
    COUNT(s.ProductKey) AS SalesCount
FROM aw_sales s
LEFT JOIN aw_products_lookup p ON s.ProductKey = p.ProductKey
LEFT JOIN aw_product_subcategory_lookup sc ON p.ProductSubcategoryKey = sc.ProductSubcategoryKey
LEFT JOIN aw_product_category_lookup c ON sc.ProductCategoryKey = c.ProductCategoryKey
GROUP BY c.CategoryName
ORDER BY SalesCount DESC;
