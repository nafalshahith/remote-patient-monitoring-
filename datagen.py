import random
import pandas as pd
from datetime import datetime

def stream_data(patients=5):
    data = []
    for i in range(1, patients + 1):
        data.append({
            "timestamp": datetime.now(),
            "patient_id": f"P{i}",
            "heart_rate": random.randint(60, 120),
            "systolic_bp": random.randint(90, 160),
            "diastolic_bp": random.randint(60, 100),
            "spo2": random.randint(88, 100)
        })
    return pd.DataFrame(data)
