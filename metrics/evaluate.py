import pandas as pd
import os
import json

# Load your clustered data
rfm = pd.read_csv("data/Processed/rfm_clustered.csv")

# Aggregate cluster metrics
cluster_summary = rfm.groupby('Cluster').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': 'mean',
    'Cluster': 'count'
}).rename(columns={"Cluster": "Count"}).reset_index()

# Ensure metrics folder exists
os.makedirs("metrics", exist_ok=True)

# Convert to dict and save as JSON
metrics_file = "metrics/cluster_metrics.json"
cluster_summary.to_dict(orient='records')
with open(metrics_file, "w") as f:
    json.dump(cluster_summary.to_dict(orient='records'), f, indent=4)

print("Metrics saved to", metrics_file)

