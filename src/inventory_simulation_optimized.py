import sqlite3
import csv
import math
from datetime import datetime, timedelta

DB_PATH = "asian_grocery.db"
POLICY_PATH = "outputs/policy_optimization_recommendations.csv"

START_DATE = "2025-01-01"
END_DATE = "2025-12-31"
Z = 1.65


def daterange(start_date, end_date):
    current = start_date
    while current <= end_date:
        yield current
        current += timedelta(days=1)


def load_optimized_policy():
    policy_map = {}

    with open(POLICY_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            product_id = int(row["product_id"])
            policy_map[product_id] = {
                "recommended_reorder_qty": int(row["recommended_reorder_qty"])
            }

    return policy_map


def load_product_parameters(conn, policy_map):
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
    )
    SELECT
      p.product_id,
      p.product_name,
      p.reorder_qty,
      sup.supplier_id,
      sup.supplier_name,
      sup.lead_time_days,
      sup.lead_time_std,
      st.mean_daily_demand,
      st.std_daily_demand
    FROM products p
    JOIN suppliers sup
      ON p.supplier_id = sup.supplier_id
    JOIN stats st
      ON p.product_id = st.product_id
    ORDER BY p.product_id;
    """

    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()

    products = {}

    for row in rows:
        (
            product_id,
            product_name,
            original_reorder_qty,
            supplier_id,
            supplier_name,
            lead_time_days,
            lead_time_std,
            mean_daily,
            std_daily
        ) = row

        mu_d = float(mean_daily)
        sigma_d = float(std_daily)
        L = float(lead_time_days)
        sigma_LT = float(lead_time_std)

        variance = (L * (sigma_d ** 2)) + ((mu_d ** 2) * (sigma_LT ** 2))
        safety_stock = Z * math.sqrt(max(0.0, variance))
        reorder_point = mu_d * L + safety_stock

        optimized_reorder_qty = policy_map.get(product_id, {}).get(
            "recommended_reorder_qty",
            int(original_reorder_qty)
        )

        products[product_id] = {
            "product_name": product_name,
            "original_reorder_qty": int(original_reorder_qty),
            "optimized_reorder_qty": int(optimized_reorder_qty),
            "supplier_id": supplier_id,
            "supplier_name": supplier_name,
            "lead_time_days": int(lead_time_days),
            "lead_time_std": float(lead_time_std),
            "mean_daily_demand": mu_d,
            "std_daily_demand": sigma_d,
            "safety_stock": safety_stock,
            "reorder_point": reorder_point,
        }

    return products


def load_daily_sales(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT sale_date, product_id, qty_sold
        FROM sales
    """)
    rows = cur.fetchall()

    sales_map = {}
    for sale_date, product_id, qty_sold in rows:
        sales_map[(sale_date, product_id)] = qty_sold

    return sales_map


def clear_previous_optimized_simulation(conn):
    cur = conn.cursor()
    cur.execute("DELETE FROM inventory_snapshots_optimized;")
    cur.execute("DELETE FROM purchase_order_items_optimized;")
    cur.execute("DELETE FROM purchase_orders_optimized;")
    conn.commit()


def get_open_po_products(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT poi.product_id
        FROM purchase_orders_optimized po
        JOIN purchase_order_items_optimized poi
          ON po.po_id = poi.po_id
        WHERE po.status = 'placed'
    """)
    rows = cur.fetchall()
    return {row[0] for row in rows}


def receive_due_pos(conn, current_date_str, inventory):
    cur = conn.cursor()

    cur.execute("""
        SELECT po.po_id, poi.product_id, poi.qty_ordered, poi.qty_received
        FROM purchase_orders_optimized po
        JOIN purchase_order_items_optimized poi
          ON po.po_id = poi.po_id
        WHERE po.status = 'placed'
          AND po.expected_arrival = ?
    """, (current_date_str,))

    rows = cur.fetchall()

    for po_id, product_id, qty_ordered, qty_received in rows:
        received_qty = qty_received if qty_received > 0 else qty_ordered
        inventory[product_id] += received_qty

        cur.execute("""
            UPDATE purchase_orders_optimized
            SET status = 'received',
                received_date = ?
            WHERE po_id = ?
        """, (current_date_str, po_id))

        cur.execute("""
            UPDATE purchase_order_items_optimized
            SET qty_received = ?
            WHERE po_id = ? AND product_id = ?
        """, (received_qty, po_id, product_id))

    conn.commit()


def create_purchase_order(conn, product_id, product_info, order_date_str):
    cur = conn.cursor()

    order_date = datetime.strptime(order_date_str, "%Y-%m-%d")
    expected_arrival = order_date + timedelta(days=product_info["lead_time_days"])
    expected_arrival_str = expected_arrival.strftime("%Y-%m-%d")

    cur.execute("""
        INSERT INTO purchase_orders_optimized (
            supplier_id,
            order_date,
            expected_arrival,
            received_date,
            status,
            notes
        )
        VALUES (?, ?, ?, NULL, 'placed', ?)
    """, (
        product_info["supplier_id"],
        order_date_str,
        expected_arrival_str,
        f"Optimized policy simulation for product_id={product_id}"
    ))

    po_id = cur.lastrowid

    cur.execute("""
        SELECT unit_cost
        FROM products
        WHERE product_id = ?
    """, (product_id,))
    unit_cost = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO purchase_order_items_optimized (
            po_id,
            product_id,
            qty_ordered,
            qty_received,
            unit_cost
        )
        VALUES (?, ?, ?, 0, ?)
    """, (
        po_id,
        product_id,
        product_info["optimized_reorder_qty"],
        unit_cost
    ))

    conn.commit()


def save_inventory_snapshot(conn, snapshot_date_str, inventory):
    cur = conn.cursor()

    for product_id, stock_on_hand in inventory.items():
        cur.execute("""
            INSERT INTO inventory_snapshots_optimized (
                snapshot_date,
                product_id,
                stock_on_hand
            )
            VALUES (?, ?, ?)
        """, (snapshot_date_str, product_id, stock_on_hand))

    conn.commit()


def main():
    conn = sqlite3.connect(DB_PATH)

    clear_previous_optimized_simulation(conn)

    policy_map = load_optimized_policy()
    products = load_product_parameters(conn, policy_map)
    sales_map = load_daily_sales(conn)

    inventory = {
        product_id: info["original_reorder_qty"] * 2
        for product_id, info in products.items()
    }

    start_date = datetime.strptime(START_DATE, "%Y-%m-%d")
    end_date = datetime.strptime(END_DATE, "%Y-%m-%d")

    for current_date in daterange(start_date, end_date):
        current_date_str = current_date.strftime("%Y-%m-%d")

        receive_due_pos(conn, current_date_str, inventory)

        for product_id in products:
            qty_sold = sales_map.get((current_date_str, product_id), 0)
            inventory[product_id] = max(0, inventory[product_id] - qty_sold)

        open_po_products = get_open_po_products(conn)

        for product_id, info in products.items():
            current_stock = inventory[product_id]
            rop = info["reorder_point"]

            if current_stock <= rop and product_id not in open_po_products:
                create_purchase_order(conn, product_id, info, current_date_str)

        save_inventory_snapshot(conn, current_date_str, inventory)

    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM inventory_snapshots_optimized;")
    inventory_rows = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM purchase_orders_optimized;")
    po_count = cur.fetchone()[0]

    cur.execute("""
        SELECT
          COUNT(*)
        FROM inventory_snapshots_optimized
        WHERE stock_on_hand = 0
    """)
    total_stockout_rows = cur.fetchone()[0]

    cur.execute("""
        SELECT p.product_name, COUNT(*) AS po_times
        FROM purchase_orders_optimized po
        JOIN purchase_order_items_optimized poi
          ON po.po_id = poi.po_id
        JOIN products p
          ON poi.product_id = p.product_id
        GROUP BY poi.product_id
        ORDER BY po_times DESC
        LIMIT 5
    """)
    top5_pos = cur.fetchall()

    conn.close()

    print("\nOptimized inventory simulation complete.")
    print(f"Inventory snapshot rows: {inventory_rows}")
    print(f"Purchase orders created (optimized): {po_count}")
    print(f"Total stockout snapshot rows (optimized): {total_stockout_rows}")

    print("\nTop 5 most frequently reordered products (optimized):")
    for product_name, po_times in top5_pos:
        print(f"- {product_name}: {po_times} POs")


if __name__ == "__main__":
    main()
