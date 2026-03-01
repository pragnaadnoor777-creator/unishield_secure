import pandas as pd
from sklearn.ensemble import IsolationForest
import numpy as np

# 1. Simulate University Access Logs (Replace with real data later)
# Features: [Hour of Day, Data Volume (MB), Location_Score (1-10)]
data = {
    'hour': [9, 10, 11, 14, 15, 16, 2, 3, 12, 13],
    'data_volume': [5, 12, 8, 15, 7, 10, 500, 450, 5, 8],
    'location_id': [1, 1, 2, 1, 1, 2, 9, 9, 1, 1] 
}
df = pd.DataFrame(data)

# 2. Initialize the Anomaly Detection Model
# Contamination defines the expected percentage of outliers in the data
model = IsolationForest(contamination=0.2, random_state=42)

# 3. Train the model on "Normal" Behavior
model.fit(df[['hour', 'data_volume', 'location_id']])

# 4. Predict Anomalies
# -1 indicates an anomaly, 1 indicates normal behavior
df['anomaly_score'] = model.predict(df[['hour', 'data_volume', 'location_id']])

# 5. Output Results
print("University Access Risk Report:")
print(df)

# Logic: Flagging a 3 AM bulk download from an unknown location
def check_access(hour, volume, location):
    query = np.array([[hour, volume, location]])
    prediction = model.predict(query)
    if prediction[0] == -1:
        return "⚠️ ALERT: Highly suspicious activity detected. Access Blocked."
    return "✅ Access Granted."

# Example Test
print("\nTesting Real-time Access Request:")
print(check_access(3, 800, 10)) # Simulated "Insider Threat"
