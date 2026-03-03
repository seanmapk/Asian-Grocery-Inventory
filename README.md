# Grocery Inventory Management System

## Project Overview
This project stimulates an inventory and replenishment management system for an Asian grocery store in Germany.
Many imported Asian products may face the risk of long supplier lead times, demand fluctuations, and out of stock.
This system integrates SQL data query/storage with Python analytics to support data-driven decision-making.
The goal is to help the management team minimize stockout risk while maintaining a healthy inventory level.

## Business Problem
- Uncertain supplier lead times
- Demand volatility (e.g., weekend/seasonal peaks)
- Risk of overstock and product expiration
- Stockout due to delayed transportation

This project provides analytical tools that aim to improve replenishment decisions and tackle the above challenges.

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
