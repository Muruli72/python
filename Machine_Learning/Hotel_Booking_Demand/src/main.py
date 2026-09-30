import pandas as pd

from data_cleaning import load_data, clean_data

from visualization import (
    hotel_booking_chart,
    adr_histogram,
    scatter_plot,
    pie_chart
)

from model import train_model


# Load Dataset
print("Loading Dataset...")

df = load_data()

print("\nFirst 5 Rows:\n")
print(df.head())


# Clean Dataset
print("\nCleaning Dataset...")

df = clean_data(df)

print("\nDataset Cleaned Successfully")


# Dataset Information
print("\nDataset Shape:", df.shape)

print("\nDataset Columns:\n")
print(df.columns)

print("\nDataset Info:\n")
print(df.info())


# Visualizations
print("\nGenerating Visualizations...")

hotel_booking_chart(df)

adr_histogram(df)

scatter_plot(df)

pie_chart(df)


# Train Machine Learning Model
print("\nTraining Machine Learning Model...")

model = train_model(df)


print("\nProject Completed Successfully")