# Retail Sales Analysis using Apache PySpark

## 1. Project Overview

This project implements a real-world Big Data analytics application using **Apache Spark and PySpark**.

It analyzes online retail transaction data to understand sales performance, product popularity, customer purchasing patterns, and revenue trends across different countries and months.

The project uses the publicly available **Online Retail Dataset** from the UCI Machine Learning Repository.

The objective is to demonstrate how PySpark can process transaction data using DataFrames and RDDs and generate meaningful business insights.

## 2. Problem Statement

An online retail business generates thousands of transaction records containing product details, quantities, prices, customers, and purchase dates.

Analyzing this information manually is difficult.

This project uses Apache Spark to:

- Calculate total revenue.
- Identify top-selling products.
- Analyze country-wise revenue.
- Identify monthly sales trends.
- Find the highest-spending customers.
- Perform word frequency analysis on product descriptions using RDDs.

## 3. Dataset Information

**Dataset:** Online Retail

**Source:** UCI Machine Learning Repository

**Dataset link:** https://archive.ics.uci.edu/dataset/352/online-retail

**Original records:** 541,909

**Original file size:** Approximately 22.6 MB.

**Time period:** December 2010 – December 2011.

The dataset contains the following columns:

| Column | Description |
|---|---|
| InvoiceNo | Transaction invoice number |
| StockCode | Product identifier |
| Description | Product name |
| Quantity | Number of items purchased |
| InvoiceDate | Transaction date and time |
| UnitPrice | Price per unit |
| CustomerID | Customer identifier |
| Country | Customer's country |

The original Excel dataset is converted into CSV format before being loaded into Spark.

**Note:** Dataset files are not stored in this GitHub repository. They must be downloaded separately.

## 4. Technologies Used

- Python
- Apache Spark
- PySpark
- Spark SQL
- RDD (Resilient Distributed Dataset)
- OpenPyXL
- Git and GitHub
- VS Code

### Tested Environment

- Python 3.14.2
- PySpark 4.2.0
- Java 17
- OpenPyXL 3.1.5
- macOS

## 5. Project Structure

```text
Retail-Sales-Analysis/
│
├── data/
│   ├── online_retail.xlsx
│   └── online_retail.csv
│
├── src/
│   ├── convert_data.py
│   ├── main.py
│   └── rdd_analysis.py
│
├── outputs/
│   ├── top_products/
│   ├── country_sales/
│   ├── monthly_sales/
│   ├── top_customers/
│   └── word_count/
│
├── .gitignore
├── requirements.txt
└── README.md
```

The dataset and generated output files are excluded from Git tracking.

## 6. Installation and Configuration

### Step 1: Clone the repository

```bash
git clone https://github.com/Muruli72/python.git
```

Navigate to the project directory:

```bash
cd python/College_Labs/Retail-Sales-Analysis
```

### Step 2: Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on macOS:

```bash
source .venv/bin/activate
```

### Step 3: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Verify Java installation

```bash
java -version
```

Java 17 is used in the tested environment.

## 7. Dataset Download and Conversion

Create the data and output directories:

```bash
mkdir -p data outputs
```

Download the original Excel dataset:

```bash
curl -L --fail "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx" -o data/online_retail.xlsx
```

Convert Excel into CSV:

```bash
python src/convert_data.py
```

This program uses OpenPyXL to read the Excel worksheet and Python's CSV module to write the transaction data into a CSV file.

The generated CSV file is:

```text
data/online_retail.csv
```

## 8. Running the Project

Run the Python files in the following order.

### Program 1: Excel to CSV Conversion

```bash
python src/convert_data.py
```

Purpose:
- Read the original Excel workbook.
- Access the active worksheet.
- Read data row by row.
- Write the records into CSV format.

### Program 2: Retail Sales Analysis

```bash
python src/main.py
```

Purpose:
- Create a SparkSession.
- Load the CSV file into a Spark DataFrame.
- Clean invalid transaction records.
- Calculate transaction-level revenue.
- Perform product-wise sales analysis.
- Calculate country-wise revenue.
- Analyze monthly revenue.
- Identify top customers.
- Save the analysis reports.

### Program 3: RDD Word Count Analysis

```bash
python src/rdd_analysis.py
```

Purpose:
- Load product descriptions into a Spark DataFrame.
- Convert the Description column into an RDD.
- Split descriptions into individual words.
- Use map() to generate (word, 1) pairs.
- Use reduceByKey() to calculate word frequencies.
- Identify the 20 most frequent words.
- Save the Word Count report.

## 9. Data Cleaning

The original dataset contains cancelled transactions, negative quantities, non-positive prices, and missing values.

The following conditions are applied:

- Remove records with missing invoice numbers.
- Exclude cancelled invoices beginning with C.
- Remove records with missing product descriptions.
- Remove missing quantities and prices.
- Retain only positive quantities.
- Retain only positive unit prices.

After cleaning:

| Description | Records |
|---|---:|
| Original records | 541,909 |
| Valid sales records | 530,104 |
| Removed records | 11,805 |

Records with missing CustomerID are retained for overall sales analysis but excluded from customer-wise ranking.

## 10. Business Analysis and Results

### Total Revenue

Total revenue calculated from valid sales transactions:

**10,666,684.54**

Revenue is calculated using:

```python
Revenue = Quantity * UnitPrice
```

### Country-wise Revenue

The United Kingdom generated the highest revenue.

| Country | Revenue |
|---|---:|
| United Kingdom | 9,025,222.08 |
| Netherlands | 285,446.34 |
| EIRE | 283,453.96 |
| Germany | 228,867.14 |
| France | 209,715.11 |

### Monthly Sales Analysis

November 2011 recorded the highest monthly revenue:

**1,509,496.33**

### Customer Analysis

Customer 14646 generated the highest customer revenue:

**280,206.02**

### RDD Word Count

The RDD program produced:

| Metric | Result |
|---|---:|
| Total word occurrences | 2,303,493 |
| Unique words | 2,190 |

The 20 most frequent words are also generated and saved as a CSV report.

## 11. Output Files

The project generates the following reports:

| Output directory | Contents |
|---|---|
| outputs/top_products/ | Top 10 products |
| outputs/country_sales/ | Country-wise revenue |
| outputs/monthly_sales/ | Monthly revenue |
| outputs/top_customers/ | Top 10 customers |
| outputs/word_count/ | Top 20 word frequencies |

Spark writes CSV part files inside these directories along with its success metadata.

## 12. Apache Spark Concepts Demonstrated

This project demonstrates the following PySpark concepts:

### DataFrame Operations
- SparkSession creation
- Reading CSV files
- Schema inference
- select()
- filter()
- where()
- withColumn()
- groupBy()
- agg()
- orderBy()
- DataFrame caching

### RDD Operations
- DataFrame to RDD conversion
- map()
- flatMap()
- reduceByKey()
- count()
- takeOrdered()

### Other Concepts
- Lazy evaluation
- Spark transformations and actions
- Pair RDDs
- Data partitioning
- Saving DataFrames as CSV files

## 13. Limitations and Future Improvements

The current project runs Spark locally using local[*] execution mode.

Possible future improvements include:

- Running the application on a multi-node Spark cluster.
- Building interactive sales dashboards.
- Adding more advanced customer segmentation.
- Implementing additional RDD operations.
- Comparing DataFrame and RDD processing performance.

## 14. Conclusion

This project demonstrates the use of Apache Spark and PySpark for processing and analyzing real-world online retail transaction data.

It applies DataFrame and RDD operations to perform data cleaning, revenue calculation, product analysis, customer analysis, country-wise analysis, monthly sales analysis, and Word Count.

The project provides practical experience in Big Data processing and demonstrates how Spark can be used to extract useful business insights from transaction data.

## 15. Dataset Reference

Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository.

https://doi.org/10.24432/C5BW33

Dataset license: Creative Commons Attribution 4.0 (CC BY 4.0).
