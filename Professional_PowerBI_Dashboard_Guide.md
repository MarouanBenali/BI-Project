# Professional Power BI Dashboard Guide (A to Z) — AdventureWorks

This document is a **complete professional guide** to build a full Power BI dashboard using the AdventureWorks data warehouse.
It is structured like a **real Business Intelligence project used in companies**.

---

# 🧱 Step 1: Connect Power BI to MySQL

1. Open **Power BI Desktop**
2. Click **Get Data → Database → MySQL Database**
3. Enter:
   - Server: `localhost` (or your MySQL server)
   - Database: `aw_datawarehouse`
4. Enter credentials
5. Click:
   - **Load** OR
   - **Transform Data** (recommended)

---

# 🧠 Step 2: Data Model (VERY IMPORTANT)

## 🔗 Create Relationships

Ensure the following relationships:

- `aw_sales[ProductKey]` → `aw_products_lookup[ProductKey]`
- `aw_sales[CustomerKey]` → `aw_customers_lookup[CustomerKey]`
- `aw_sales[TerritoryKey]` → `aw_territories_lookup[SalesTerritoryKey]`
- `aw_sales[OrderDate]` → `aw_calendar_lookup[Date]`
- `aw_product_subcategory_lookup[ProductCategoryKey]` → `aw_product_category_lookup[ProductCategoryKey]`

---

## 📌 Star Schema Structure

### Fact Tables:
- aw_sales
- aw_returns

### Dimension Tables:
- customers
- products
- territories
- calendar
- categories

---

# 📊 Step 3: DAX Measures (CORE KPIs)

## 💰 Revenue
```dax
Revenue = 
SUMX( 
    aw_sales, 
    aw_sales[OrderQuantity] * RELATED(aw_products_lookup[ProductPrice]) 
)
```

## 📦 Total Quantity
```dax
Total Quantity = SUM(aw_sales[OrderQuantity])
```

## 👥 Total Customers
```dax
Total Customers = DISTINCTCOUNT(aw_customers_lookup[CustomerKey])
```

## 📊 Total Orders
```dax
Total Orders = DISTINCTCOUNT(aw_sales[OrderDate])
```

## 🔁 Return Rate
```dax
Return Rate = 
DIVIDE( 
    SUM(aw_returns[ReturnQuantity]), 
    SUM(aw_sales[OrderQuantity]) 
)
```

## 💵 Average Order Value
```dax
AOV = DIVIDE([Revenue], [Total Orders])
```

---

# 🏆 Step 4: Page 1 — Executive Dashboard

🎯 Goal: High-level KPIs for decision makers

📌 KPIs (Top Cards)
- Revenue
- Total Quantity
- Total Customers
- Total Orders
- Return Rate

📈 Visuals
1. Sales Trend (Line Chart)
   - X-axis: Date hierarchy (Year → Month)
   - Y-axis: Revenue
2. Revenue by Category (Bar Chart)
   - CategoryName
   - Revenue
3. Sales by Territory (Map / Bar)
   - Country / Region
   - Revenue
   - Continent (Legend)
4. Top 5 Products
   - ProductName
   - Revenue

---

# 🌍 Step 5: Page 2 — Sales Analysis

🎯 Goal: Understand WHERE and WHAT we sell

📊 Visuals
1. Territory Analysis
   - Country / Region
   - Revenue
   - Continent (Legend)
2. Sales by Category
   - CategoryName
   - Revenue
3. Top Products
   - ProductName
   - Revenue (Top 10 filter)
4. Monthly Trend
   - Date hierarchy
   - Revenue

---

# 👥 Step 6: Page 3 — Customer Analysis

🎯 Goal: Understand customer behavior

📊 Visuals
1. Customers by Income Level
   - IncomeLevel
   - Customer Count
2. Customers by Age
   - Age groups (bins)
3. Customers by Occupation
   - Occupation
   - Count

💡 KPI
```dax
Avg Revenue per Customer = DIVIDE([Revenue], [Total Customers])
```

---

# 🔁 Step 7: Page 4 — Returns Analysis

🎯 Goal: Analyze product quality issues

📊 Visuals
1. Return Rate KPI
2. Top Returned Products
   - ProductName
   - ReturnQuantity
3. Returns by Category
   - CategoryName
   - Return Rate
4. Returns Over Time
   - Date
   - ReturnQuantity

---

# 🎛️ Step 8: Interactivity (IMPORTANT)

🔘 Slicers
- Year
- Country
- Category
- Income Level

🔗 Cross Filtering
- Enable interaction between all visuals

🧭 Drill Down
- Year → Quarter → Month
- Category → Product

📌 Drill Through Pages
- Product Details Page
- Customer Details Page

---

# 🎨 Step 9: Design Guidelines

🎨 Theme
- Primary: Dark Blue
- Secondary: Gray
- Accent: Green / Red

📐 Layout Structure
- TOP: KPIs
- MIDDLE: Trends
- BOTTOM: Breakdown
- RIGHT: Filters

💡 Best Practices
- Prefer Bar & Line charts
- Avoid too many donuts
- Keep layout clean
- Use consistent colors

---

# 🚀 Step 10: Advanced Features

🧠 Q&A
Ask:
- Top products
- Sales by country

🔍 Tooltips
- Revenue
- Return Rate
- Quantity

🌳 Decomposition Tree
Revenue breakdown:
- Country
- Category
- Product

📊 Key Influencers
What drives Return Rate?

---

# 🏁 FINAL RESULT

After completing this guide, you will have:
- ✔ Professional BI Dashboard
- ✔ Star Schema Data Model
- ✔ Advanced DAX Measures
- ✔ Interactive Reports
- ✔ Portfolio-ready project
