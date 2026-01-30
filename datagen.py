import random
import pandas as pd
from datetime import datetime
import time

def generate_vital_data(patient_id):
    return {
        "timestamp": datetime.now(),
        "patient_id": patient_id,
        "heart_rate": random.randint(60, 120),
        "systolic_bp": random.randint(90, 160),
        "diastolic_bp": random.randint(60, 100),
        "spo2": random.randint(88, 100)
    }

def stream_data(patients=5):
    data = []
    for i in range(1, patients + 1):
        data.append(generate_vital_data(f"P{i}"))
    return pd.DataFrame(data)

# ---------- Live simulation loop ----------
all_data = pd.DataFrame()  # store historical data

while True:
    new_data = stream_data(5)  # 5 patients
    all_data = pd.concat([all_data, new_data]).tail(500)  # keep last 500 rows
    all_data.to_csv("patient_vitals.csv", index=False)
    print("CSV updated")
    time.sleep(5)  # update every 5 seconds
