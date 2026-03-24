# Grocery Inventory Management System

## Project Overview
This project stimulates an **inventory and replenishment management system** for an Asian grocery store in Germany.

Many imported Asian products often face challenges such as:
- Long supplier lead times
- Demand fluctuations (weekend/seasonal peaks)
- Out of stock or overstock

This system integrates SQL database design with Python simulation and analytics to support data-driven replenishment decisions. The goal is to help the management team minimize stockout risk while improving operational efficiency.

## Observed Business Problem
- Uncertain supplier lead times
- Demand volatility (e.g., weekend/seasonal peaks, promotions)
- Risk of overstock and product expiration
- Inefficient replenishment (too frequent reordering)

## Technical Tools
- **Database:** SQLite (relational schema design)
- **Programming:** Python (Pandas, SQL query)
- **Analytics:** Demand forecasting, safety stock calculation, reorder point model
- **Output:** KPI reports, replenishment recommendations

## System Architecture
1. SQL database
   - Products
   - Suppliers
   - Sales transactions
   - Inventory levels
   - Purchase orders
     
2. Python scripts
   - Generate and simulate demand data
   - Calculate the demand mean and variability
   - Calculate safety stock and reorder point
   - Analyze stockout rate and inventory turnover
   - Summarize replenishment recommendations

## Key Metrics
- Daily demand mean and standard deviation
- Safety stock level
- Reorder point
- Stockout rate
- Inventory turnover ratio
