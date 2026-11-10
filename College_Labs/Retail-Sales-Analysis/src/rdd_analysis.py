
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pathlib import Path
import re

# Locate the retail dataset
project_folder = Path(__file__).resolve().parent.parent
csv_file = project_folder / "data" / "online_retail.csv"

# Create Spark application
spark = SparkSession.builder \
    .appName("RetailRDDAnalysis") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Load product descriptions
df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(str(csv_file))

# Convert DataFrame column into an RDD
descriptions_rdd = df.select("Description") \
    .where(col("Description").isNotNull()) \
    .rdd.map(lambda row: row["Description"])

# Split descriptions into individual words
words_rdd = descriptions_rdd.flatMap(
    lambda description: re.findall(
        r"[a-zA-Z]+", description.lower()
    )
)

# Calculate frequency of each word
word_counts = words_rdd.map(
    lambda word: (word, 1)
).reduceByKey(
    lambda a, b: a + b
)

# Display total word count
print("Total Words:", words_rdd.count())

# Display number of unique words
print("Unique Words:", word_counts.count())

# Find the 20 most frequent words
top_words = word_counts.takeOrdered(
    20,
    key=lambda item: (-item[1], item[0])
)

print("\nTOP 20 MOST FREQUENT WORDS")

for word, count in top_words:
    print(word, ":", count)

# Save results
output_path = project_folder / "outputs" / "word_count"

result_df = spark.createDataFrame(
    top_words, ["Word", "Count"]
)

result_df.coalesce(1).write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv(str(output_path))

print("\nWord count report saved successfully!")

spark.stop()
