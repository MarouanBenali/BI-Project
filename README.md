# Business-Intelligence-project-with-Python-and-PowerBI

The goal is to build a data-driven BI system based on free data and your choice to cross with one or more multi-format sources to include this heterogeneity problem.

We must build the cube and then generate two reports that you consider relevant.

We will have to take into consideration:
- The choice of the environment (ETL, Database, BI Platform ...)
- Presentation and method of analysis.
- The structure of the reports
- Optimization

---

## 📁 Project Files
- **schema.sql**: MySQL data warehouse schema
- **requirements.txt**: Python dependencies
- **ETL_Project/**: Complete Python ETL pipeline
- **Professional_PowerBI_Dashboard_Guide.md**: Full A-to-Z Power BI guide (English)
- **RAPPORT_FRANCAIS.md**: Rapport complet du projet en Français
- **check_integrity.py**: Data integrity validator
- **advanced_analysis_queries.sql**: Helpful SQL queries
- **final_star_schema_fix_summary.sql**: Star schema fixes

---

## 📊 Dataset
The dataset provided is a minimized version of Microsoft's AdventureWorks.  
More info: https://github.com/microsoft/sql-server-samples/tree/master/samples/databases/adventure-works

---

## 🛠️ Built With
* [Power BI](https://powerbi.microsoft.com/en-us/) - Interactive Data Visualization
<p align="center">
    <img width="100" height="100" src="https://powerbi.microsoft.com/pictures/shared/social/social-default-image.png">
</p>

* [Python](https://www.python.org/) - Python-based ETL Pipeline (Extract → Transform → Load)
<p align="center">
    <img width="300" height="100" src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png">
</p>

* [MySQL WorkBench](https://www.mysql.com/products/workbench/)

---

## 🚀 Quick Start

This project uses a **Python-based ETL pipeline** (instead of Talend) for simplicity and maintainability.

### Setup Instructions:
1. Install Python 3.8+ and MySQL Server
2. Create the MySQL database using `schema.sql`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the ETL pipeline: `python ETL_Project/main.py`
5. **Build a Professional Dashboard**: Follow the full guide at `Professional_PowerBI_Dashboard_Guide.md`!
6. (Optional) Open the existing `PowerBI - Adventureworks Cycle.pbix`

---

## 🏆 Project Outcome
- ✅ Production-ready ETL pipeline
- ✅ Fully functional Star Schema data warehouse
- ✅ Complete guide for building a professional Power BI dashboard
- ✅ Portfolio-ready BI project

Check the `Screenshots/` folder for examples!
