import sqlite3
import csv
import math
import os

DB_PATH = "asian_grocery.db"
OUT_PATH = "outputs/reorder_point_report.csv"

# Service level (95%)
Z = 1.65

START_DATE = "2025-01-01"
END_DATE = "2025-12-31"

QUERY = f"""
WITH daily AS (
  SELECT
    s.product_id,
    s.sale_date,
    s.qty_sold
  FROM sales s
  WHERE s.sale_date BETWEEN '{START_DATE}' AND '{END_DATE}'
),
stats AS (
  SELECT
    product_id,
    AVG(qty_sold) AS mean_daily_demand,
    SQRT(AVG(qty_sold * qty_sold) - AVG(qty_sold) * AVG(qty_sold)) AS std_daily_demand
  FROM daily
  GROUP BY product_id
)

SELECT
  p.product_id,
  p.product_name,
  p.category,
  sup.supplier_name,
  sup.lead_time_days,
  sup.lead_time_std,
  p.reorder_qty,
  st.mean_daily_demand,
  st.std_daily_demand
FROM products p
JOIN suppliers sup
  ON p.supplier_id = sup.supplier_id
JOIN stats st
  ON p.product_id = st.product_id
ORDER BY p.product_id;
"""

def main():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(QUERY)
    rows = cur.fetchall()

    conn.close()

    os.makedirs("outputs", exist_ok=True)

    results = []

    for row in rows:

        (
            product_id,
            product_name,
            category,
            supplier_name,
            lead_time_days,
            lead_time_std,
            reorder_qty,
            mean_daily,
            std_daily
        ) = row

        # ---- Demand variables ----
        μ = float(mean_daily)
        σ_d = float(std_daily)

        # ---- Lead time variables ----
        L = float(lead_time_days)
        σ_LT = float(lead_time_std)

        # ---- FULL Safety Stock formula ----
        variance = (L * (σ_d ** 2)) + ((μ ** 2) * (σ_LT ** 2))
        safety_stock = Z * math.sqrt(variance)

        # ---- Reorder Point ----
        reorder_point = μ * L + safety_stock

        results.append({
            "product_id": product_id,
            "product_name": product_name,
            "supplier": supplier_name,
            "lead_time_days": L,
            "lead_time_std": σ_LT,
            "mean_daily_demand": round(μ, 2),
            "std_daily_demand": round(σ_d, 2),
            "safety_stock": math.ceil(safety_stock),
            "reorder_point": math.ceil(reorder_point),
            "reorder_qty_current": reorder_qty
        })

    # ---- save CSV ----
    fieldnames = list(results[0].keys())

    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # ---- print Top 5 ROP ----
    top5 = sorted(results, key=lambda x: x["reorder_point"], reverse=True)[:5]

    print("\nTop 5 Highest Reorder Point Products:\n")

    for p in top5:
        print(
            f"{p['product_name']} | "
            f"LT={p['lead_time_days']}±{p['lead_time_std']} | "
            f"Mean={p['mean_daily_demand']} | "
            f"SS={p['safety_stock']} | "
            f"ROP={p['reorder_point']}"
        )

    print("\nSaved report:", OUT_PATH)


if __name__ == "__main__":
    main()
