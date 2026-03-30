import csv
import math
import os

INPUT_PATH = "outputs/replenishment_diagnostic_report.csv"
OUTPUT_PATH = "outputs/policy_optimization_recommendations.csv"


def recommend_reorder_qty(current_qty, rop, stockout_rate, po_count):
    """
    Rule-based optimization logic

    Rule A:
    If stockout_rate >= 0.20
    -> recommended qty = ceil(1.5 * ROP)

    Rule B:
    If stockout_rate < 0.20 and ROP/current_qty >= 1.5
    -> recommended qty = ceil(1.2 * ROP)

    Rule C:
    If stockout_rate == 0 and po_count >= 20 and ROP/current_qty < 1.5
    -> recommended qty = ceil(1.15 * current_qty)

    Otherwise:
    -> keep current qty
    """

    if current_qty <= 0:
        return current_qty, "Invalid current reorder quantity"

    rop_to_reorder_ratio = rop / current_qty

    if stockout_rate >= 0.20:
        return math.ceil(1.5 * rop), "High stockout rate: increase batch size"

    if stockout_rate < 0.20 and rop_to_reorder_ratio >= 1.5:
        return math.ceil(1.2 * rop), "ROP too high relative to current reorder quantity"

    if stockout_rate == 0 and po_count >= 20 and rop_to_reorder_ratio < 1.5:
        return math.ceil(1.15 * current_qty), "No stockout risk but placing frequent orders: increase batch size slightly"

    return current_qty, "Keep current replenishment strategy"


def main():

    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Input file not found: {INPUT_PATH}")

    os.makedirs("outputs", exist_ok=True)

    results = []

    with open(INPUT_PATH, "r", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader:

            product_id = int(row["product_id"])
            product_name = row["product_name"]
            supplier_name = row["supplier_name"]
            category = row["category"]

            mean_daily_demand = float(row["mean_daily_demand"])
            std_daily_demand = float(row["std_daily_demand"])

            lead_time_days = float(row["lead_time_days"])
            lead_time_std = float(row["lead_time_std"])

            safety_stock = float(row["safety_stock"])
            reorder_point = float(row["reorder_point"])

            current_reorder_qty = int(row["reorder_qty_current"])

            po_count = int(row["po_count"])
            stockout_days = int(row["stockout_days"])
            stockout_rate = float(row["stockout_rate"])

            rop_to_reorder_ratio = float(row["rop_to_reorder_ratio"])

            recommended_qty, reason = recommend_reorder_qty(
                current_qty=current_reorder_qty,
                rop=reorder_point,
                stockout_rate=stockout_rate,
                po_count=po_count
            )

            qty_increase = recommended_qty - current_reorder_qty

            pct_increase = 0
            if current_reorder_qty > 0:
                pct_increase = qty_increase / current_reorder_qty

            results.append({
                "product_id": product_id,
                "product_name": product_name,
                "supplier_name": supplier_name,
                "category": category,
                "mean_daily_demand": round(mean_daily_demand, 2),
                "std_daily_demand": round(std_daily_demand, 2),
                "lead_time_days": lead_time_days,
                "lead_time_std": lead_time_std,
                "safety_stock": round(safety_stock, 2),
                "reorder_point": round(reorder_point, 2),
                "current_reorder_qty": current_reorder_qty,
                "po_count": po_count,
                "stockout_days": stockout_days,
                "stockout_rate": round(stockout_rate, 4),
                "rop_to_reorder_ratio": round(rop_to_reorder_ratio, 2),
                "recommended_reorder_qty": recommended_qty,
                "qty_increase": qty_increase,
                "pct_increase": round(pct_increase, 4),
                "optimization_reason": reason
            })

    # Save CSV
    fieldnames = list(results[0].keys())

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # Print biggest adjustments
    biggest_adjustments = sorted(results, key=lambda x: x["qty_increase"], reverse=True)[:10]

    print("\nTop items with biggest reorder quantity adjustment:\n")

    for r in biggest_adjustments:

        print(
            f"{r['product_name']} | "
            f"CurrentQty={r['current_reorder_qty']} -> RecommendedQty={r['recommended_reorder_qty']} | "
            f"Increase={r['qty_increase']} | "
            f"ROP={r['reorder_point']} | "
            f"StockoutRate={r['stockout_rate']} | "
            f"Reason={r['optimization_reason']}"
        )

    print(f"\nSaved report: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
