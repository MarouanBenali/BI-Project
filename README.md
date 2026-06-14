# Business Intelligence Project — AdventureWorks (Python + Power BI)

## 📋 Overview
This is a **complete, production-ready Business Intelligence (BI) project** built using Microsoft's AdventureWorks dataset.
It includes a Python ETL pipeline, a MySQL data warehouse (Star Schema), a full guide to building a professional Power BI dashboard, **and machine learning features!

---

## 🛠️ Built With
| Component             | Tool/Language        |
|-----------------------|----------------------|
| **ETL Pipeline**      | Python 3.8+          |
| **Data Warehouse**    | MySQL                |
| **Visualization**     | Power BI Desktop     |
| **Data Modeling**     | MySQL Workbench      |
| **Machine Learning**  | scikit-learn, pandas |

---

## 📁 Project Structure & Files
```
BI-Project/
├── Dataset/                      # Raw CSV data files
│   ├── Sales/
│   └── ...
├── Diagrams/                     # Data model diagrams
├── Documentation/                # Project documentation (PPTX, DOCX)
├── ETL_Project/                  # Python ETL pipeline
│   ├── main.py                   # Main orchestration
│   ├── extract.py                # Data extraction logic
│   ├── transform.py              # Data transformation logic
│   ├── load.py                   # Data loading logic
│   ├── config.py                 # Central configuration
│   └── utils.py                  # Helper functions
├── ML/                            # Machine Learning scripts
│   ├── customer_segmentation.py # Customer Segmentation using K-Means
│   ├── sales_forecasting.py       # Sales Forecasting
│   └── README.md
├── MySql Workbanch/              # MySQL files (schema, queries)
│   ├── advanced_analysis_queries.sql
│   ├── final_star_schema_fix_summary.sql
│   └── schema.sql
├── PowerBI/                      # Power BI dashboard files
│   ├── PowerBI.pbix
│   └── PowerBI.pdf
├── .gitignore                    # Git ignore rules
├── README.md                     # This file
└── requirements.txt              # Python dependencies
```

---

## 🚀 Quick Start
### 1. Prerequisites
- Python 3.8+
- MySQL Server
- Power BI Desktop

### 2. Setup Instructions
1. **Create the database**: Run `MySql Workbanch/schema.sql` in MySQL Workbench or your MySQL client
2. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```
3. **Configure database credentials**: Edit `ETL_Project/config.py` with your MySQL username/password
4. **Run ETL pipeline**:
   ```powershell
   python ETL_Project/main.py
   ```
5. **View the dashboard**: Open `PowerBI/PowerBI.pbix` in Power BI Desktop

---

## 🤖 Machine Learning Features
### 1. Customer Segmentation (K-Means Clustering)
Segments customers into meaningful groups based on:
- Age
- Total Orders
- Total Quantity Purchased

**How to run:**
```powershell
python ML/customer_segmentation.py
```

### 2. Sales Forecasting (Time Series)
Forecasts future monthly sales using Linear Regression (with lag features)

**How to run:**
```powershell
python ML/sales_forecasting.py
```

Results and visualizations are saved in `ML/results/`!

---

## 📊 Data Model (Star Schema)
### Fact Tables
- `aw_sales` (Sales transactions)
- `aw_returns` (Return transactions)

### Dimension Tables
- `aw_customers_lookup`
- `aw_products_lookup`
- `aw_calendar_lookup`
- `aw_territories_lookup`
- `aw_product_category_lookup`
- `aw_product_subcategory_lookup`

All foreign key constraints are properly set up and validated!

---

## ✨ Key Features
✅ **Production-ready Python ETL pipeline** (~21 seconds execution time)
✅ **Fully functional Star Schema data warehouse**
✅ **100% data integrity validated**
✅ **Professional Power BI dashboard included**
✅ **Advanced SQL analysis queries**
✅ **Machine Learning Features (Customer Segmentation, Sales Forecasting)**
✅ **Complete project documentation** (PPTX, DOCX, diagrams)
✅ **Portfolio-ready project structure**

---

## 📚 Documentation
- Full documentation available in the `Documentation/` folder
- Diagrams available in `Diagrams/`
- SQL queries available in `MySql Workbanch/`
- Power BI dashboard in `PowerBI/`
- ML scripts and README in `ML/`

---

## 🏆 Credits
- AdventureWorks dataset by Microsoft: https://github.com/microsoft/sql-server-samples
