import os

# Central Configuration for Python ETL Pipeline

# 1. Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "Dataset")

# 2. Database Connection Credentials
# These can be overridden using environment variables
DB_DIALECT = "mysql+pymysql"
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASS = os.environ.get("DB_PASS", "")  # Adjust based on your local MySQL password
DB_NAME = os.environ.get("DB_NAME", "aw_datawarehouse")

# Construct Connection String
DATABASE_URI = f"{DB_DIALECT}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# 3. ETL Job Constants
CHUNK_SIZE = 5000  # For bulk loading batching
LOG_FILE = os.path.join(BASE_DIR, "etl_pipeline.log")
LOG_LEVEL = "INFO"
