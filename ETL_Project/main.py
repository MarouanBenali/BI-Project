import time
from extract import extract_all
from transform import transform_all
from load import get_db_engine, load_data
from utils import get_logger

logger = get_logger("Orchestrator")

def run_pipeline():
    """
    Main entry point for running the complete Python ETL pipeline.
    """
    logger.info("==============================================")
    logger.info("  STARTING PYTHON ETL PIPELINE REPLACEMENT    ")
    logger.info("==============================================")
    
    start_time = time.time()
    
    try:
        # Step 1: Extraction
        extract_start = time.time()
        logger.info("[ETL PHASE 1/3] Extracting raw files...")
        raw_data = extract_all()
        extract_duration = time.time() - extract_start
        logger.info(f"Extraction completed in {extract_duration:.2f} seconds.")
        
        # Step 2: Transformation
        transform_start = time.time()
        logger.info("[ETL PHASE 2/3] Transforming datasets...")
        transformed_data = transform_all(raw_data)
        transform_duration = time.time() - transform_start
        logger.info(f"Transformation completed in {transform_duration:.2f} seconds.")
        
        # Step 3: Loading
        load_start = time.time()
        logger.info("[ETL PHASE 3/3] Loading processed data to MySQL...")
        engine = get_db_engine()
        load_data(transformed_data, engine)
        load_duration = time.time() - load_start
        logger.info(f"Loading completed in {load_duration:.2f} seconds.")
        
        total_duration = time.time() - start_time
        logger.info("==============================================")
        logger.info("  ETL PIPELINE RUN COMPLETED SUCCESSFULLY!    ")
        logger.info(f"  Total execution time: {total_duration:.2f} seconds.")
        logger.info("==============================================")
        
    except Exception as e:
        logger.critical("ETL Pipeline execution failed!", exc_info=True)
        print(f"\n[CRITICAL ERROR] ETL Pipeline failed: {e}")
        exit(1)

if __name__ == "__main__":
    run_pipeline()
