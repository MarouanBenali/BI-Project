# Python ETL Pipeline (Talend Replacement)

This project is a complete, modular, and production-oriented Python-based ETL pipeline designed to replace Talend/Pentaho for the AdventureWorks Business Intelligence DWH. It extracts raw CSV datasets, performs cleanings and transformations, and loads them into a MySQL data warehouse schema for Power BI reporting.

## Project Structure

```
ETL_Project/
 ├── config.py         # Environment configurations, paths, and database settings
 ├── extract.py        # Ingestion of source CSV files with fallback encoding
 ├── transform.py      # DWH dimensional modeling and transformations
 ├── load.py           # Database connection and bulk load loading routines
 ├── utils.py          # SKU parsing, capitalization routines, and logging utilities
 ├── main.py           # Orchestration layer (Extract -> Transform -> Load)
 ├── requirements.txt  # Python package dependencies
 └── README.md         # Documentation
```

---

## Technical Features

1. **Extract**: Loads multiple CSV files from the `Dataset/` folder, dynamically resolving delimiters (comma for files, semicolon for territories) and encoding types.
2. **Transform**:
   - **Customers Lookup**: Concatenates prefix and names with title-case capitalization, computes `Age` and `BirthYear`, derives `IncomeLevel`, checks if parent (`Parent`), and calculates `CustomerPriority`.
   - **Products Lookup**: Re-computes `DiscountPrice` (15% off list price), `PricePoint` tier ("High", "Mid-Range", "Low"), and extracts standard SKU code and SKU category using string manipulation.
   - **Calendar Lookup**: Generates start of month, start of year, English month/day names, short forms, and weekend classification flags.
   - **Sales Fact Table**: Consolidates 2015, 2016, and 2017 files, computes `QuantityType` ("Single Item" or "Multiple Items"), and filters out rows that fail referential integrity checks (invalid keys).
   - **Returns Fact Table**: Filters out records failing foreign key integrity tests.
3. **Load**: Establishes database connection using SQLAlchemy + PyMySQL, truncates tables to preserve pre-configured schemas/indexes, and performs high-speed bulk inserts (`method='multi'`).

---

## Setup & Running the Project

### 1. Prerequisites
- **Python 3.8+** must be installed on your machine.
- **MySQL Database Server** must be running.

### 2. Configure Database Schema
Before running the ETL pipeline, initialize the `aw_datawarehouse` database using the provided `schema.sql` file located in the root of the project:
```bash
mysql -u root -p < schema.sql
```

### 3. Install Python Dependencies
Install the required libraries:
```bash
pip install -r ETL_Project/requirements.txt
```

### 4. Configure Connection Settings
By default, the pipeline connects to MySQL at `localhost:3306` with username `root` and an empty password.
If your local MySQL uses a password or is running on a different port/host, set the environment variables before running:
- **Windows Command Prompt**:
  ```cmd
  set DB_PASS=your_password
  ```
- **Windows PowerShell**:
  ```powershell
  $env:DB_PASS="your_password"
  ```
- **Linux/macOS**:
  ```bash
  export DB_PASS="your_password"
  ```

Alternatively, you can edit the credentials directly inside [config.py](file:///c:/Users/pc/Desktop/BI/ETL_Project/config.py).

### 5. Run the ETL Pipeline
To execute the pipeline end-to-end, run:
```bash
python ETL_Project/main.py
```

Check the console output or look at the generated log file `etl_pipeline.log` in the root folder to trace execution details.
