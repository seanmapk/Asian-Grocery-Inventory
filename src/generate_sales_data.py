import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "asian_grocery.db"

START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 12, 31)

def load_product_profiles(cur):
    """
    Build a product profile map with:
    - product_name
    - category
    - base_demand
    - seasonality type
    - promo sensitivity
    """
    cur.execute("""
        SELECT product_id, product_name, category
        FROM products
    """)
    rows = cur.fetchall()

    product_profiles = {}

    for product_id, product_name, category in rows:
        name = product_name.lower()
        category_lower = category.lower()

        # 1) Base demand by product/category characteristics
        if "dumplings" in name or "rice" in name:
            base_demand = random.randint(10, 15)   # staple / high demand
        elif "kimchi" in name:
            base_demand = random.randint(8, 12)
        elif "bubble milk tea" in name:
            base_demand = random.randint(6, 10)
        elif "hot pot" in name:
            base_demand = random.randint(5, 9)
        elif "sauce" in name or "paste" in name:
            base_demand = random.randint(6, 10)
        elif "cake" in name or "pocky" in name:
            base_demand = random.randint(5, 9)
        else:
            base_demand = random.randint(4, 8)

        # 2) Seasonality tag
        seasonality = "normal"

        # Winter-demand products
        if "hot pot" in name:
            seasonality = "winter_hotpot"

        # Summer-demand products
        elif "bubble milk tea" in name or "beverage" in category_lower:
            seasonality = "summer_drink"

        # Year-end / gifting products
        elif "cake" in name or "snacks" in category_lower:
            seasonality = "holiday_gift"

        # 3) Promotion sensitivity
        # Higher value = stronger lift if promo happens
        if "dumplings" in name or "kimchi" in name:
            promo_sensitivity = 1.4
        elif "bubble milk tea" in name or "pocky" in name or "cake" in name:
            promo_sensitivity = 1.6
        else:
            promo_sensitivity = 1.3

        product_profiles[product_id] = {
            "product_name": product_name,
            "category": category,
            "base_demand": base_demand,
            "seasonality": seasonality,
            "promo_sensitivity": promo_sensitivity,
        }

    return product_profiles


def apply_seasonality(demand, profile, date):
    """
    Adjust demand based on product-specific seasonality.
    """
    seasonality = profile["seasonality"]

    # Winter peak for hot pot related items: Nov-Feb
    if seasonality == "winter_hotpot" and date.month in [11, 12, 1, 2]:
        demand *= 1.45

    # Summer peak for drinks: Jun-Aug
    elif seasonality == "summer_drink" and date.month in [6, 7, 8]:
        demand *= 1.35

    # Holiday gift/snack peak: Nov-Dec
    elif seasonality == "holiday_gift" and date.month in [11, 12]:
        demand *= 1.30

    return demand


def apply_weekend_effect(demand, date):
    """
    Weekend demand uplift.
    """
    if date.weekday() >= 5:  # Saturday / Sunday
        demand *= 1.20
    return demand


def apply_promotion_spike(demand, profile):
    """
    Random promotion spike.
    Small probability each day, but stronger effect for promo-sensitive products.
    """
    promo_probability = 0.04  # 4% chance per day

    if random.random() < promo_probability:
        demand *= profile["promo_sensitivity"]

    return demand


def generate_daily_demand(profile, date):
    """
    Demand generation logic:
    1. Start from product base demand
    2. Apply seasonality
    3. Apply weekend effect
    4. Apply promotion spike
    5. Add random noise
    """
    demand = profile["base_demand"]

    demand = apply_seasonality(demand, profile, date)
    demand = apply_weekend_effect(demand, date)
    demand = apply_promotion_spike(demand, profile)

    # Add stochastic noise
    demand = random.normalvariate(demand, 2)

    return max(0, int(demand))


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Optional but recommended:
    # clear old sales data before regeneration
    cur.execute("DELETE FROM sales;")

    product_profiles = load_product_profiles(cur)

    current_date = START_DATE
    while current_date <= END_DATE:
        for product_id, profile in product_profiles.items():
            qty_sold = generate_daily_demand(profile, current_date)

            cur.execute("""
                INSERT OR REPLACE INTO sales (sale_date, product_id, qty_sold)
                VALUES (?, ?, ?)
            """, (
                current_date.strftime("%Y-%m-%d"),
                product_id,
                qty_sold
            ))

        current_date += timedelta(days=1)

    conn.commit()
    conn.close()

    print("Sales data generation with seasonality and promotion spikes complete.")


if __name__ == "__main__":
    main()
