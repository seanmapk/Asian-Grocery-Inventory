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
![KPI Dashboard](kpi_dashboard.png)
<p align="center">
  <strong>Figure:</strong> The optimized policy reduces purchase orders by 27.9% while lowering the stockout rate from 15.51% to 0.27%, demonstrating improved replenishment efficiency and service level.
</p>
- The optimization balances inventory efficiency and service level through dynamic adjustment of reorder quantities.
  
## Key Insights
### 1. High-Risk Products Improved Stockout Rate Significantly
- Frozen Dumplings: **63.8% → 1.6%**
- Kimchi: **55.6% → 0.8%**
- Hot Pot Soup Base: **50.4% → 1.3%**

These products originally faced **long supplier lead time** & **undersized reorder quantities**.

### 2. Moderate Concerns Fully Resolved
- Pineapple Cake: **25.5% → 0%**
- Thai Jasmine Rice: **24.9% → 0%**
- Korean BBQ Sauce: **12.1% → 0%**

Optimized batch sizes to eliminate stockouts.

### 3. Stable Products Remained Efficient
- Sushi Rice
- Miso Paste  
- Soy Sauce
   
No unnecessary strategy changes were made.


![SKU Improvement Chart](sku_improvement_chart.png)
<p align="center">
  <strong>Figure:</strong> SKU-Level (stock keeping unit) Stockout Rate Improvement After Policy Optimization
</p>

## Methodology
### Demand Model
Demand = base_demand × seasonality effect × weekend effect × promotion effect + random noise

### Inventory Model
Reorder Point = μ × L + Z × √(Lσ² + μ²σ_L²)
- μ: mean daily demand
- L: supplier lead time
- Z: service level factor
- σ: standard deviation of daily demand
- σ_L: lead time variability

### Optimization Logic
- Increase batch size for high stockout SKUs
- Adjust reorder quantity when ROP is too high
- Slightly increase batch size for frequently ordered items
- Keep stable products unchanged

## Key Takeaways
1. Small reorder quantities may lead to **high stockout** and **frequent reordering**
2. Demand variability must be taken into account in inventory decisions
3. Data-driven and rule-based optimization can bring significant business improvements
