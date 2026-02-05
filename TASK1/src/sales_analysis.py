import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create output directory if not exists
os.makedirs("outputs", exist_ok=True)

# Load dataset
df = pd.read_csv("data/online_retail.csv")

# -------------------------------
# DATA CLEANING
# -------------------------------
df.dropna(inplace=True)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Revenue'] = df['Quantity'] * df['UnitPrice']

# -------------------------------
# MONTHLY REVENUE TREND
# -------------------------------
monthly_revenue = (
    df.groupby(df['InvoiceDate'].dt.to_period('M'))['Revenue']
    .sum()
    .reset_index()
)
monthly_revenue['InvoiceDate'] = monthly_revenue['InvoiceDate'].astype(str)

plt.figure(figsize=(12,5))
plt.plot(monthly_revenue['InvoiceDate'], monthly_revenue['Revenue'])
plt.xticks(rotation=90)
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("outputs/monthly_revenue_trend.png")
plt.show()

# -------------------------------
# TOP 10 PRODUCTS BY REVENUE
# -------------------------------
top_products = (
    df.groupby('Description')['Revenue']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10,5))
top_products.plot(kind='bar')
plt.title("Top 10 Products by Revenue")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("outputs/top_products.png")
plt.show()

# -------------------------------
# TOP 10 COUNTRIES BY REVENUE
# -------------------------------
top_countries = (
    df.groupby('Country')['Revenue']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10,5))
top_countries.plot(kind='bar')
plt.title("Top 10 Countries by Revenue")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("outputs/top_countries.png")
plt.show()

print("✅ Analysis Completed Successfully!")
