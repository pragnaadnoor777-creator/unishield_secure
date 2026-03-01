import pandas as pd
import numpy as np
import joblib
import warnings
from sklearn.ensemble import IsolationForest

# Suppress feature name warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning)

def train_model():
    # Simulate University Access Logs
    data = {
        'hour': [9, 10, 11, 14, 15, 16, 2, 3, 12, 13, 11, 15],
        'data_volume': [5, 12, 8, 15, 7, 10, 500, 450, 5, 8, 10, 12],
        'location_id': [1, 1, 2, 1, 1, 2, 9, 9, 1, 1, 2, 1] 
    }
    df = pd.DataFrame(data)
    
    # Model optimized for Edge-AI (AMD Ryzen AI compatible)
    model = IsolationForest(contamination=0.15, random_state=42)
    model.fit(df[['hour', 'data_volume', 'location_id']])
    
    # Save the brain
    joblib.dump(model, 'ai_engine/anomaly_model.joblib')
    print("✅ AI Brain trained and saved as 'anomaly_model.joblib'")

def predict_risk(hour, volume, location):
    try:
        model = joblib.load('ai_engine/anomaly_model.joblib')
        query = np.array([[hour, volume, location]])
        prediction = model.predict(query)
        return "🚨 HIGH RISK" if prediction[0] == -1 else "🟢 LOW RISK"
    except:
        return "⚠️ Error: Run anomaly_detector.py first to train the model."

if __name__ == "__main__":
    train_model()