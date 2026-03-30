import sqlite3
import csv
import math
import os

DB_PATH = "asian_grocery.db"
OUT_PATH = "outputs/replenishment_diagnostic_report.csv"

START_DATE = "2025-01-01"
END_DATE = "2025-12-31"
Z = 1.65


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # ---- 1. Demand statistics + supplier info ----
    query = f"""
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
    ),
    po_counts AS (
      SELECT
        poi.product_id,
        COUNT(*) AS po_count
      FROM purchase_order_items poi
      JOIN purchase_orders po
        ON poi.po_id = po.po_id
      GROUP BY poi.product_id
    ),
    stockout_stats AS (
      SELECT
        product_id,
        SUM(CASE WHEN stock_on_hand = 0 THEN 1 ELSE 0 END) AS stockout_days,
        COUNT(*) AS total_snapshot_days
      FROM inventory_snapshots
      GROUP BY product_id
    )
    SELECT
      p.product_id,
      p.product_name,
      sup.supplier_name,
      p.category,
      p.reorder_qty,
      sup.lead_time_days,
      sup.lead_time_std,
      st.mean_daily_demand,
      st.std_daily_demand,
      COALESCE(pc.po_count, 0) AS po_count,
      COALESCE(ss.stockout_days, 0) AS stockout_days,
      COALESCE(ss.total_snapshot_days, 0) AS total_snapshot_days
    FROM products p
    JOIN suppliers sup
      ON p.supplier_id = sup.supplier_id
    JOIN stats st
      ON p.product_id = st.product_id
    LEFT JOIN po_counts pc
      ON p.product_id = pc.product_id
    LEFT JOIN stockout_stats ss
      ON p.product_id = ss.product_id
    ORDER BY p.product_id;
    """

    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    os.makedirs("outputs", exist_ok=True)

    results = []

    for row in rows:
        (
            product_id,
            product_name,
            supplier_name,
            category,
            reorder_qty,
            lead_time_days,
            lead_time_std,
            mean_daily,
            std_daily,
            po_count,
            stockout_days,
            total_snapshot_days
        ) = row

        μ = float(mean_daily)
        σ_d = float(std_daily)
        L = float(lead_time_days)
        σ_LT = float(lead_time_std)

        # Full safety stock model
        variance = (L * (σ_d ** 2)) + ((μ ** 2) * (σ_LT ** 2))
        safety_stock = Z * math.sqrt(max(0.0, variance))
        reorder_point = (μ * L) + safety_stock

        stockout_rate = 0
        if total_snapshot_days > 0:
            stockout_rate = stockout_days / total_snapshot_days

        rop_to_reorder_ratio = None
        if reorder_qty and reorder_qty > 0:
            rop_to_reorder_ratio = float(reorder_point) / float(reorder_qty)

        results.append({
            "product_id": product_id,
            "product_name": product_name,
            "supplier_name": supplier_name,
            "category": category,
            "mean_daily_demand": round(μ, 2),
            "std_daily_demand": round(σ_d, 2),
            "lead_time_days": lead_time_days,
            "lead_time_std": lead_time_std,
            "safety_stock": math.ceil(safety_stock),
            "reorder_point": math.ceil(reorder_point),
            "reorder_qty_current": reorder_qty,
            "po_count": po_count,
            "stockout_days": stockout_days,
            "stockout_rate": round(stockout_rate, 4),
            "rop_to_reorder_ratio": round(rop_to_reorder_ratio, 2) if rop_to_reorder_ratio is not None else None
        })

    # ---- Save CSV ----
    fieldnames = list(results[0].keys())

    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # ---- Print top 5 by PO count ----
    top_po = sorted(results, key=lambda x: x["po_count"], reverse=True)[:5]

    print("\nTop 5 products by PO count:\n")
    for r in top_po:
        print(
            f"{r['product_name']} | "
            f"POs={r['po_count']} | "
            f"ROP={r['reorder_point']} | "
            f"ReorderQty={r['reorder_qty_current']} | "
            f"ROP/Qty={r['rop_to_reorder_ratio']} | "
            f"StockoutRate={r['stockout_rate']}"
        )

    # ---- Print top 5 by stockout rate ----
    top_stockout = sorted(results, key=lambda x: x["stockout_rate"], reverse=True)[:5]

    print("\nTop 5 products by stockout rate:\n")
    for r in top_stockout:
        print(
            f"{r['product_name']} | "
            f"StockoutDays={r['stockout_days']} | "
            f"StockoutRate={r['stockout_rate']} | "
            f"POs={r['po_count']}"
        )

    print(f"\nSaved report: {OUT_PATH}")


if __name__ == "__main__":
    main()
