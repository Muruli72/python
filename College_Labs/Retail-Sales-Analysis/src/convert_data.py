
import csv
from pathlib import Path
from openpyxl import load_workbook

# Locate the project folder and dataset
project_folder = Path(__file__).resolve().parent.parent

excel_file = project_folder / "data" / "online_retail.xlsx"
csv_file = project_folder / "data" / "online_retail.csv"

# Open Excel in read-only mode to save memory
workbook = load_workbook(excel_file, read_only=True, data_only=True)
sheet = workbook.active

# Convert Excel rows into CSV rows
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    for row in sheet.iter_rows(values_only=True):
        writer.writerow(row)

workbook.close()

print("Excel converted to CSV successfully!")
print("CSV saved at:", csv_file)
