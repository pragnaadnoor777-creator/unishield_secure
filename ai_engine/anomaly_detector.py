import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.metrics import f1_score

# 1. Enhanced Data Generation (Normal vs. Attack)
def generate_campus_data(n_samples=200):
    # Normal: Day hours, low volume, campus locations
    normal = pd.DataFrame({
        'hour': np.random.randint(8, 18, n_samples),
        'data_volume': np.random.uniform(1, 50, n_samples),
        'location_id': np.random.randint(1, 3, n_samples),
        'label': 1  # 1 = Normal
    })
    # Attack: Night hours, huge volume, remote locations
    attacks = pd.DataFrame({
        'hour': [2, 3, 1, 4],
        'data_volume': [800, 1200, 950, 1100],
        'location_id': [9, 8, 9, 7],
        'label': -1 # -1 = Anomaly
    })
    return pd.concat([normal, attacks]).sample(frac=1)

# 2. Train and Save Model
def train_model():
    df = generate_campus_data()
    # Features used for training
    features = ['hour', 'data_volume', 'location_id']
    
    # AMD Hardware Note: This model is lightweight enough to run 
    # locally on Ryzen AI NPUs for secure edge-processing.
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(df[features])
    
    # Save the model to your repository
    joblib.dump(model, 'ai_engine/anomaly_model.joblib')
    print(" Model trained and saved as 'anomaly_model.joblib'")
    
    # Evaluate (Aiming for 0.90 F1-score as per UniShield-Secure specs)
    preds = model.predict(df[features])
    score = f1_score(df['label'], preds, pos_label=-1)
    print(f" Model F1-Score: {score:.2f}")

# 3. Real-time Inference Function
def predict_risk(hour, volume, loc):
    model = joblib.load('ai_engine/anomaly_model.joblib')
    sample = np.array([[hour, volume, loc]])
    prediction = model.predict(sample)
    return " HIGH RISK" if prediction[0] == -1 else " LOW RISK"

if __name__ == "__main__":
    train_model()
    # Test an "Insider Threat" scenario
    print(f"Test Scenario (3 AM, 900MB, Loc 9): {predict_risk(3, 900, 9)}")
