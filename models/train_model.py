import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import joblib


#read the data
data=pd.read_csv("data/Processed/processed_data.csv")

# Assuming rfm_df is already computed

rfm = data[['Recency', 'Frequency', 'Monetary']]

scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm)


#kmeans---
kmeans = KMeans(n_clusters=4, random_state=42)
rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)

joblib.dump(kmeans, "models/kmeans_model.pkl")

rfm.to_csv("data/Processed/rfm_clustered.csv", index=False)


