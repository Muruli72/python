
import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

project_folder = Path(__file__).resolve().parent.parent

output_folder = project_folder / "outputs"
figure_folder = project_folder / "figures"

figure_folder.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. READ PYSPARK OUTPUT CSV FILES
# --------------------------------------------------

def read_report(report_name):
    folder = output_folder / report_name
    csv_files = sorted(folder.glob("part-*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"No Spark CSV report found in {folder}. "
            "Run the corresponding PySpark program first."
        )

    with open(csv_files[0], "r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def number(value):
    return float(value)


def save_figure(fig, filename):
    path = figure_folder / filename

    fig.savefig(
        path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)
    print("Saved:", path)


plt.rcParams.update({
    "figure.figsize": (11, 6),
    "font.size": 10,
    "axes.titlesize": 16
})


# --------------------------------------------------
# FIGURE 1: MONTHLY RETAIL REVENUE TREND
# --------------------------------------------------

monthly = read_report("monthly_sales")

months = [row["Month"] for row in monthly]
revenues = [number(row["TotalRevenue"]) for row in monthly]

fig, ax = plt.subplots()

ax.plot(months, revenues, marker="o", linewidth=2)

ax.set_title("Monthly Retail Revenue Trend (Dec 2010 - Dec 2011)")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue")
ax.tick_params(axis="x", rotation=45)
ax.grid(alpha=0.3)

save_figure(fig, "figure_01_monthly_revenue.png")


# --------------------------------------------------
# FIGURE 2: COUNTRY-WISE RETAIL REVENUE
# --------------------------------------------------

countries = read_report("country_sales")
countries = sorted(
    countries,
    key=lambda row: number(row["TotalRevenue"]),
    reverse=True
)[:10]

country_names = [row["Country"] for row in countries]
country_revenue = [
    number(row["TotalRevenue"]) for row in countries
]

fig, ax = plt.subplots()

ax.barh(country_names[::-1], country_revenue[::-1])

ax.set_title("Country-wise Retail Revenue Analysis")
ax.set_xlabel("Total Revenue")
ax.set_ylabel("Country")
ax.grid(axis="x", alpha=0.3)

save_figure(fig, "figure_02_country_revenue.png")


# --------------------------------------------------
# FIGURE 3: TOP 10 REVENUE-GENERATING ENTRIES
# --------------------------------------------------

products = read_report("top_products")

products = sorted(
    products,
    key=lambda row: number(row["TotalRevenue"]),
    reverse=True
)[:10]

product_names = [
    row["Description"][:32] for row in products
]

product_revenue = [
    number(row["TotalRevenue"]) for row in products
]

fig, ax = plt.subplots()

ax.barh(product_names[::-1], product_revenue[::-1])

ax.set_title("Top 10 Revenue-Generating Product Entries")
ax.set_xlabel("Total Revenue")
ax.set_ylabel("Product Description / Entry")
ax.grid(axis="x", alpha=0.3)

save_figure(fig, "figure_03_top_products.png")


# --------------------------------------------------
# FIGURE 4: REVENUE SHARE OF TOP 10 ENTRIES
# --------------------------------------------------

product_labels = [
    row["StockCode"] for row in products
]

product_values = [
    number(row["TotalRevenue"]) for row in products
]

fig, ax = plt.subplots()

ax.pie(
    product_values,
    labels=product_labels,
    autopct="%1.1f%%",
    startangle=90,
    pctdistance=0.8
)

centre_circle = plt.Circle((0, 0), 0.55, color="white")
ax.add_artist(centre_circle)

ax.set_title("Revenue Share by Top 10 Product Entries")

save_figure(fig, "figure_04_revenue_share.png")


# --------------------------------------------------
# FIGURE 5: TOP 10 CUSTOMERS
# --------------------------------------------------

customers = read_report("top_customers")

customers = sorted(
    customers,
    key=lambda row: number(row["TotalRevenue"]),
    reverse=True
)[:10]

customer_ids = [
    row["CustomerID"] for row in customers
]

customer_revenue = [
    number(row["TotalRevenue"]) for row in customers
]

fig, ax = plt.subplots()

ax.barh(customer_ids[::-1], customer_revenue[::-1])

ax.set_title("Top 10 Revenue-Generating Customers")
ax.set_xlabel("Total Revenue")
ax.set_ylabel("Customer ID")
ax.grid(axis="x", alpha=0.3)

save_figure(fig, "figure_05_top_customers.png")


# --------------------------------------------------
# FIGURE 6: INTERNATIONAL SALES MARKETS
# --------------------------------------------------

export_markets = [
    row for row in read_report("country_sales")
    if row["Country"] != "United Kingdom"
]

export_markets = sorted(
    export_markets,
    key=lambda row: number(row["TotalRevenue"]),
    reverse=True
)[:10]

market_names = [
    row["Country"] for row in export_markets
]

market_revenue = [
    number(row["TotalRevenue"]) for row in export_markets
]

fig, ax = plt.subplots()

ax.barh(market_names[::-1], market_revenue[::-1])

ax.set_title("Top 10 International Retail Markets")
ax.set_xlabel("Total Revenue")
ax.set_ylabel("Country (excluding United Kingdom)")
ax.grid(axis="x", alpha=0.3)

save_figure(fig, "figure_06_international_markets.png")


# --------------------------------------------------
# FIGURE 7: TOP 20 FREQUENT WORDS
# --------------------------------------------------

words = read_report("word_count")

words = sorted(
    words,
    key=lambda row: int(row["Count"]),
    reverse=True
)[:20]

word_names = [row["Word"] for row in words]
word_frequencies = [int(row["Count"]) for row in words]

fig, ax = plt.subplots()

ax.barh(word_names[::-1], word_frequencies[::-1])

ax.set_title("Top 20 Frequent Product Description Words")
ax.set_xlabel("Word Frequency")
ax.set_ylabel("Word")
ax.grid(axis="x", alpha=0.3)

save_figure(fig, "figure_07_word_count.png")


# --------------------------------------------------
# HELPER FUNCTIONS FOR ARCHITECTURE DIAGRAMS
# --------------------------------------------------

def draw_box(ax, x, y, width, height, label):

    box = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.02",
        linewidth=1.5,
        facecolor="#e8f1fb",
        edgecolor="#28527a"
    )

    ax.add_patch(box)

    ax.text(
        x + width / 2,
        y + height / 2,
        label,
        ha="center",
        va="center",
        fontsize=9,
        wrap=True
    )


def draw_arrow(ax, start, end):

    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops=dict(
            arrowstyle="->",
            linewidth=1.5
        )
    )


# --------------------------------------------------
# FIGURE 8: SYSTEM ARCHITECTURE
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(13, 7))

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

ax.set_title(
    "System Architecture: Retail Sales Big Data Analytics",
    pad=20
)

# Source layer
draw_box(ax, 0.04, 0.76, 0.17, 0.12, "Excel Dataset\nonline_retail.xlsx")
draw_box(ax, 0.29, 0.76, 0.18, 0.12, "convert_data.py\nOpenPyXL + CSV")
draw_box(ax, 0.55, 0.76, 0.15, 0.12, "CSV Dataset")
draw_box(ax, 0.78, 0.76, 0.18, 0.12, "Spark Application\nSparkSession")

draw_arrow(ax, (0.21, 0.82), (0.29, 0.82))
draw_arrow(ax, (0.47, 0.82), (0.55, 0.82))
draw_arrow(ax, (0.70, 0.82), (0.78, 0.82))

# DataFrame pipeline
ax.text(0.5, 0.63, "DATAFRAME ANALYSIS PIPELINE",
        ha="center", weight="bold")

draw_box(ax, 0.12, 0.43, 0.21, 0.12, "DataFrame Loading\nand Data Cleaning")
draw_box(ax, 0.40, 0.43, 0.23, 0.12, "Revenue and\nBusiness Analysis")
draw_box(ax, 0.72, 0.43, 0.19, 0.12, "Business CSV\nReports")

draw_arrow(ax, (0.85, 0.76), (0.23, 0.55))
draw_arrow(ax, (0.33, 0.49), (0.40, 0.49))
draw_arrow(ax, (0.63, 0.49), (0.72, 0.49))

# RDD pipeline
ax.text(0.5, 0.32, "RDD WORD COUNT PIPELINE",
        ha="center", weight="bold")

draw_box(ax, 0.12, 0.10, 0.21, 0.12, "Description Column\nRDD Conversion")
draw_box(ax, 0.40, 0.10, 0.23, 0.12, "map() / flatMap()\nreduceByKey()")
draw_box(ax, 0.72, 0.10, 0.19, 0.12, "Word Count\nCSV Report")

draw_arrow(ax, (0.62, 0.76), (0.23, 0.22))
draw_arrow(ax, (0.33, 0.16), (0.40, 0.16))
draw_arrow(ax, (0.63, 0.16), (0.72, 0.16))

save_figure(fig, "figure_08_system_architecture.png")


# --------------------------------------------------
# FIGURE 9: END-TO-END PROJECT WORKFLOW
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(9, 10))

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

ax.set_title(
    "End-to-End Retail Analytics Project Workflow",
    pad=20
)

steps = [
    "1. Download Online Retail Dataset",
    "2. Convert Excel Dataset into CSV",
    "3. Create SparkSession",
    "4. Load CSV into Spark DataFrame",
    "5. Clean Missing and Invalid Records",
    "6. Calculate Revenue",
    "7. Perform Business Analysis",
    "8. Execute RDD Word Count",
    "9. Generate and Save CSV Reports"
]

y_positions = [
    0.88, 0.78, 0.68, 0.58, 0.48,
    0.38, 0.28, 0.18, 0.08
]

for i, (step, y) in enumerate(zip(steps, y_positions)):

    draw_box(ax, 0.20, y, 0.60, 0.065, step)

    if i < len(steps) - 1:
        draw_arrow(
            ax,
            (0.50, y),
            (0.50, y_positions[i + 1] + 0.065)
        )

save_figure(fig, "figure_09_project_workflow.png")


# --------------------------------------------------
# FIGURE 10: PROJECT DEVELOPMENT GANTT CHART
# --------------------------------------------------

# These are illustrative project phases, not measured
# historical durations. Adjust them to your actual timeline.

tasks = [
    ("Dataset acquisition and setup", 0, 1),
    ("Excel to CSV conversion", 1, 1),
    ("Spark loading and cleaning", 2, 1),
    ("Retail business analysis", 3, 2),
    ("RDD Word Count implementation", 5, 1),
    ("Documentation and GitHub", 6, 1)
]

fig, ax = plt.subplots(figsize=(11, 6))

for index, (task, start, duration) in enumerate(tasks):

    ax.barh(
        index,
        duration,
        left=start,
        height=0.5
    )

ax.set_yticks(range(len(tasks)))
ax.set_yticklabels([task[0] for task in tasks])

ax.invert_yaxis()

ax.set_xlabel("Illustrative project work units")
ax.set_title("Retail Sales Analytics Project Development Timeline")

ax.set_xlim(0, 7)
ax.set_xticks(range(8))
ax.grid(axis="x", alpha=0.3)

ax.text(
    0.5,
    -0.14,
    "Illustrative sequence only — replace durations with actual project records.",
    transform=ax.transAxes,
    ha="center",
    fontsize=9
)

save_figure(fig, "figure_10_project_gantt.png")


# --------------------------------------------------
# COMPLETION MESSAGE
# --------------------------------------------------

print("\nALL 10 FIGURES GENERATED SUCCESSFULLY!")

print("\nFigure directory:", figure_folder)
