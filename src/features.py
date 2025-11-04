# src/features.py
import pandas as pd
import datetime as dt

def create_rfm(df, cutoff_date):
    snapshot_date = pd.Timestamp(cutoff_date) + pd.Timedelta(days=1)
    rfm = df[df['InvoiceDate'] <= pd.Timestamp(cutoff_date)].groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalPrice': 'sum'
    }).reset_index()
    rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
    return rfm

def create_label(df, cutoff_date, label_window_days=30):
    cutoff = pd.Timestamp(cutoff_date)
    window_end = cutoff + pd.Timedelta(days=label_window_days)
    future_df = df[(df['InvoiceDate'] > cutoff) & (df['InvoiceDate'] <= window_end)]
    buyers = future_df['CustomerID'].unique()
    return buyers

if __name__ == "__main__":
    df = pd.read_csv('data/clean_retail.csv', parse_dates=['InvoiceDate'])
    cutoff_date = '2010-12-31'   # example: change based on your data
    rfm = create_rfm(df, cutoff_date)
    buyers = create_label(df, cutoff_date)
    rfm['NextMonthPurchase'] = rfm['CustomerID'].isin(buyers).astype(int)
    rfm.to_csv('data/rfm_labeled.csv', index=False)
    print(rfm.head())
