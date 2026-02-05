import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create outputs folder
os.makedirs("outputs", exist_ok=True)

# Load data
df = pd.read_csv("data/telco_customer_churn.csv")

# ---------------------------
# DATA CLEANING
# ---------------------------
df.dropna(inplace=True)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df.dropna(inplace=True)

# Convert churn to binary
df['ChurnFlag'] = df['Churn'].map({'Yes': 1, 'No': 0})

# ---------------------------
# OVERALL CHURN RATE
# ---------------------------
churn_rate = df['ChurnFlag'].mean()

plt.figure(figsize=(6,4))
sns.barplot(x=['Churn Rate'], y=[churn_rate])
plt.title("Overall Customer Churn Rate")
plt.ylabel("Rate")
plt.savefig("outputs/churn_rate.png")
plt.show()

# ---------------------------
# CHURN BY TENURE (CUSTOMER LIFETIME)
# ---------------------------
df['TenureGroup'] = pd.cut(
    df['tenure'],
    bins=[0,12,24,36,48,60,72],
    labels=['0-1 yr','1-2 yr','2-3 yr','3-4 yr','4-5 yr','5+ yr']
)

tenure_churn = df.groupby('TenureGroup')['ChurnFlag'].mean()

tenure_churn.plot(kind='bar', figsize=(8,5))
plt.title("Churn Rate by Customer Tenure")
plt.ylabel("Churn Rate")
plt.savefig("outputs/retention_by_tenure.png")
plt.show()

# ---------------------------
# CHURN BY SEGMENT
# ---------------------------
segment_churn = df.groupby('Contract')['ChurnFlag'].mean()

segment_churn.plot(kind='bar', figsize=(8,5))
plt.title("Churn Rate by Contract Type")
plt.ylabel("Churn Rate")
plt.savefig("outputs/churn_by_segment.png")
plt.show()

# ---------------------------
# COHORT ANALYSIS (Signup Month Proxy)
# ---------------------------
df['SignupMonth'] = pd.cut(df['tenure'],
                           bins=[0,12,24,36,48,60,72],
                           labels=['New','1Y','2Y','3Y','4Y','5Y+'])

cohort = pd.crosstab(df['SignupMonth'], df['Churn'])

sns.heatmap(cohort, annot=True, fmt='d', cmap='Blues')
plt.title("Customer Retention Cohort Overview")
plt.savefig("outputs/cohort_retention.png")
plt.show()

print("✅ Churn & Retention Analysis Completed")
