from sqlalchemy import create_engine, text
from config import DATABASE_URI, CHUNK_SIZE
from utils import get_logger

logger = get_logger("Load")

def get_db_engine():
    """
    Creates and returns an SQLAlchemy database engine.
    """
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

def clear_table(table_name, engine):
    """
    Empties the target table using TRUNCATE (or DELETE if FK checks restrict TRUNCATE).
    This preserves the predefined schema, indexes, and primary keys.
    """
    logger.info(f"Clearing existing data from table: {table_name}")
    with engine.begin() as conn:
        try:
            # Disable foreign key checks temporarily to allow truncating
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
            conn.execute(text(f"TRUNCATE TABLE `{table_name}`;"))
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
            logger.info(f"Table {table_name} truncated successfully.")
        except Exception as e:
            # Fallback to DELETE if TRUNCATE fails
            logger.warning(f"TRUNCATE failed for {table_name}: {e}. Falling back to DELETE...")
            try:
                conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
                conn.execute(text(f"DELETE FROM `{table_name}`;"))
                conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
                logger.info(f"Table {table_name} data deleted successfully.")
            except Exception as e_del:
                logger.error(f"Failed to clear table {table_name}: {e_del}")
                raise e_del

def load_data(transformed_data, engine):
    """
    Loads all transformed dataframes into their respective MySQL tables.
    """
    # Order of tables to load: independent lookups first, then dependent, then facts
    load_order = [
        "aw_territories_lookup",
        "aw_product_category_lookup",
        "aw_product_subcategory_lookup",
        "aw_calendar_lookup",
        "aw_customers_lookup",
        "aw_products_lookup",
        "aw_sales",
        "aw_returns"
    ]
    
    logger.info("Beginning the database loading phase...")
    
    for table_name in load_order:
        if table_name not in transformed_data:
            logger.warning(f"Table {table_name} not found in transformed data. Skipping.")
            continue
            
        df = transformed_data[table_name]
        logger.info(f"Loading {len(df)} records into table `{table_name}`...")
        
        try:
            # Clear table first to preserve schema constraints but overwrite data
            clear_table(table_name, engine)
            
            # Load data using pandas bulk upload (without method='multi' to avoid max_allowed_packet crashes)
            df.to_sql(
                name=table_name,
                con=engine,
                if_exists="append",
                index=False,
                chunksize=CHUNK_SIZE
            )
            logger.info(f"Successfully loaded `{table_name}` table.")
        except Exception as e:
            logger.error(f"Error loading table {table_name}: {e}")
            raise e
            
    logger.info("Loading phase completed successfully.")
