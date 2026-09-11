Product Sales Region Data Analysis

Overview

This notebook performs exploratory data analysis (EDA) on a product sales dataset loaded from an Excel file. It generates a data profiling report, handles missing values, engineers date‑based features, and produces a wide range of visualizations to uncover insights about revenue, regions, products, salespeople, promotions, returns, delivery times, and customer behavior.

Requirements
Python 3.x
pandas
numpy
ydata-profiling (or fg-data-profiling for goofle colab)
matplotlib
seaborn
google.colab (only if running in Google Colab)

Install the core packages with:

bash
pip install pandas numpy ydata-profiling matplotlib seaborn

HOW TO RUN

Open the notebook in Google Colab (or Jupyter).
When prompted, upload the Product-Sales-Region.xlsx file.
Run all cells sequentially.
The script will generate report.html and display numerous plots inline.

DATA

The Excel file is expected to contain columns such as:

Date, OrderDate, DeliveryDate

Product, Region, Salesperson

Quantity, UnitPrice, Discount, TotalPrice, ShippingCost

Promotion, Returned, PaymentMethod, CustomerType

ANAYLYSIS STEPS

1. Import libraries and set plot styles.

2. Upload and read the Excel file.

3. Generate initial profiling report.

4. Inspect data shape, types, missing values, duplicates.

5. Impute missing Promotion values with 'No Promotion'.

6. Generate updated profiling report.

7. Convert dates and extract month, month name, month‑year.

8. Calculate delivery days and net revenue (unused).

9. Plot monthly sales quantity and revenue.

10. Analyze revenue by region, product, and salesperson.

11. Examine promotion effectiveness.

12. Compute return rates by region and product.

13. Visualize distributions, correlations, and relationships.

14. Generate a 2×2 summary dashboard.

Output
report.html: Interactive data profiling report.

Multiple matplotlib / seaborn plots displayed inline.