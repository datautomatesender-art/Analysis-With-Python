from importlib.metadata import files
from data_profiling import report
from data_profiling.config import Report
import pandas as pd
import numpy as np
import data_profiling
from data_profiling import ProfileReport
from google.colab import files
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams['figure.figsize'] = (12, 5)
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'

uploaded = files.upload()

df = pd.read_excel('Product-Sales-Region.xlsx')

profile = ProfileReport(df, title="Product Sales Region Data Profiling Report", explorative=True)
profile.to_file('report.html')
files.download('report.html')

df.shape

df.dtypes

df.isnull().sum()

df.head(10)

missing = df.isnull().mean()*100
print(missing[missing>0].sort_values)

n_dupes = df.duplicated().sum()

n_dupes

df = df.copy()

categorical_cols = ['Promotion']
df[categorical_cols] = df[categorical_cols].fillna('No Promotion')

print(df.isnull().sum()[df.isnull().sum() > 0])

profile = ProfileReport(df, title="Product Sales Region Data Profiling Report", explorative=True)
profile.to_file('report.html')
files.download('report.html')

df.head(5)

df["Date"] = pd.to_datetime(df["Date"])

df["Month"] = df["Date"].dt.month

df.head(5)

df["Month_Name"] = df["Date"].dt.month_name()

df["Month_Year"] = df["Date"].dt.strftime("%b %Y")

df.head(5)

monthly = df.groupby("Month")["Quantity"].sum()

monthly.plot(kind="bar", title="Monthly Sales")

# Reuse your cleaned df from before, or rebuild:
df['Date'] = pd.to_datetime(df['Date'])
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df['DeliveryDate'] = pd.to_datetime(df['DeliveryDate'])
df['Month_Year'] = df['Date'].dt.to_period('M').astype(str)
df['Month_Name'] = df['Date'].dt.month_name()
df['Promotion'] = df['Promotion'].fillna('No Promotion').replace('', 'No Promotion')
df['DeliveryDays'] = (df['DeliveryDate'] - df['OrderDate']).dt.days
df['NetRevenue'] = np.where(df['Returned'] == 1, 0, df['TotalPrice'])

monthly = df.groupby('Month_Year')['TotalPrice'].sum().sort_index()

plt.figure()
monthly.plot(kind='line', marker='o', color='steelblue')
plt.title('Monthly Sales Revenue Trend')
plt.xlabel('Month')
plt.ylabel('Revenue (TotalPrice)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure()
monthly.plot(kind='bar', color='teal')
plt.title('Monthly Revenue')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

region_rev = df.groupby('Region')['TotalPrice'].sum().sort_values(ascending=False)

plt.figure()
sns.barplot(x=region_rev.index, y=region_rev.values, palette='viridis')
plt.title('Revenue by Region')
plt.xlabel('Region')
plt.ylabel('Revenue')
for i, v in enumerate(region_rev.values):
    plt.text(i, v, f'{v:,.0f}', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.show()

product_rev = df.groupby('Product')['TotalPrice'].sum().sort_values(ascending=False)

plt.figure()
sns.barplot(x=product_rev.index, y=product_rev.values, palette='magma')
plt.title('Revenue by Product')
plt.xlabel('Product')
plt.ylabel('Revenue')
plt.tight_layout()
plt.show()

pivot = pd.pivot_table(df, index='Region', columns='Product',
                       values='TotalPrice', aggfunc='sum', fill_value=0)

plt.figure(figsize=(12, 5))
sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlGnBu', linewidths=0.5)
plt.title('Revenue Heatmap: Region × Product')
plt.tight_layout()
plt.show()

sp = df.groupby('Salesperson')['TotalPrice'].agg(['sum','mean','count']).sort_values('sum', ascending=False)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sns.barplot(x=sp.index, y=sp['sum'], ax=axes[0], palette='Blues_d')
axes[0].set_title('Total Revenue per Salesperson')
axes[0].tick_params(axis='x', rotation=45)

sns.barplot(x=sp.index, y=sp['mean'], ax=axes[1], palette='Greens_d')
axes[1].set_title('Average Order Value per Salesperson')
axes[1].tick_params(axis='x', rotation=45)

sns.barplot(x=sp.index, y=sp['count'], ax=axes[2], palette='Oranges_d')
axes[2].set_title('Number of Orders per Salesperson')
axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

promo = df.groupby('Promotion')['TotalPrice'].agg(['sum','mean','count']).sort_values('sum', ascending=False)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
sns.barplot(x=promo.index, y=promo['sum'], ax=axes[0], palette='viridis')
axes[0].set_title('Total Revenue by Promotion')

sns.barplot(x=promo.index, y=promo['mean'], ax=axes[1], palette='coolwarm')
axes[1].set_title('Average Order Value by Promotion')

sns.barplot(x=promo.index, y=promo['count'], ax=axes[2], palette='Set2')
axes[2].set_title('Order Count by Promotion')

for ax in axes:
    ax.tick_params(axis='x', rotation=30)
plt.tight_layout()
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(16, 5))

# Return rate by Region
ret_region = df.groupby('Region')['Returned'].mean().sort_values(ascending=False) * 100
sns.barplot(x=ret_region.index, y=ret_region.values, ax=axes[0], palette='Reds')
axes[0].set_title('Return Rate by Region (%)')
axes[0].set_ylabel('Return Rate (%)')

# Return rate by Product
ret_product = df.groupby('Product')['Returned'].mean().sort_values(ascending=False) * 100
sns.barplot(x=ret_product.index, y=ret_product.values, ax=axes[1], palette='Reds')
axes[1].set_title('Return Rate by Product (%)')
axes[1].tick_params(axis='x', rotation=30)

plt.tight_layout()
plt.show()

num_cols = ['Quantity', 'UnitPrice', 'Discount', 'TotalPrice', 'ShippingCost', 'DeliveryDays']

df[num_cols].hist(bins=30, figsize=(15, 10), color='steelblue', edgecolor='white')
plt.suptitle('Distribution of Numeric Features', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(16, 5))

sns.boxplot(data=df, x='Region', y='TotalPrice', ax=axes[0], palette='Set3')
axes[0].set_title('TotalPrice Distribution by Region')

sns.boxplot(data=df, x='Product', y='TotalPrice', ax=axes[1], palette='Set2')
axes[1].set_title('TotalPrice Distribution by Product')
axes[1].tick_params(axis='x', rotation=30)

plt.tight_layout()
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

df['PaymentMethod'].value_counts().plot(
    kind='pie', autopct='%1.1f%%', ax=axes[0], title='Payment Method Share', ylabel='')

df['CustomerType'].value_counts().plot(
    kind='pie', autopct='%1.1f%%', ax=axes[1], title='Customer Type Share', ylabel='')

plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
corr = df[['Quantity','UnitPrice','Discount','TotalPrice','ShippingCost','DeliveryDays','Returned']].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, linewidths=0.5)
plt.title('Correlation Matrix (Numeric Features)')
plt.tight_layout()
plt.show()

pivot_rm = pd.pivot_table(df, index='Region', columns='Month_Year',
                          values='TotalPrice', aggfunc='sum', fill_value=0)

plt.figure(figsize=(14, 5))
sns.heatmap(pivot_rm, cmap='rocket_r', linewidths=0.3)
plt.title('Monthly Revenue by Region')
plt.xlabel('Month')
plt.ylabel('Region')
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
sns.scatterplot(data=df, x='Discount', y='TotalPrice', hue='CustomerType', alpha=0.6)
plt.title('Discount vs TotalPrice')
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 5))
sns.violinplot(data=df, x='Region', y='DeliveryDays', palette='Pastel1', inner='quartile')
plt.title('Delivery Time Distribution by Region')
plt.ylabel('Delivery Days')
plt.tight_layout()
plt.show()

fig, axes = plt.subplots(2, 2, figsize=(16, 10))

df.groupby('Region')['TotalPrice'].sum().sort_values().plot(
    kind='barh', ax=axes[0,0], color='teal', title='Revenue by Region')

df.groupby('Product')['TotalPrice'].sum().sort_values().plot(
    kind='barh', ax=axes[0,1], color='coral', title='Revenue by Product')

df.groupby('Month_Year')['TotalPrice'].sum().plot(
    kind='line', marker='o', ax=axes[1,0], color='steelblue', title='Monthly Revenue')

df.groupby('Promotion')['TotalPrice'].sum().plot(
    kind='bar', ax=axes[1,1], color='mediumpurple', title='Revenue by Promotion')

plt.tight_layout()
plt.show()