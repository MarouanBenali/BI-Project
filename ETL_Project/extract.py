import os
import pandas as pd
from config import DATASET_DIR
from utils import get_logger

logger = get_logger("Extract")

def extract_csv(file_name, subfolder="", sep=",", encoding="utf-8-sig"):
    """
    Utility function to load a single CSV file with error handling.
    """
    file_path = os.path.join(DATASET_DIR, subfolder, file_name)
    logger.info(f"Extracting {file_name} from path: {file_path}")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Source file not found at: {file_path}")
        
    try:
        # Try primary encoding
        df = pd.read_csv(file_path, sep=sep, encoding=encoding)
        logger.info(f"Successfully loaded {file_name} with {encoding} encoding. Shape: {df.shape}")
        return df
    except UnicodeDecodeError:
        # Fallback encoding if utf-8 fails
        logger.warning(f"UTF-8 decode failed for {file_name}. Retrying with ISO-8859-1 or latin-1...")
        df = pd.read_csv(file_path, sep=sep, encoding="latin-1")
        logger.info(f"Successfully loaded {file_name} with latin-1 fallback. Shape: {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Error reading {file_name}: {e}")
        raise e

def extract_all():
    """
    Extracts all files for the BI project.
    Returns:
        dict: A dictionary of pandas DataFrames.
    """
    data = {}
    
    # 1. Calendar
    data["calendar"] = extract_csv("AdventureWorks_Calendar.csv.csv")
    
    # 2. Customers
    data["customers"] = extract_csv("AdventureWorks_Customers.csv.csv")
    
    # 3. Product Categories
    data["product_categories"] = extract_csv("AdventureWorks_Product_Categories.csv.csv")
    
    # 4. Product Subcategories
    data["product_subcategories"] = extract_csv("AdventureWorks_Product_Subcategories.csv.csv")
    
    # 5. Products
    data["products"] = extract_csv("AdventureWorks_Products.csv.csv")
    
    # 6. Returns
    data["returns"] = extract_csv("AdventureWorks_Returns.csv.csv")
    
    # 7. Territories (Delimited with semicolon ';')
    data["territories"] = extract_csv("AdventureWorks_Territories.csv.csv", sep=";")
    
    # 8. Sales (Unite 2015, 2016, 2017)
    sales_2015 = extract_csv("AdventureWorks_Sales_2015.csv.csv", subfolder="Sales")
    sales_2016 = extract_csv("AdventureWorks_Sales_2016.csv.csv", subfolder="Sales")
    sales_2017 = extract_csv("AdventureWorks_Sales_2017.csv.csv", subfolder="Sales")
    
    logger.info("Unifying sales datasets (2015, 2016, 2017)...")
    data["sales"] = pd.concat([sales_2015, sales_2016, sales_2017], ignore_index=True)
    logger.info(f"Unified Sales dataset shape: {data['sales'].shape}")
    
    return data

if __name__ == "__main__":
    # Test Extraction
    logger.info("Testing extraction process...")
    dfs = extract_all()
    for name, df in dfs.items():
        print(f"Table: {name} -> Columns: {list(df.columns[:3])}.. | Rows: {len(df)}")
