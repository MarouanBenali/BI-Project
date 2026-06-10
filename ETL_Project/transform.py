import pandas as pd
import datetime
from utils import get_logger, capitalize_each_word, extract_sku, extract_sku_category

logger = get_logger("Transform")

def transform_customers(df_cust):
    """
    Transforms raw customers data to match aw_customers_lookup schema.
    """
    logger.info("Transforming Customers dataset...")
    df = df_cust.copy()
    
    # 1. Drop duplicates by primary key
    df = df.drop_duplicates(subset=["CustomerKey"]).dropna(subset=["CustomerKey"])
    df["CustomerKey"] = df["CustomerKey"].astype(int)
    
    # 2. Re-create FullName: Merge Prefix, FirstName, LastName and apply Title Capitalization
    def make_fullname(row):
        prefix = str(row["Prefix"]).strip() if pd.notna(row["Prefix"]) else ""
        first = str(row["FirstName"]).strip() if pd.notna(row["FirstName"]) else ""
        last = str(row["LastName"]).strip() if pd.notna(row["LastName"]) else ""
        # Filter out "nan" strings that might arise from casting
        prefix = "" if prefix.lower() == "nan" else prefix
        first = "" if first.lower() == "nan" else first
        last = "" if last.lower() == "nan" else last
        return f"{prefix} {first} {last}".strip()
        
    df["FullName"] = df.apply(make_fullname, axis=1)
    df["FullName"] = df["FullName"].apply(capitalize_each_word)
    
    # 3. Handle EmailAddress, UserName, and Domain
    df["EmailAddress"] = df["EmailAddress"].fillna("").astype(str).str.strip()
    df["UserName"] = df["EmailAddress"].apply(lambda email: email.split("@")[0] if "@" in email else "")
    
    def extract_domain(email):
        if "@" in email:
            domain_part = email.split("@")[1].split(".")[0]
            domain_part = domain_part.replace("-", " ")
            return capitalize_each_word(domain_part)
        return ""
        
    df["Domain"] = df["EmailAddress"].apply(extract_domain)
    
    # 4. Handle AnnualIncome and IncomeLevel
    # Clean non-digits (remove currency symbols, commas, spaces)
    df["AnnualIncome"] = df["AnnualIncome"].astype(str).str.replace(r"\D", "", regex=True)
    df["AnnualIncome"] = pd.to_numeric(df["AnnualIncome"], errors="coerce").fillna(0).astype(int)
    
    def get_income_level(income):
        if income >= 150000:
            return "Very High"
        elif income >= 100000:
            return "High"
        elif income >= 50000:
            return "Average"
        else:
            return "Low"
            
    df["IncomeLevel"] = df["AnnualIncome"].apply(get_income_level)
    
    # 5. Handle BirthDate, BirthYear, CurrentAge
    df["BirthDate"] = pd.to_datetime(df["BirthDate"], errors="coerce")
    current_year = datetime.datetime.now().year
    
    df["BirthYear"] = df["BirthDate"].dt.year
    # Handle NaN values for BirthYear
    df["BirthYear"] = df["BirthYear"].fillna(1900).astype(int)
    
    df["CurrentAge"] = current_year - df["BirthYear"]
    # If birthdate was missing, set CurrentAge to 0
    df.loc[df["BirthDate"].isna(), "CurrentAge"] = 0
    
    # Format BirthDate as string date YYYY-MM-DD or keep as datetime.date for DB load
    df["BirthDate"] = df["BirthDate"].dt.date
    
    # 6. Derived columns: Parent, CustomerPriority
    df["TotalChildren"] = pd.to_numeric(df["TotalChildren"], errors="coerce").fillna(0).astype(int)
    df["Parent"] = df["TotalChildren"].apply(lambda tc: "Yes" if tc > 0 else "No")
    
    def get_priority(row):
        if row["CurrentAge"] < 50 and row["AnnualIncome"] > 100000:
            return "Priority"
        return "Standard"
        
    df["CustomerPriority"] = df.apply(get_priority, axis=1)
    
    # 7. Format columns to match database schema
    schema_cols = [
        "CustomerKey", "Prefix", "FirstName", "LastName", "BirthDate", "MaritalStatus",
        "Gender", "EmailAddress", "AnnualIncome", "TotalChildren", "EducationLevel",
        "Occupation", "HomeOwner", "FullName", "UserName", "Domain", "IncomeLevel",
        "BirthYear", "CurrentAge", "Parent", "CustomerPriority"
    ]
    
    # Standardize types and fill nulls safely
    for col in ["Prefix", "FirstName", "LastName", "MaritalStatus", "Gender", "EducationLevel", "Occupation", "HomeOwner"]:
        df[col] = df[col].fillna("").astype(str).str.strip()
        
    df = df[schema_cols]
    logger.info(f"Customers transformation complete. Shape: {df.shape}")
    return df

def transform_products(df_prod):
    """
    Transforms products dataset to match aw_products_lookup schema.
    """
    logger.info("Transforming Products dataset...")
    df = df_prod.copy()
    
    df = df.drop_duplicates(subset=["ProductKey"]).dropna(subset=["ProductKey"])
    df["ProductKey"] = df["ProductKey"].astype(int)
    df["ProductSubcategoryKey"] = pd.to_numeric(df["ProductSubcategoryKey"], errors="coerce").fillna(0).astype(int)
    
    # Apply custom SKU functions
    df["ProductSKU"] = df["ProductSKU"].fillna("").astype(str).str.strip()
    df["SKUType"] = df["ProductSKU"].apply(extract_sku)
    df["SKUCategory"] = df["ProductSKU"].apply(extract_sku_category)
    
    # Calculations
    df["ProductPrice"] = pd.to_numeric(df["ProductPrice"], errors="coerce").fillna(0.0)
    df["ProductCost"] = pd.to_numeric(df["ProductCost"], errors="coerce").fillna(0.0)
    df["DiscountPrice"] = (df["ProductPrice"] * 0.85).round(4)
    
    def get_price_point(price):
        if price > 500:
            return "High"
        elif price > 100:
            return "Mid-Range"
        else:
            return "Low"
            
    df["PricePoint"] = df["ProductPrice"].apply(get_price_point)
    
    # Standardize string fields
    for col in ["ProductName", "ModelName", "ProductDescription", "ProductColor", "ProductStyle"]:
        df[col] = df[col].fillna("").astype(str).str.strip()
        
    schema_cols = [
        "ProductKey", "ProductSubcategoryKey", "ProductSKU", "ProductName", "ModelName",
        "ProductDescription", "ProductColor", "ProductStyle", "ProductCost", "ProductPrice",
        "SKUType", "DiscountPrice", "PricePoint", "SKUCategory"
    ]
    df = df[schema_cols]
    logger.info(f"Products transformation complete. Shape: {df.shape}")
    return df

def transform_calendar(df_cal):
    """
    Transforms calendar dataset to match aw_calendar_lookup schema.
    """
    logger.info("Transforming Calendar dataset...")
    df = df_cal.copy()
    
    # Standardize Date column
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    
    # 1. Start of Month & Start of Year
    df["StartOfMonth"] = df["Date"].dt.to_period("M").dt.to_timestamp().dt.date
    df["StartOfYear"] = df["Date"].dt.to_period("Y").dt.to_timestamp().dt.date
    
    # 2. Year & Month Hierarchy
    df["Year"] = df["Date"].dt.year.astype(int)
    
    # 3. Day of Week (Monday=1, ..., Sunday=7)
    df["DayOfWeek"] = df["Date"].dt.dayofweek + 1
    
    # 4. Weekend Flag
    df["Weekend"] = df["DayOfWeek"].apply(lambda dow: "Yes" if dow in [6, 7] else "No")
    
    # 5. Month & Day Names
    df["MonthName"] = df["Date"].dt.strftime("%B")
    df["DayName"] = df["Date"].dt.strftime("%A")
    
    # 6. Short Month & Short Day (First 3 chars)
    df["ShortMonth"] = df["MonthName"].str[:3]
    df["ShortDay"] = df["DayName"].str[:3]
    
    # Format Date back to string/date for load
    df["Date"] = df["Date"].dt.date
    
    schema_cols = [
        "Date", "StartOfMonth", "MonthName", "StartOfYear", "Year", "DayOfWeek",
        "Weekend", "ShortMonth", "ShortDay", "DayName"
    ]
    df = df[schema_cols]
    
    # Ensure distinct calendar rows
    df = df.drop_duplicates(subset=["Date"])
    logger.info(f"Calendar transformation complete. Shape: {df.shape}")
    return df

def transform_sales(df_sales, df_cust, df_prod, df_terr):
    """
    Transforms sales dataset to match aw_sales schema and ensures referential integrity.
    """
    logger.info("Transforming Sales Fact dataset...")
    df = df_sales.copy()
    
    # 1. Clean dates
    df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
    df["StockDate"] = pd.to_datetime(df["StockDate"], errors="coerce")
    df = df.dropna(subset=["OrderDate", "ProductKey", "CustomerKey"])
    
    # 2. Keys parsing
    df["ProductKey"] = df["ProductKey"].astype(int)
    df["CustomerKey"] = df["CustomerKey"].astype(int)
    df["TerritoryKey"] = df["TerritoryKey"].astype(int)
    df["OrderLineItem"] = df["OrderLineItem"].astype(int)
    df["OrderQuantity"] = df["OrderQuantity"].astype(int)
    
    # 3. Quantity Type
    df["QuantityType"] = df["OrderQuantity"].apply(lambda q: "Multiple Items" if q > 1 else "Single Item")
    
    df["OrderDate"] = df["OrderDate"].dt.date
    df["StockDate"] = df["StockDate"].dt.date
    
    schema_cols = [
        "OrderDate", "StockDate", "OrderNumber", "ProductKey", "CustomerKey",
        "TerritoryKey", "OrderLineItem", "OrderQuantity", "QuantityType"
    ]
    df = df[schema_cols]
    
    # 4. Referential Integrity Checks
    logger.info("Enforcing referential integrity on Sales Fact table...")
    
    initial_rows = len(df)
    valid_products = set(df_prod["ProductKey"])
    valid_customers = set(df_cust["CustomerKey"])
    valid_territories = set(df_terr["SalesTerritoryKey"])
    
    mismatched_prod = df[~df["ProductKey"].isin(valid_products)]
    mismatched_cust = df[~df["CustomerKey"].isin(valid_customers)]
    mismatched_terr = df[~df["TerritoryKey"].isin(valid_territories)]
    
    if len(mismatched_prod) > 0:
        logger.warning(f"Found {len(mismatched_prod)} sales rows with unknown ProductKeys! Filtering them out.")
    if len(mismatched_cust) > 0:
        logger.warning(f"Found {len(mismatched_cust)} sales rows with unknown CustomerKeys! Filtering them out.")
    if len(mismatched_terr) > 0:
        logger.warning(f"Found {len(mismatched_terr)} sales rows with unknown TerritoryKeys! Filtering them out.")
        
    df = df[
        df["ProductKey"].isin(valid_products) & 
        df["CustomerKey"].isin(valid_customers) & 
        df["TerritoryKey"].isin(valid_territories)
    ]
    
    logger.info(f"Sales Fact transformation complete. Final Rows: {len(df)} (Dropped {initial_rows - len(df)} invalid rows)")
    return df

def transform_returns(df_ret, df_prod, df_terr):
    """
    Transforms returns dataset to match aw_returns schema and ensures referential integrity.
    """
    logger.info("Transforming Returns Fact dataset...")
    df = df_ret.copy()
    
    df["ReturnDate"] = pd.to_datetime(df["ReturnDate"], errors="coerce")
    df = df.dropna(subset=["ReturnDate", "ProductKey", "TerritoryKey"])
    
    df["ProductKey"] = df["ProductKey"].astype(int)
    df["TerritoryKey"] = df["TerritoryKey"].astype(int)
    df["ReturnQuantity"] = df["ReturnQuantity"].astype(int)
    
    df["ReturnDate"] = df["ReturnDate"].dt.date
    
    schema_cols = ["ReturnDate", "TerritoryKey", "ProductKey", "ReturnQuantity"]
    df = df[schema_cols]
    
    # Referential integrity check
    logger.info("Enforcing referential integrity on Returns Fact table...")
    initial_rows = len(df)
    valid_products = set(df_prod["ProductKey"])
    valid_territories = set(df_terr["SalesTerritoryKey"])
    
    df = df[
        df["ProductKey"].isin(valid_products) & 
        df["TerritoryKey"].isin(valid_territories)
    ]
    logger.info(f"Returns Fact transformation complete. Final Rows: {len(df)} (Dropped {initial_rows - len(df)} invalid rows)")
    return df

def transform_territories(df_terr):
    """
    Transforms territories to match aw_territories_lookup schema.
    """
    logger.info("Transforming Territories lookup...")
    df = df_terr.copy()
    df = df.drop_duplicates(subset=["SalesTerritoryKey"]).dropna(subset=["SalesTerritoryKey"])
    df["SalesTerritoryKey"] = df["SalesTerritoryKey"].astype(int)
    
    for col in ["Region", "Country", "Continent"]:
        df[col] = df[col].fillna("").astype(str).str.strip()
        
    df = df[["SalesTerritoryKey", "Region", "Country", "Continent"]]
    return df

def transform_product_categories(df_cat):
    """
    Transforms categories dataset.
    """
    logger.info("Transforming Product Categories lookup...")
    df = df_cat.copy()
    df = df.drop_duplicates(subset=["ProductCategoryKey"]).dropna(subset=["ProductCategoryKey"])
    df["ProductCategoryKey"] = df["ProductCategoryKey"].astype(int)
    df["CategoryName"] = df["CategoryName"].fillna("").astype(str).str.strip()
    return df[["ProductCategoryKey", "CategoryName"]]

def transform_product_subcategories(df_subcat):
    """
    Transforms subcategories dataset.
    """
    logger.info("Transforming Product Subcategories lookup...")
    df = df_subcat.copy()
    df = df.drop_duplicates(subset=["ProductSubcategoryKey"]).dropna(subset=["ProductSubcategoryKey"])
    df["ProductSubcategoryKey"] = df["ProductSubcategoryKey"].astype(int)
    df["ProductCategoryKey"] = df["ProductCategoryKey"].astype(int)
    df["SubcategoryName"] = df["SubcategoryName"].fillna("").astype(str).str.strip()
    return df[["ProductSubcategoryKey", "SubcategoryName", "ProductCategoryKey"]]


def transform_all(extracted_data):
    """
    Transforms all extracted dataframes recursively.
    """
    transformed = {}
    
    # 1. Base Dimensions first (independent dimensions)
    transformed["aw_territories_lookup"] = transform_territories(extracted_data["territories"])
    transformed["aw_product_category_lookup"] = transform_product_categories(extracted_data["product_categories"])
    transformed["aw_product_subcategory_lookup"] = transform_product_subcategories(extracted_data["product_subcategories"])
    transformed["aw_calendar_lookup"] = transform_calendar(extracted_data["calendar"])
    
    # 2. Dependent Dimensions (e.g. Products depends on Subcategories, Customers is independent)
    transformed["aw_customers_lookup"] = transform_customers(extracted_data["customers"])
    transformed["aw_products_lookup"] = transform_products(extracted_data["products"])
    
    # 3. Fact Tables (depends on dimensions for referential integrity checks)
    transformed["aw_sales"] = transform_sales(
        extracted_data["sales"],
        transformed["aw_customers_lookup"],
        transformed["aw_products_lookup"],
        transformed["aw_territories_lookup"]
    )
    
    transformed["aw_returns"] = transform_returns(
        extracted_data["returns"],
        transformed["aw_products_lookup"],
        transformed["aw_territories_lookup"]
    )
    
    return transformed
