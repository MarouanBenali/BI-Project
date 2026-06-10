"""
Data Integrity Validation Script
Runs comprehensive checks on the AdventureWorks Datawarehouse
"""

import pymysql
import pandas as pd
from config import DATABASE_URI
import time
from utils import get_logger

logger = get_logger("IntegrityChecker")

def get_db_connection():
    """Establish database connection"""
    from sqlalchemy import create_engine
    engine = create_engine(DATABASE_URI)
    return engine

def run_integrity_checks():
    """Run all integrity checks and generate report"""
    logger.info("=" * 80)
    logger.info("STARTING DATA INTEGRITY CHECKS")
    logger.info("=" * 80)
    
    engine = get_db_connection()
    
    # Read the integrity checks SQL file
    with open('../data_integrity_checks.sql', 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Execute the script and capture results
    import mysql.connector
    from config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME
    
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=int(DB_PORT),
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        charset='utf8mb4'
    )
    
    cursor = conn.cursor()
    
    # Split the SQL content by statements (simple split on semicolon)
    statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
    
    results = []
    
    for stmt in statements:
        if stmt.upper().startswith('SELECT'):
            try:
                cursor.execute(stmt)
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                if rows:
                    df = pd.DataFrame(rows, columns=columns)
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
