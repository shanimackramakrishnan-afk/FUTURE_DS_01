import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -------------------------
# SET PROJECT ROOT PATH
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "funnel_data.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "outputs")

os.makedirs(OUTPUT_PATH, exist_ok=True)

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv(DATA_PATH)

# Standardize column names (prevents KeyError)
df.columns = df.columns.str.lower().str.strip()

# -------------------------
# FUNNEL METRICS (SAFE)
# -------------------------
df['visitor_to_lead_conversion'] = df['leads'] / df['visitors']
df['lead_to_customer_conversion'] = df['customers'] / df['leads'].replace(0, pd.NA)
df['overall_conversion'] = df['customers'] / df['visitors']

# -------------------------
# FUNNEL OVERVIEW
# -------------------------
funnel_totals = df[['visitors', 'leads', 'customers']].sum()

plt.figure(figsize=(6,4))
sns.barplot(x=funnel_totals.index, y=funnel_totals.values)
plt.title("Overall Marketing Funnel")
plt.ylabel("Users")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PATH, "funnel_overview.png"))
plt.show()

# -------------------------
# CONVERSION BY CHANNEL
# -------------------------
plt.figure(figsize=(10,5))
sns.barplot(
    data=df,
    x='channel',
    y='overall_conversion'
)
plt.title("Overall Conversion Rate by Channel")
plt.ylabel("Conversion Rate")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PATH, "conversion_by_channel.png"))
plt.show()

# -------------------------
# DROP-OFF ANALYSIS (FAST & CLEAN)
# -------------------------

df['dropoff_visitors_to_leads'] = df['visitors'] - df['leads']
df['dropoff_leads_to_customers'] = df['leads'] - df['customers']

dropoff_channel = (
    df.groupby('channel', as_index=False)
      .agg(
          Visitors_to_Leads=('dropoff_visitors_to_leads', 'sum'),
          Leads_to_Customers=('dropoff_leads_to_customers', 'sum')
      )
)

# Convert to long format for seaborn
dropoff_long = dropoff_channel.melt(
    id_vars='channel',
    var_name='Funnel Stage',
    value_name='Users Lost'
)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=dropoff_long,
    y='channel',
    x='Users Lost',
    hue='Funnel Stage'
)

plt.title("Drop-Off Analysis by Funnel Stage (Channel-wise)")
plt.xlabel("Users Lost")
plt.ylabel("Channel")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PATH, "dropoff_analysis.png"))
plt.show()
