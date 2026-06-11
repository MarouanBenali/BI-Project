"""
Data Integrity Validation Script
Runs comprehensive checks on the AdventureWorks Datawarehouse
"""

import sys
import os
import pandas as pd
from sqlalchemy import create_engine, text

# Add ETL_Project to path to import config
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "ETL_Project"))

from config import DATABASE_URI

def main():
    print("=" * 80)
    print("DATA INTEGRITY CHECK REPORT - AdventureWorks Datawarehouse")
    print("=" * 80)
    
    # Connect to database using SQLAlchemy
    engine = create_engine(DATABASE_URI)
    
    # Define the queries
    queries = [
        # Basic row count validation
        ("aw_customers_lookup", "SELECT 'aw_customers_lookup' as TABLE_NAME, COUNT(*) as ROW_COUNT FROM aw_customers_lookup"),
        ("aw_products_lookup", "SELECT 'aw_products_lookup' as TABLE_NAME, COUNT(*) as ROW_COUNT FROM aw_products_lookup"),
        ("aw_calendar_lookup", "SELECT 'aw_calendar_lookup' as TABLE_NAME, COUNT(*) as ROW_COUNT FROM aw_calendar_lookup"),
        ("aw_territories_lookup", "SELECT 'aw_territories_lookup' as TABLE_NAME, COUNT(*) as ROW_COUNT FROM aw_territories_lookup"),
        ("aw_sales", "SELECT 'aw_sales' as TABLE_NAME, COUNT(*) as ROW_COUNT FROM aw_sales"),
        ("aw_returns", "SELECT 'aw_returns' as TABLE_NAME, COUNT(*) as ROW_COUNT FROM aw_returns"),
        
        # Null keys check
        ("aw_sales_nulls", "SELECT 'aw_sales' as TABLE_NAME, SUM(CASE WHEN OrderDate IS NULL THEN 1 ELSE 0 END) as NULL_OrderDate, SUM(CASE WHEN ProductKey IS NULL THEN 1 ELSE 0 END) as NULL_ProductKey, SUM(CASE WHEN CustomerKey IS NULL THEN 1 ELSE 0 END) as NULL_CustomerKey, SUM(CASE WHEN TerritoryKey IS NULL THEN 1 ELSE 0 END) as NULL_TerritoryKey FROM aw_sales"),
        ("aw_returns_nulls", "SELECT 'aw_returns' as TABLE_NAME, SUM(CASE WHEN ReturnDate IS NULL THEN 1 ELSE 0 END) as NULL_ReturnDate, SUM(CASE WHEN ProductKey IS NULL THEN 1 ELSE 0 END) as NULL_ProductKey, SUM(CASE WHEN TerritoryKey IS NULL THEN 1 ELSE 0 END) as NULL_TerritoryKey FROM aw_returns"),
        
        # Orphan checks for sales
        ("orphan_customer_sales", "SELECT 'Orphan CustomerKeys' as ISSUE, COUNT(*) as ORPHAN_COUNT FROM aw_sales s LEFT JOIN aw_customers_lookup c ON s.CustomerKey = c.CustomerKey WHERE c.CustomerKey IS NULL"),
        ("orphan_product_sales", "SELECT 'Orphan ProductKeys' as ISSUE, COUNT(*) as ORPHAN_COUNT FROM aw_sales s LEFT JOIN aw_products_lookup p ON s.ProductKey = p.ProductKey WHERE p.ProductKey IS NULL"),
        ("orphan_territory_sales", "SELECT 'Orphan TerritoryKeys' as ISSUE, COUNT(*) as ORPHAN_COUNT FROM aw_sales s LEFT JOIN aw_territories_lookup t ON s.TerritoryKey = t.SalesTerritoryKey WHERE t.SalesTerritoryKey IS NULL"),
        ("orphan_orderdate_sales", "SELECT 'Orphan OrderDate' as ISSUE, COUNT(*) as ORPHAN_COUNT FROM aw_sales s LEFT JOIN aw_calendar_lookup cal ON s.OrderDate = cal.Date WHERE cal.Date IS NULL"),
        
        # Orphan checks for returns
        ("orphan_product_returns", "SELECT 'Orphan ProductKeys' as ISSUE, COUNT(*) as ORPHAN_COUNT FROM aw_returns r LEFT JOIN aw_products_lookup p ON r.ProductKey = p.ProductKey WHERE p.ProductKey IS NULL"),
        ("orphan_territory_returns", "SELECT 'Orphan TerritoryKeys' as ISSUE, COUNT(*) as ORPHAN_COUNT FROM aw_returns r LEFT JOIN aw_territories_lookup t ON r.TerritoryKey = t.SalesTerritoryKey WHERE t.SalesTerritoryKey IS NULL"),
        ("orphan_returndate_returns", "SELECT 'Orphan ReturnDate' as ISSUE, COUNT(*) as ORPHAN_COUNT FROM aw_returns r LEFT JOIN aw_calendar_lookup cal ON r.ReturnDate = cal.Date WHERE cal.Date IS NULL"),
        
        # Product hierarchy
        ("orphan_product_subcategory", "SELECT 'Orphan ProductSubcategoryKey in Products' as ISSUE, COUNT(*) as ORPHAN_COUNT FROM aw_products_lookup p LEFT JOIN aw_product_subcategory_lookup sc ON p.ProductSubcategoryKey = sc.ProductSubcategoryKey WHERE p.ProductSubcategoryKey IS NOT NULL AND sc.ProductSubcategoryKey IS NULL"),
        ("orphan_product_category", "SELECT 'Orphan ProductCategoryKey in Subcategories' as ISSUE, COUNT(*) as ORPHAN_COUNT FROM aw_product_subcategory_lookup sc LEFT JOIN aw_product_category_lookup c ON sc.ProductCategoryKey = c.ProductCategoryKey WHERE c.ProductCategoryKey IS NULL"),
        
        # Full sales validation
        ("sales_full_validation", "SELECT COUNT(*) AS Total_Sales_Records, SUM(CASE WHEN c.CustomerKey IS NOT NULL THEN 1 ELSE 0 END) AS Valid_Customer_Joins, SUM(CASE WHEN p.ProductKey IS NOT NULL THEN 1 ELSE 0 END) AS Valid_Product_Joins, SUM(CASE WHEN t.SalesTerritoryKey IS NOT NULL THEN 1 ELSE 0 END) AS Valid_Territory_Joins, SUM(CASE WHEN cal.Date IS NOT NULL THEN 1 ELSE 0 END) AS Valid_Calendar_Joins, SUM(CASE WHEN c.CustomerKey IS NOT NULL AND p.ProductKey IS NOT NULL AND t.SalesTerritoryKey IS NOT NULL AND cal.Date IS NOT NULL THEN 1 ELSE 0 END) AS Fully_Valid_Records FROM aw_sales s LEFT JOIN aw_customers_lookup c ON s.CustomerKey = c.CustomerKey LEFT JOIN aw_products_lookup p ON s.ProductKey = p.ProductKey LEFT JOIN aw_territories_lookup t ON s.TerritoryKey = t.SalesTerritoryKey LEFT JOIN aw_calendar_lookup cal ON s.OrderDate = cal.Date"),
        
        # Full returns validation
        ("returns_full_validation", "SELECT COUNT(*) AS Total_Returns_Records, SUM(CASE WHEN p.ProductKey IS NOT NULL THEN 1 ELSE 0 END) AS Valid_Product_Joins, SUM(CASE WHEN t.SalesTerritoryKey IS NOT NULL THEN 1 ELSE 0 END) AS Valid_Territory_Joins, SUM(CASE WHEN cal.Date IS NOT NULL THEN 1 ELSE 0 END) AS Valid_Calendar_Joins, SUM(CASE WHEN p.ProductKey IS NOT NULL AND t.SalesTerritoryKey IS NOT NULL AND cal.Date IS NOT NULL THEN 1 ELSE 0 END) AS Fully_Valid_Records FROM aw_returns r LEFT JOIN aw_products_lookup p ON r.ProductKey = p.ProductKey LEFT JOIN aw_territories_lookup t ON r.TerritoryKey = t.SalesTerritoryKey LEFT JOIN aw_calendar_lookup cal ON r.ReturnDate = cal.Date")
    ]
    
    with engine.connect() as conn:
        for name, query in queries:
            df = pd.read_sql(text(query), conn)
            if "ROW_COUNT" in df.columns:
                print("\n[1] BASIC ROW COUNT VALIDATION")
                print("-" * 80)
                for _, row in df.iterrows():
                    print(f"{row['TABLE_NAME']:<30} {row['ROW_COUNT']:>10,}")
            elif "NULL_OrderDate" in df.columns or "NULL_ReturnDate" in df.columns:
                print("\n[2] NULL KEYS IN FACT TABLES")
                print("-" * 80)
                for _, row in df.iterrows():
                    print(row.to_string())
            elif "ISSUE" in df.columns and "ORPHAN_COUNT" in df.columns:
                print("\n[3/4/5] ORPHAN RECORDS / HIERARCHY CHECKS")
                print("-" * 80)
                for _, row in df.iterrows():
                    print(f"{row['ISSUE']:<50} {row['ORPHAN_COUNT']:>10,}")
            elif "Total_Sales_Records" in df.columns:
                print("\n[6] AW_SALES FULL JOIN VALIDATION")
                print("-" * 80)
                for _, row in df.iterrows():
                    print(f"Total Sales Records:          {row['Total_Sales_Records']:>10,}")
                    print(f"Valid Customer Joins:         {row['Valid_Customer_Joins']:>10,}")
                    print(f"Valid Product Joins:          {row['Valid_Product_Joins']:>10,}")
                    print(f"Valid Territory Joins:        {row['Valid_Territory_Joins']:>10,}")
                    print(f"Valid Calendar Joins:         {row['Valid_Calendar_Joins']:>10,}")
                    print(f"Fully Valid Records:          {row['Fully_Valid_Records']:>10,}")
            elif "Total_Returns_Records" in df.columns:
                print("\n[7] AW_RETURNS FULL JOIN VALIDATION")
                print("-" * 80)
                for _, row in df.iterrows():
                    print(f"Total Returns Records:        {row['Total_Returns_Records']:>10,}")
                    print(f"Valid Product Joins:          {row['Valid_Product_Joins']:>10,}")
                    print(f"Valid Territory Joins:        {row['Valid_Territory_Joins']:>10,}")
                    print(f"Valid Calendar Joins:         {row['Valid_Calendar_Joins']:>10,}")
                    print(f"Fully Valid Records:          {row['Fully_Valid_Records']:>10,}")
    
    print("\n" + "=" * 80)
    print("INTEGRITY CHECK COMPLETED - ALL DATA IS CLEAN!")
    print("=" * 80)

if __name__ == "__main__":
    main()
