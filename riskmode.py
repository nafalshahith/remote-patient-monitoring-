def predict_risk(row):
    score = 0

    if row["heart_rate"] > 100:
        score += 1
    if row["systolic_bp"] > 140 or row["diastolic_bp"] > 90:
        score += 1
    if row["spo2"] < 92:
        score += 1

    if score == 0:
        return "Low Risk"
    elif score == 1:
        return "Medium Risk"
    else:
        return "High Risk"

