import pandas as pd
import numpy as np
import os

def generate_feature_dataset(input_file_path):
    """
    Reads the OnlineRetail dataset (.xlsx or .csv) and creates
    processed_customer_data.csv with key business metrics per customer.
    """

    # ✅ Check if file exists
    if not os.path.exists(input_file_path):
        raise FileNotFoundError(f"❌ File not found: {input_file_path}")

    # ✅ Read dataset (supports Excel or CSV)
    if input_file_path.endswith('.xlsx'):
        df = pd.read_excel(input_file_path)
    else:
        df = pd.read_csv(input_file_path, encoding='latin1')

    print("✅ Raw OnlineRetail data loaded successfully!")

    # ✅ Basic cleaning
    df.dropna(subset=['CustomerID'], inplace=True)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

    # ✅ Group by customer and calculate metrics
    features = df.groupby('CustomerID').agg({
        'TotalPrice': ['sum', 'mean', 'count'],
        'Quantity': 'mean',
        'InvoiceDate': ['min', 'max'],
        'Country': 'first'
    })

    # ✅ Flatten multi-index column names
    features.columns = [
        'TotalSpend', 'AOV', 'NumOrders', 'AvgBasketSize',
        'FirstPurchase', 'LastPurchase', 'Country'
    ]

    # ✅ Derived features
    features['CustomerTenure'] = (features['LastPurchase'] - features['FirstPurchase']).dt.days
    features['PurchaseInterval'] = features['CustomerTenure'] / (features['NumOrders'] - 1)
    features['PurchaseInterval'] = features['PurchaseInterval'].replace(
        [np.inf, np.nan], features['PurchaseInterval'].mean()
    )

    # ✅ Example simulated features
    features['ReturnRate'] = np.random.uniform(0, 10, len(features))          # %
    features['UniqueProducts'] = np.random.randint(1, 25, len(features))      # count
    features['LastMonthSpend'] = np.random.uniform(100, 1000, len(features))  # $

    # ✅ Reset index for saving
    features.reset_index(inplace=True)

    # ✅ Save processed dataset to project root
    output_path = os.path.join(os.path.dirname(__file__), '..', 'processed_customer_data.csv')
    features.to_csv(output_path, index=False)

    print(f"✅ Processed dataset saved at: {os.path.abspath(output_path)}")
    return features


# ------------------------------------------------------------
# 🚀 MAIN EXECUTION
# ------------------------------------------------------------
if __name__ == "__main__":
    base_path = os.path.join(os.path.dirname(__file__), '..', 'data')
    excel_path = os.path.join(base_path, 'OnlineRetail.xlsx')
    csv_path = os.path.join(base_path, 'OnlineRetail.csv')

    if os.path.exists(excel_path):
        print("📘 Found OnlineRetail.xlsx — loading Excel dataset...")
        generate_feature_dataset(excel_path)

    elif os.path.exists(csv_path):
        print("📗 Found OnlineRetail.csv — loading CSV dataset...")
        generate_feature_dataset(csv_path)

    else:
        print("⚠️ Please place your OnlineRetail.xlsx or OnlineRetail.csv inside the 'data' folder.")
