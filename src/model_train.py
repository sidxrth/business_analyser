import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os
import matplotlib.pyplot as plt

# 1️⃣ Load and Clean Data
print("📦 Loading dataset...")
df = pd.read_excel('data/OnlineRetail.xlsx', engine='openpyxl')

# Drop rows with missing CustomerID
df = df.dropna(subset=['CustomerID'])

# Convert date column
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Create TotalPrice
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

print("✅ Data loaded and cleaned.")

# 2️⃣ Create Enhanced Customer Features (RFM + More)
print("⚙️ Creating enhanced customer features...")
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

# Base grouping
customer_features = df.groupby('CustomerID').agg({
    'InvoiceDate': [
        lambda x: (snapshot_date - x.max()).days,  # Recency
        lambda x: (x.max() - x.min()).days,        # Customer Tenure
        'count'                                   # Frequency (# of purchases)
    ],
    'TotalPrice': 'sum',                          # Monetary (total spend)
    'StockCode': pd.Series.nunique,               # Unique products
    'InvoiceNo': pd.Series.nunique,               # Number of orders
    'Quantity': 'sum'                             # Total quantity
})

# Rename columns
customer_features.columns = [
    'Recency', 'CustomerTenure', 'Frequency', 'Monetary',
    'UniqueProducts', 'NumOrders', 'TotalQuantity'
]

# Average Order Value
customer_features['AOV'] = customer_features['Monetary'] / customer_features['NumOrders']

# Average Basket Size
customer_features['AvgBasketSize'] = customer_features['TotalQuantity'] / customer_features['NumOrders']

# Country (region)
country_data = df.groupby('CustomerID')['Country'].first()
customer_features = customer_features.merge(country_data, on='CustomerID', how='left')

# Average Purchase Interval (avg days between orders)
purchase_intervals = (
    df.groupby('CustomerID')['InvoiceDate']
    .apply(lambda x: x.sort_values().diff().dt.days.mean())
    .fillna(0)
)
customer_features['AvgPurchaseInterval'] = purchase_intervals

# Last Month Spend (total spend in last 30 days)
last_month_cutoff = snapshot_date - pd.Timedelta(days=30)
last_month_spend = df[df['InvoiceDate'] > last_month_cutoff].groupby('CustomerID')['TotalPrice'].sum()
customer_features['LastMonthSpend'] = customer_features.index.map(last_month_spend).fillna(0)

# Return Rate (% of cancelled orders)
returns = df[df['InvoiceNo'].astype(str).str.startswith('C')].groupby('CustomerID')['InvoiceNo'].count()
total_orders = df.groupby('CustomerID')['InvoiceNo'].count()
return_rate = (returns / total_orders).fillna(0)
customer_features['ReturnRate'] = customer_features.index.map(return_rate)

# Define Target: PurchasedAgain (Recency <= 30)
customer_features['PurchasedAgain'] = np.where(customer_features['Recency'] <= 30, 1, 0)

print("✅ Enhanced customer features created successfully!")
print(customer_features.head())

# 3️⃣ Prepare Data for Modeling
# Drop non-numeric columns (Country will be encoded later)
X = customer_features[[
    'Recency', 'CustomerTenure', 'Frequency', 'Monetary', 'UniqueProducts',
    'NumOrders', 'AOV', 'AvgBasketSize', 'AvgPurchaseInterval',
    'LastMonthSpend', 'ReturnRate'
]]

y = customer_features['PurchasedAgain']

# Handle missing / infinite values
X = X.replace([np.inf, -np.inf], np.nan)
X = X.fillna(0)

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42, stratify=y
)

# 4️⃣ Train Model
print("🚀 Training logistic regression model...")
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
print("✅ Model training completed!")

# 5️⃣ Evaluate Model
y_pred = model.predict(X_test)
print("\n✅ Classification Report:")
print(classification_report(y_test, y_pred))
print("✅ Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# 6️⃣ Feature Importance Visualization
coef = model.coef_[0]
features = X.columns
plt.figure(figsize=(10,6))
plt.barh(features, coef)
plt.title("Feature Importance (Logistic Regression Coefficients)")
plt.xlabel("Coefficient Value")
plt.ylabel("Feature")
plt.tight_layout()

# Save plot instead of showing
os.makedirs("model", exist_ok=True)
plt.savefig("model/feature_importance.png")
plt.close()
print("📊 Feature importance plot saved at: model/feature_importance.png")

# 7️⃣ Save Model and Scaler
joblib.dump(model, "model/logistic_model.joblib")
joblib.dump(scaler, "model/scaler.joblib")

print("✅ Model saved successfully at: model/logistic_model.joblib")
print("✅ Scaler saved successfully at: model/scaler.joblib")
print("🎉 Training complete! Your enhanced predictive model is ready.")
