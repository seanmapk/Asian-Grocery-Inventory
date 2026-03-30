import os
import matplotlib.pyplot as plt

OUTPUT_DIR = "outputs"

def save_po_chart():
    labels = ["Baseline", "Optimized"]
    values = [276, 199]
    x = [0, 0.6]   

    plt.figure(figsize=(6, 4))
    plt.bar(x, values, width=0.4) 

    plt.xticks(x, labels)
    plt.ylabel("Number of POs")
    plt.title("Purchase Orders Comparison")

    plt.ylim(0, max(values) * 1.15)

    for i, v in enumerate(values):
        plt.text(x[i], v + max(values)*0.02, str(v), ha="center")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "po_comparison.png"), dpi=200)
    plt.close()


def save_stockout_chart():
    labels = ["Baseline", "Optimized"]
    values = [15.51, 0.27]
    x = [0, 0.6]

    plt.figure(figsize=(6, 4))
    plt.bar(x, values, width=0.4)

    plt.xticks(x, labels)
    plt.ylabel("Stockout Rate (%)")
    plt.title("Stockout Rate Comparison")

    plt.ylim(0, max(values) * 1.3)

    for i, v in enumerate(values):
        plt.text(x[i], v + max(values)*0.03, f"{v}%", ha="center")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "stockout_comparison.png"), dpi=200)
    plt.close()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    save_po_chart()
    save_stockout_chart()
    print("Charts updated successfully!")


if __name__ == "__main__":
    main()

