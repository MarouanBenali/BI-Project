"""
Data Integrity Validation Script
Runs comprehensive checks on the AdventureWorks Datawarehouse
"""

import pandas as pd
from sqlalchemy import create_engine, text
from config import DATABASE_URI
from utils import get_logger
import sys
import os

# Add parent directory for imports (if running from ETL_Project/)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = get_logger("IntegrityChecker")

def get_db_engine():
    """Establish database connection using SQLAlchemy"""
    logger.info("Initializing database connection engine...")
    try:
        engine = create_engine(DATABASE_URI)
        # Verify connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection established successfully.")
        return engine
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        raise e

def run_integrity_checks():
    """Run all integrity checks and generate report"""
    logger.info("=" * 80)
    logger.info("STARTING DATA INTEGRITY CHECKS")
    logger.info("=" * 80)
    
    engine = get_db_engine()
    
    # Read the integrity checks SQL file
    sql_file_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
        "data_integrity_checks.sql"
    )
    
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    results = []
    
    with engine.connect() as conn:
        # Split the SQL content by statements (simple split on semicolon)
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        for stmt in statements:
            if stmt.upper().startswith('SELECT'):
                try:
                    df = pd.read_sql(text(stmt), conn)
                    if len(df) > 0:
                        results.append((stmt[:100] + "...", df))
                except Exception as e:
                    logger.warning(f"Could not execute statement: {e}")
    
    # Print summary report
    print("\n" + "=" * 80)
    print("DATA INTEGRITY CHECK REPORT")
    print("=" * 80)
    
    # Print results
    for desc, df in results:
        print("\n" + "-" * 80)
        print(desc)
        print("-" * 80)
        print(df.to_string(index=False))
    
    return results

if __name__ == "__main__":
    run_integrity_checks()
