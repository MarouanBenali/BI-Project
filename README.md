# Business Intelligence Project — AdventureWorks (Python + Power BI)

## 📋 Overview
This is a **complete, production-ready Business Intelligence (BI) project** built using Microsoft's AdventureWorks dataset.
It includes a Python ETL pipeline, a MySQL data warehouse (Star Schema), and a full guide to building a professional Power BI dashboard.

---

## 🛠️ Built With
| Component             | Tool/Language        |
|-----------------------|----------------------|
| **ETL Pipeline**      | Python 3.8+          |
| **Data Warehouse**    | MySQL                |
| **Visualization**     | Power BI Desktop     |
| **Data Modeling**     | MySQL Workbench      |

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
├── MySql Workbanch/              # MySQL files (schema, queries)
│   ├── advanced_analysis_queries.sql
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
✅ **Production-ready Python ETL pipeline** (~8 seconds execution time)
✅ **Fully functional Star Schema data warehouse**
✅ **100% data integrity validated**
✅ **Professional Power BI dashboard included**
✅ **Advanced SQL analysis queries**
✅ **Complete project documentation** (PPTX, DOCX, diagrams)
✅ **Portfolio-ready project structure**

---

## 📚 Documentation
- Full documentation available in the `Documentation/` folder
- Diagrams available in `Diagrams/`
- SQL queries available in `MySql Workbanch/`
- Power BI dashboard in `PowerBI/`

---

## 🏆 Credits
- AdventureWorks dataset by Microsoft: https://github.com/microsoft/sql-server-samples
