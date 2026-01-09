# 🛒 Retail Demand Forecasting & Inventory Optimization System

## 📌 Project Overview

This project implements an **end-to-end retail demand forecasting and inventory optimization system** for a multi-store retail company.  
The solution forecasts product demand at the **store–product level** and converts those forecasts into **actionable inventory decisions** such as safety stock, reorder points, and order quantities.

The objective is to replace manual, rule-based inventory planning with a **data-driven, scalable approach** to reduce stockouts, minimize excess inventory, and improve operational efficiency.

---

## 🎯 Business Problem

A multi-store retail company operates across multiple regions and product categories.  
The current inventory management process relies on:

- Historical averages  
- Fixed reorder rules  
- Manual judgment  

These approaches fail to capture:
- Store-level demand variation  
- Product-level demand differences  
- Seasonality and trends  
- Promotions, discounts, and pricing effects  

As a result, the business faces frequent stockouts, overstocking, higher holding costs, and limited visibility into future demand.

---

## 🎯 Project Objectives

- Forecast demand at the **store–product level**
- Identify demand trends, seasonality, and variability
- Compare baseline and machine learning forecasting models
- Optimize inventory using:
  - Safety stock
  - Reorder points
  - Order quantity recommendations
- Deliver **actionable business insights** for inventory planning

---

## 🗂 Dataset Description

The dataset contains approximately **73,000 records** with the following key features:

- Date  
- Store ID  
- Product ID  
- Category  
- Region  
- Units Sold (target variable)  
- Inventory Level  
- Units Ordered  
- Price  
- Discount  
- Holiday/Promotion  
- Weather Condition  
- Seasonality  
- Competitor Pricing  

---

## 🧭 Project Workflow

### 1️⃣ Business Understanding
- Defined the business problem and objectives
- Translated business needs into analytical questions

### 2️⃣ Data Understanding & Cleaning
- Validated data types and formats
- Ensured time consistency
- Handled missing values

### 3️⃣ Exploratory Data Analysis (EDA)
- Store performance analysis  
- Product demand analysis (high / medium / low)  
- Store–product demand variation  
- Demand trends over time  
- Seasonal and monthly patterns  
- Demand variability and volatility  
- Promotion and discount impact  
- Price sensitivity  

### 4️⃣ Feature Engineering
- Time-based features (day, week, month, weekday)
- Lag features (lag_1, lag_7, lag_14)
- Rolling averages (7-day, 14-day)
- Promotion indicators
- Encoded categorical variables

A **time-sorted dataset** was used to preserve temporal structure.

---

### 5️⃣ Modeling & Evaluation

#### Baseline Model
- Naive forecast: next-day demand = previous-day demand
- Metric: Mean Absolute Error (MAE)

#### Machine Learning Model
- **Random Forest Regressor**
- Time-based train–test split
- Incorporated lag features, rolling averages, pricing, and promotions

#### Model Performance

| Model | MAE |
|------|-----|
| Baseline | ~119.7 |
| Random Forest | ~89.1 |

➡️ **~26% improvement over baseline**

Classical ARIMA/SARIMA models were evaluated, but ML was selected as the primary approach due to scalability and support for external demand drivers.

---

### 6️⃣ Inventory Optimization (Prescriptive Analytics)

Inventory optimization was performed at the **store–product level** using forecast-driven demand statistics.

Calculated:
- Average demand
- Demand variability (standard deviation)
- Safety stock
- Reorder point (ROP)
- Order quantity

Current inventory levels were compared against reorder points to generate **clear replenishment recommendations**.

---

## 📈 Key Insights

- Demand varies significantly across products and stores
- Promotions and discounts strongly influence demand
- High-variability products require higher safety stock
- Uniform inventory rules lead to inefficiencies
- ML-based forecasting enables proactive inventory planning

---

## 💼 Business Impact

- Reduced stockouts for high-demand products
- Lower excess inventory for slow-moving items
- Improved product availability and customer satisfaction
- Scalable, data-driven inventory decision-making

---

## ⚠️ Assumptions & Limitations

- Constant lead time assumed
- Holding and ordering costs not explicitly modeled
- Forecast accuracy depends on promotion and pricing data quality

---

## 🔮 Future Enhancements

- Supplier-specific lead times
- Cost-based EOQ optimization
- Advanced models (XGBoost / LightGBM)
- Automated dashboards for inventory planners
- Real-time forecast updates

---

## 🧰 Tech Stack

- Python  
- Pandas, NumPy  
- Matplotlib, Seaborn  
- Scikit-learn  
- Statsmodels (optional time-series analysis)

---

## 🌐 FastAPI Application

The project includes a **FastAPI-based REST API** that exposes the demand forecasting and inventory optimization logic as reusable endpoints.

### Available Endpoints

- **POST `/train`**  
  Trains the demand forecasting model using historical data.

- **POST `/predict-inventory`**  
  Returns inventory recommendations for a given store and product:
  - Forecasted daily demand
  - Safety stock
  - Reorder point
  - Order quantity

### Example Request
```json
{
  "store_id": "S001",
  "product_id": "P0001"
}
```

---

## 🚀 How to Run This Project (Local Setup)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Sharayu-Irale/Retail-Demand-Forecasting-Inventory-Optimization.git
cd Retail-Demand-Forecasting-Inventory-Optimization
```

---

### 2️⃣ Create & Activate Virtual Environment
```bash
python -m venv retail
retail\Scripts\activate
```

---

### 3️⃣ Install Dependencies
```bash
cd api
pip install -r requirements.txt
```

---

### 4️⃣ Run the FastAPI Application
```bash
python -m uvicorn main:app --reload
```

---

### 5️⃣ Access Swagger UI
Open your browser and go to:
```
http://127.0.0.1:8000/docs
```

---

### 6️⃣ API Usage Flow
1. Call **POST `/train`** (no request body) to train the model  
2. Call **POST `/predict-inventory`** with store and product IDs  

---

## ☁️ Deployment

The FastAPI application is deployed on **Render** as a cloud-hosted web service.  
Swagger UI is available for interactive API testing after deployment.

---

## 📈 Future Enhancements

- Supplier-specific lead times  
- Cost-based EOQ optimization  
- Advanced models (XGBoost / LightGBM)  
- Model persistence using joblib  
- Dockerization and CI/CD pipeline  
- Real-time demand forecasting dashboards  

---

## 👤 Author

**Sharayu Irale**
