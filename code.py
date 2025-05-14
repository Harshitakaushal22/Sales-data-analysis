import zipfile
import pandas as pd
import os

# === Step 1: Define the ZIP file path ===
zip_path = r"C:\Users\workk\Downloads\superstore.csv.zip"
extract_folder = r"C:\Users\workk\Downloads\extracted_superstore_zip"

# === Step 2: Extract the ZIP file ===
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_folder)
    print("ZIP file extracted successfully.")
    print("Files inside ZIP:")
    zip_ref.printdir()

# === Step 3: Find the CSV file ===
csv_file = None
for file in os.listdir(extract_folder):
    if file.endswith(".csv"):
        csv_file = os.path.join(extract_folder, file)
        break

if csv_file is None:
    print("No CSV file found inside the ZIP.")
else:
    print(f"CSV file found: {csv_file}")

    # === Step 4: Load the CSV with pandas ===
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_file, encoding='ISO-8859-1')  # Backup encoding

    print("CSV loaded successfully.\n")

    # === Step 5: Preview the data ===
    print(df.head())
    print("\nDataset Info:")
    print(df.info())
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# === Step 6: Check for missing values ===
print("\nMissing values in each column:")
print(df.isnull().sum())

# Fill missing values: numeric with mean, categorical with mode
for col in df.columns:
    if df[col].dtype == 'object':
        df[col].fillna(df[col].mode()[0], inplace=True)
    else:
        df[col].fillna(df[col].mean(), inplace=True)

# === Step 7: Remove duplicates ===
before = df.shape[0]
df.drop_duplicates(inplace=True)
after = df.shape[0]
print(f"Removed {before - after} duplicate rows.")

# === Step 8: Handle outliers using IQR ===
def remove_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return data[(data[column] >= lower) & (data[column] <= upper)]

for col in ['Sales', 'Profit', 'Discount']:
    if col in df.columns:
        df = remove_outliers_iqr(df, col)

# === Step 9: Summary Statistics ===
print("\nSummary Statistics:")
print(df.describe())

# === Step 10: Correlation Heatmap ===
plt.figure(figsize=(10, 6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()
# === Step 11: Histograms ===
df.hist(bins=20, figsize=(14, 10), color='skyblue', edgecolor='black')
plt.suptitle("Distribution of Numerical Features")
plt.show()

# === Step 12: Boxplots ===
plt.figure(figsize=(10, 6))
sns.boxplot(data=df[['Sales', 'Profit', 'Discount']])
plt.title("Boxplot for Sales, Profit, Discount")
plt.show()

# === Step 13: Sales Over Time ===
# Try to find a date column like 'Order Date'
for col in df.columns:
    if 'date' in col.lower():
        df[col] = pd.to_datetime(df[col])
        date_col = col
        break

# Plot time series
if 'date_col' in locals():
    df.set_index(date_col).resample('M')['Sales'].sum().plot(figsize=(12,6), title='Monthly Sales Over Time')
    plt.ylabel("Total Sales")
    plt.xlabel("Date")
    plt.show()

# === Step 14: Sales by Region and Category ===
if 'Region' in df.columns:
    df.groupby('Region')['Sales'].sum().plot(kind='bar', title="Sales by Region", color='lightgreen')
    plt.ylabel("Total Sales")
    plt.show()

if 'Category' in df.columns:
    df.groupby('Category')['Sales'].sum().plot(kind='pie', autopct='%1.1f%%', title="Sales by Category", figsize=(6,6))
    plt.ylabel("")
    plt.show()