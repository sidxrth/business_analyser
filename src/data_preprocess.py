# src/data_preprocess.py
import pandas as pd

def load_data(path='data/OnlineRetail.xlsx'):
    df = pd.read_excel(path, engine='openpyxl')
    return df

def clean_data(df):
    # drop rows without CustomerID
    df = df.dropna(subset=['CustomerID'])
    # remove cancelled transactions (InvoiceNo starting with 'C')
    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
    # remove negative or zero quantity
    df = df[df['Quantity'] > 0]
    # create TotalPrice
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    # convert InvoiceDate to datetime
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    return df

if __name__ == "__main__":
    df = load_data()
    df = clean_data(df)
    print(df.shape)
    df.to_csv('data/clean_retail.csv', index=False)
    print("✅ Data preprocessing completed successfully!")

