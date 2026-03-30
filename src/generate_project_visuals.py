import os
import matplotlib.pyplot as plt

OUTPUT_DIR = "outputs"

BASELINE_PO = 276
OPTIMIZED_PO = 199

BASELINE_STOCKOUT_RATE = 15.51
OPTIMIZED_STOCKOUT_RATE = 0.27

# SKU improvement（baseline stockout rate - optimized stockout rate）
SKU_IMPROVEMENTS = [
    ("Frozen Dumplings 1kg", 0.6220),
    ("Kimchi 500g", 0.5480),
    ("Hot Pot Soup Base", 0.4904),
    ("Pineapple Cake Box", 0.2548),
    ("Thai Jasmine Rice 2kg", 0.2493),
]

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_kpi_dashboard():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

    # ---- Purchase Orders ----
    labels = ["Baseline", "Optimized"]
    po_values = [BASELINE_PO, OPTIMIZED_PO]
    x1 = [0, 0.7]

    axes[0].bar(x1, po_values, width=0.42)
    axes[0].set_xticks(x1, labels)
    axes[0].set_ylabel("Number of POs")
    axes[0].set_title("Purchase Orders")
    axes[0].set_ylim(0, max(po_values) * 1.18)

    for i, v in enumerate(po_values):
        axes[0].text(x1[i], v + max(po_values) * 0.02, str(v), ha="center")

    # ---- Stockout Rate ----
    stockout_values = [BASELINE_STOCKOUT_RATE, OPTIMIZED_STOCKOUT_RATE]
    x2 = [0, 0.7]

    axes[1].bar(x2, stockout_values, width=0.42)
    axes[1].set_xticks(x2, labels)
    axes[1].set_ylabel("Stockout Rate (%)")
    axes[1].set_title("Stockout Rate")
    axes[1].set_ylim(0, max(stockout_values) * 1.22)

    for i, v in enumerate(stockout_values):
        axes[1].text(x2[i], v + max(stockout_values) * 0.03, f"{v}%", ha="center")

    fig.suptitle("Before vs After KPI Dashboard", fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "kpi_dashboard.png"), dpi=220)
    plt.close()

def save_sku_improvement_chart():
    labels = [x[0] for x in SKU_IMPROVEMENTS]
    values = [x[1] * 100 for x in SKU_IMPROVEMENTS]  # convert to %

    plt.figure(figsize=(9, 5.5))
    y = list(range(len(labels)))

    plt.barh(y, values)
    plt.yticks(y, labels)
    plt.xlabel("Stockout Rate Improvement (%)")
    plt.title("Top SKU Stockout Improvements")
    plt.gca().invert_yaxis()  # biggest on top

    for i, v in enumerate(values):
        plt.text(v + 0.8, i, f"{v:.1f}%", va="center")

    plt.xlim(0, max(values) * 1.18)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "sku_improvement_chart.png"), dpi=220)
    plt.close()

def save_github_cover():
    fig = plt.figure(figsize=(12, 5), facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")

    title = "Asian Grocery Inventory Optimization"
    subtitle = "Simulation-based replenishment policy using Python + SQLite"

    po_reduction = (BASELINE_PO - OPTIMIZED_PO) / BASELINE_PO * 100
    stockout_reduction = (
        (BASELINE_STOCKOUT_RATE - OPTIMIZED_STOCKOUT_RATE)
        / BASELINE_STOCKOUT_RATE * 100
    )

    # ===== Title block (centered) =====
    ax.text(
        0.5, 0.80, title,
        fontsize=28, fontweight="bold",
        ha="center", va="center",
        color="#000000",
        transform=ax.transAxes
    )

    ax.text(
        0.5, 0.68, subtitle,
        fontsize=16,
        ha="center", va="center",
        color="#555555",
        transform=ax.transAxes
    )

    # ===== Subtle divider line =====
    ax.hlines(
        y=0.56, xmin=0.18, xmax=0.82,
        colors="#D9D9D9", linewidth=1.2,
        transform=ax.transAxes
    )

    # ===== KPI block positions =====
    LEFT_X = 0.30
    RIGHT_X = 0.70

    # ---- Purchase Orders ----
    ax.text(
        LEFT_X, 0.43, "Purchase Orders",
        fontsize=14, fontweight="bold",
        ha="center", va="center",
        color="#222222",
        transform=ax.transAxes
    )

    ax.text(
        LEFT_X, 0.31, f"{BASELINE_PO} → {OPTIMIZED_PO}",
        fontsize=30,
        ha="center", va="center",
        color="#000000",
        transform=ax.transAxes
    )

    ax.text(
        LEFT_X, 0.20, f"{po_reduction:.1f}% reduction",
        fontsize=14,
        ha="center", va="center",
        color="#666666",
        transform=ax.transAxes
    )

    # ---- Stockout Rate ----
    ax.text(
        RIGHT_X, 0.43, "Stockout Rate",
        fontsize=14, fontweight="bold",
        ha="center", va="center",
        color="#222222",
        transform=ax.transAxes
    )

    ax.text(
        RIGHT_X, 0.31, f"{BASELINE_STOCKOUT_RATE}% → {OPTIMIZED_STOCKOUT_RATE}%",
        fontsize=30,
        ha="center", va="center",
        color="#000000",
        transform=ax.transAxes
    )

    ax.text(
        RIGHT_X, 0.20, f"{stockout_reduction:.1f}% reduction",
        fontsize=14,
        ha="center", va="center",
        color="#666666",
        transform=ax.transAxes
    )

    plt.savefig(
        os.path.join(OUTPUT_DIR, "github_cover.png"),
        dpi=220,
        facecolor="white"
    )
    plt.close()

def main():
    ensure_output_dir()
    save_kpi_dashboard()
    save_sku_improvement_chart()
    save_github_cover()

    print("Visuals generated:")
    print("- outputs/kpi_dashboard.png")
    print("- outputs/sku_improvement_chart.png")
    print("- outputs/github_cover.png")

if __name__ == "__main__":
    main()
