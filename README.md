# Grocery Inventory Management System

## Project Overview
This project stimulates an **inventory and replenishment management system** for an Asian grocery store in 2025, in Germany.

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

## System Architecture
1. SQL database
   - Products
   - Suppliers
   - Sales (simulated daily demand)
   - Inventory levels
   - Purchase orders
     
2. Python simulation & analytics
   - Demand simulation (randomness + seasonality + promotion)
   - Demand mean and variability calculation
   - Safety stock and reorder point calculation
   - Inventory simulation
   - Stockout and replenishment analysis
   - Strategy optimization

## System Flows
1. Demand Generation (Python)
2. Sales Data (SQLite)
3. Inventory Simulation (Baseline)
4. Purchase Orders Automation (reorder)
5. Diagnostic Analysis
6. Replenishment Optimization
7. Performance Comparison

## Key Metrics
- Daily demand mean and standard deviation
- Safety stock level
- Reorder point
- Stockout rate
- Purchase order frequency

## Key Results
### Purchase Orders
![Purchase Orders Comparison](outputs/po_comparison.png)

- Baseline: **276**
- Optimized: **199**
- Change: **⬇27.9%**

### Stockout Rate
![Stockout Rate Comparison](outputs/stockout_comparison.png)

- Baseline: **15.51%**
- Optimized: **0.27%**
- Change: **⬇98%**
## Key Insights
