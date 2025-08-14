import pandas as pd
import os

#read raw data
file_path="DATA/Raw/online_retail.csv"
df=pd.read_csv(file_path)

#print(df)

# Drop null CustomerIDs
df = df.dropna(subset=['CustomerID'])

# Remove canceled/returned transactions (Quantity < 0)
df = df[df['Quantity'] > 0]

# Add 'TotalPrice' column
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

import datetime as dt

NOW = dt.datetime(2011, 12, 10)  # Based on data's latest date
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# rfm table
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (NOW - x.max()).days,
    'InvoiceNo': pd.Series.nunique,
    'TotalPrice': 'sum'
}).rename(columns={
    'InvoiceDate': 'Recency',
    'InvoiceNo': 'Frequency',
    'TotalPrice': 'Monetary'
})

rfm['R'] = pd.qcut(rfm['Recency'], 4, labels=[4,3,2,1])
rfm['F'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1,2,3,4])
rfm['M'] = pd.qcut(rfm['Monetary'], 4, labels=[1,2,3,4])

rfm['RFM_Score'] = rfm['R'].astype(str) + rfm['F'].astype(str) + rfm['M'].astype(str)

def segment(row):
    if row['RFM_Score'] == '444':
        return 'Champions'
    elif row['R'] == 4 and row['F'] >= 3:
        return 'Loyal Customers'
    elif row['R'] >= 3 and row['M'] >= 3:
        return 'Potential Loyalist'
    elif row['R'] == 1:
        return 'Churned'
    else:
        return 'Others'

rfm['Segment'] = rfm.apply(segment, axis=1)

rfm.to_csv("data/Processed/processed_data.csv", index=False)