import sqlite3
import csv

DB_PATH = "asian_grocery.db"
OUT_PATH = "outputs/top_fast_movers.csv"

QUERY = """
SELECT
  p.product_name,
  sup.supplier_name,
  sup.lead_time_days,
  SUM(s.qty_sold) AS total_units_sold
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN suppliers sup ON p.supplier_id = sup.supplier_id
GROUP BY p.product_id
ORDER BY total_units_sold DESC
LIMIT 5;
"""

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(QUERY)
    rows = cur.fetchall()

    # ensure outputs folder exists
    import os
    os.makedirs("outputs", exist_ok=True)

    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["product_name", "supplier_name", "lead_time_days", "total_units_sold"])
        writer.writerows(rows)

    conn.close()
    print(f"Saved: {OUT_PATH}")
    print("\nTop 5 Fast Movers:")
    for r in rows:
        print(f"- {r[0]} | {r[1]} | LT={r[2]}d | Units={r[3]}")

if __name__ == "__main__":
    main()
