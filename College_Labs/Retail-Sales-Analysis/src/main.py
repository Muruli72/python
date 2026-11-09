
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, round, desc, date_format
from pathlib import Path

# Locate project and dataset
project_folder = Path(__file__).resolve().parent.parent
csv_file = project_folder / "data" / "online_retail.csv"

# Create Spark application
spark = SparkSession.builder \
    .appName("RetailSalesAnalysis") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Load retail dataset
df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(str(csv_file))

# Display original dataset information
print("\nORIGINAL DATASET")
print("Total records:", df.count())

# Remove invalid transactions and cancelled invoices
clean_df = df.filter(
    col("InvoiceNo").isNotNull() &
    (~col("InvoiceNo").startswith("C")) &
    col("Description").isNotNull() &
    col("Quantity").isNotNull() &
    (col("Quantity") > 0) &
    col("UnitPrice").isNotNull() &
    (col("UnitPrice") > 0)
)

# Calculate revenue for every transaction line
clean_df = clean_df.withColumn(
    "Revenue",
    round(col("Quantity") * col("UnitPrice"), 2)
)

# Cache cleaned data because we will reuse it
clean_df.cache()

# Count records after cleaning
clean_count = clean_df.count()

print("\nDATA CLEANING RESULTS")
print("Original records:", df.count())
print("Valid sales records:", clean_count)
print("Removed records:", df.count() - clean_count)

# Display cleaned data
print("\nCLEANED DATA")
clean_df.show(5, truncate=False)

# Calculate total revenue
print("\nTOTAL REVENUE")
clean_df.agg(
    round(sum("Revenue"), 2).alias("Total Revenue")
).show()

# Find top 10 products by revenue
print("\nTOP 10 PRODUCTS")
top_products = clean_df.groupBy(
    "StockCode", "Description"
).agg(
    sum("Quantity").alias("TotalQuantity"),
    round(sum("Revenue"), 2).alias("TotalRevenue")
).orderBy(desc("TotalRevenue"))

top_products.show(10, truncate=False)

# Find country-wise revenue
print("\nCOUNTRY-WISE REVENUE")
country_sales = clean_df.groupBy("Country").agg(
    round(sum("Revenue"), 2).alias("TotalRevenue")
).orderBy(desc("TotalRevenue"))

country_sales.show(10, truncate=False)

# Find monthly revenue
print("\nMONTHLY SALES")
monthly_sales = clean_df.withColumn(
    "Month", date_format(col("InvoiceDate"), "yyyy-MM")
).groupBy("Month").agg(
    round(sum("Revenue"), 2).alias("TotalRevenue")
).orderBy("Month")

monthly_sales.show(20, truncate=False)

# Find top 10 customers by revenue
print("\nTOP 10 CUSTOMERS")
top_customers = clean_df.filter(
    col("CustomerID").isNotNull()
).groupBy("CustomerID").agg(
    round(sum("Revenue"), 2).alias("TotalRevenue")
).orderBy(desc("TotalRevenue"))

top_customers.show(10, truncate=False)

# Save analysis reports
output_folder = project_folder / "outputs"

reports = {
    "top_products": top_products.limit(10),
    "country_sales": country_sales,
    "monthly_sales": monthly_sales,
    "top_customers": top_customers.limit(10)
}

for report_name, report_df in reports.items():
    report_df.coalesce(1).write \
        .mode("overwrite") \
        .option("header", "true") \
        .csv(str(output_folder / report_name))

print("\nALL ANALYSIS REPORTS SAVED SUCCESSFULLY!")

# Stop Spark
clean_df.unpersist()
spark.stop()
