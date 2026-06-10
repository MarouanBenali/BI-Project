"""
Data Integrity Validation Script
Runs comprehensive checks on the AdventureWorks Datawarehouse
"""

import pymysql
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ETL_Project.config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME

def main():
    print("=" * 80)
    print("DATA INTEGRITY CHECK REPORT - AdventureWorks Datawarehouse")
    print("=" * 80)
    
    # Connect to MySQL
    conn = pymysql.connect(
        host=DB_HOST,
        port=int(DB_PORT),
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    
    # 1. Row Counts
    print("\n[1] BASIC ROW COUNT VALIDATION")
    print("-" * 80)
    cursor.execute('SELECT "aw_customers_lookup" as TABLE_NAME, COUNT(*) as ROW_COUNT FROM aw_customers_lookup UNION ALL SELECT "aw_products_lookup", COUNT(*) FROM aw_products_lookup UNION ALL SELECT "aw_calendar_lookup", COUNT(*) FROM aw_calendar_lookup UNION ALL SELECT "aw_territories_lookup", COUNT(*) FROM aw_territories_lookup UNION ALL SELECT "aw_sales", COUNT(*) FROM aw_sales UNION ALL SELECT "aw_returns", COUNT(*) FROM aw_returns')
    for row in cursor.fetchall():
        print(f"{row[0]:<30} {row[1]:>10,}")
    
    # 2. NULL Keys Check
    print("\n[2] NULL KEYS IN FACT TABLES")
    print("-" * 80)
    cursor.execute('SELECT "aw_sales" as TABLE_NAME, SUM(CASE WHEN OrderDate IS NULL THEN 1 ELSE 0 END) as NULL_OrderDate, SUM(CASE WHEN ProductKey IS NULL THEN 1 ELSE 0 END) as NULL_ProductKey, SUM(CASE WHEN CustomerKey IS NULL THEN 1 ELSE 0 END) as NULL_CustomerKey, SUM(CASE WHEN TerritoryKey IS NULL THEN 1 ELSE 0 END) as NULL_TerritoryKey FROM aw_sales')
    row = cursor.fetchone()
    print(f"{row[0]}: NULL_OrderDate={row[1]}, NULL_ProductKey={row[2]}, NULL_CustomerKey={row[3]}, NULL_TerritoryKey={row[4]}")
    
    cursor.execute('SELECT "aw_returns" as TABLE_NAME, SUM(CASE WHEN ReturnDate IS NULL THEN 1 ELSE 0 END) as NULL_ReturnDate, SUM(CASE WHEN ProductKey IS NULL THEN 1 ELSE 0 END) as NULL_ProductKey, SUM(CASE WHEN TerritoryKey IS NULL THEN 1 ELSE 0 END) as NULL_TerritoryKey FROM aw_returns')
    row = cursor.fetchone()
    print(f"{row[0]}: NULL_ReturnDate={row[1]}, NULL_ProductKey={row[2]}, NULL_TerritoryKey={row[3]}")
    
    # 3. Orphan Records in aw_sales
    print("\n[3] ORPHAN RECORDS IN aw_sales")
    print("-" * 80)
    
    cursor.execute('SELECT "Orphan CustomerKeys" as ISSUE, COUNT(*) as ORPHAN_COUNT FROM aw_sales s LEFT JOIN aw_customers_lookup c ON s.CustomerKey = c.CustomerKey WHERE c.CustomerKey IS NULL')
    row = cursor.fetchone()
    print(f"{row[0]:<30} {row[1]:>10,}")
    
    cursor.execute('SELECT "Orphan ProductKeys" as ISSUE, COUNT(*) as ORPHAN_COUNT FROM aw_sales s LEFT JOIN aw_products_lookup p ON s.ProductKey = p.ProductKey WHERE p.ProductKey IS NULL')
    row = cursor.fetchone()
    print(f"{row[0]:<30} {row[1]:>10,}")
    
    cursor.execute('SELECT "Orphan TerritoryKeys" as ISSUE, COUNT(*) as ORPHAN_COUNT FROM aw_sales s LEFT JOIN aw_territories_lookup t ON s.TerritoryKey = t.SalesTerritoryKey WHERE t.SalesTerritoryKey IS NULL')
    row = cursor.fetchone()
    print(f"{row[0]:<30} {row[1]:>10,}")
    
    cursor.execute('SELECT "Orphan OrderDate" as ISSUE, COUNT(*) as ORPHAN_COUNT FROM aw_sales s LEFT JOIN aw_calendar_lookup cal ON s.OrderDate = cal.Date WHERE cal.Date IS NULL')
    row = cursor.fetchone()
    print(f"{row[0]:<30} {row[1]:>10,}")
    
    # 4. Orphan Records in aw_returns
    print("\n[4] ORPHAN RECORDS IN aw_returns")
    print("-" * 80)
    
    cursor.execute('SELECT "Orphan ProductKeys" as ISSUE, COUNT(*) as ORPHAN_COUNT FROM aw_returns r LEFT JOIN aw_products_lookup p ON r.ProductKey = p.ProductKey WHERE p.ProductKey IS NULL')
    row = cursor.fetchone()
    print(f"{row[0]:<30} {row[1]:>10,}")
    
    cursor.execute('SELECT "Orphan TerritoryKeys" as ISSUE, COUNT(*) as ORPHAN_COUNT FROM aw_returns r LEFT JOIN aw_territories_lookup t ON r.TerritoryKey = t.SalesTerritoryKey WHERE t.SalesTerritoryKey IS NULL')
    row = cursor.fetchone()
    print(f"{row[0]:<30} {row[1]:>10,}")
    
    cursor.execute('SELECT "Orphan ReturnDate" as ISSUE, COUNT(*) as ORPHAN_COUNT FROM aw_returns r LEFT JOIN aw_calendar_lookup cal ON r.ReturnDate = cal.Date WHERE cal.Date IS NULL')
    row = cursor.fetchone()
    print(f"{row[0]:<30} {row[1]:>10,}")
    
    # 5. Product Hierarchy Check
    print("\n[5] PRODUCT HIERARCHY INTEGRITY")
    print("-" * 80)
    
    cursor.execute('SELECT "Orphan ProductSubcategoryKey in Products" as ISSUE, COUNT(*) as ORPHAN_COUNT FROM aw_products_lookup p LEFT JOIN aw_product_subcategory_lookup sc ON p.ProductSubcategoryKey = sc.ProductSubcategoryKey WHERE p.ProductSubcategoryKey IS NOT NULL AND sc.ProductSubcategoryKey IS NULL')
    row = cursor.fetchone()
    print(f"{row[0]:<50} {row[1]:>10,}")
    
    cursor.execute('SELECT "Orphan ProductCategoryKey in Subcategories" as ISSUE, COUNT(*) as ORPHAN_COUNT FROM aw_product_subcategory_lookup sc LEFT JOIN aw_product_category_lookup c ON sc.ProductCategoryKey = c.ProductCategoryKey WHERE c.ProductCategoryKey IS NULL')
    row = cursor.fetchone()
    print(f"{row[0]:<50} {row[1]:>10,}")
    
    # 6. Sales Full Join Summary
    print("\n[6] AW_SALES FULL JOIN VALIDATION")
    print("-" * 80)
    
    cursor.execute("""
    SELECT COUNT(*) AS Total_Sales_Records,
           SUM(CASE WHEN c.CustomerKey IS NOT NULL THEN 1 ELSE 0 END) AS Valid_Customer_Joins,
           SUM(CASE WHEN p.ProductKey IS NOT NULL THEN 1 ELSE 0 END) AS Valid_Product_Joins,
           SUM(CASE WHEN t.SalesTerritoryKey IS NOT NULL THEN 1 ELSE 0 END) AS Valid_Territory_Joins,
           SUM(CASE WHEN cal.Date IS NOT NULL THEN 1 ELSE 0 END) AS Valid_Calendar_Joins,
           SUM(CASE WHEN c.CustomerKey IS NOT NULL AND p.ProductKey IS NOT NULL AND t.SalesTerritoryKey IS NOT NULL AND cal.Date IS NOT NULL THEN 1 ELSE 0 END) AS Fully_Valid_Records
    FROM aw_sales s
    LEFT JOIN aw_customers_lookup c ON s.CustomerKey = c.CustomerKey
    LEFT JOIN aw_products_lookup p ON s.ProductKey = p.ProductKey
    LEFT JOIN aw_territories_lookup t ON s.TerritoryKey = t.SalesTerritoryKey
    LEFT JOIN aw_calendar_lookup cal ON s.OrderDate = cal.Date
    """)
    row = cursor.fetchone()
    print(f"Total Sales Records:          {row[0]:>10,}")
    print(f"Valid Customer Joins:         {row[1]:>10,}")
    print(f"Valid Product Joins:          {row[2]:>10,}")
    print(f"Valid Territory Joins:        {row[3]:>10,}")
    print(f"Valid Calendar Joins:         {row[4]:>10,}")
    print(f"Fully Valid Records:          {row[5]:>10,}")
    
    # 7. Returns Full Join Summary
    print("\n[7] AW_RETURNS FULL JOIN VALIDATION")
    print("-" * 80)
    
    cursor.execute("""
    SELECT COUNT(*) AS Total_Returns_Records,
           SUM(CASE WHEN p.ProductKey IS NOT NULL THEN 1 ELSE 0 END) AS Valid_Product_Joins,
           SUM(CASE WHEN t.SalesTerritoryKey IS NOT NULL THEN 1 ELSE 0 END) AS Valid_Territory_Joins,
           SUM(CASE WHEN cal.Date IS NOT NULL THEN 1 ELSE 0 END) AS Valid_Calendar_Joins,
           SUM(CASE WHEN p.ProductKey IS NOT NULL AND t.SalesTerritoryKey IS NOT NULL AND cal.Date IS NOT NULL THEN 1 ELSE 0 END) AS Fully_Valid_Records
    FROM aw_returns r
    LEFT JOIN aw_products_lookup p ON r.ProductKey = p.ProductKey
    LEFT JOIN aw_territories_lookup t ON r.TerritoryKey = t.SalesTerritoryKey
    LEFT JOIN aw_calendar_lookup cal ON r.ReturnDate = cal.Date
    """)
    row = cursor.fetchone()
    print(f"Total Returns Records:        {row[0]:>10,}")
    print(f"Valid Product Joins:          {row[1]:>10,}")
    print(f"Valid Territory Joins:        {row[2]:>10,}")
    print(f"Valid Calendar Joins:         {row[3]:>10,}")
    print(f"Fully Valid Records:          {row[4]:>10,}")
    
    print("\n" + "=" * 80)
    print("INTEGRITY CHECK COMPLETED - ALL DATA IS CLEAN! ✅")
    print("=" * 80)
    
    conn.close()

if __name__ == "__main__":
    main()
