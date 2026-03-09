import joblib
import numpy as np

# Load trained model
model = joblib.load("random_forest_addiction_model.pkl")

print("\n📱 Digital Addiction Predictor\n")

# Take user input
daily_screen_time = int(input("Daily screen time (hours): "))
gaming_time = int(input("Gaming time (hours): "))
social_media_usage = int(input("Social media usage (hours): "))
app_sessions = int(input("Number of app sessions per day: "))
notifications = int(input("Number of notifications per day: "))
night_usage = int(input("Night usage (hours): "))

# Arrange input in correct order
input_data = np.array([
    daily_screen_time,
    gaming_time,
    social_media_usage,
    app_sessions,
    notifications,
    night_usage
]).reshape(1, -1)

# Predict
prediction = model.predict(input_data)[0]

# Output result
if prediction == 1:
    print("\n🔴 Prediction: USER IS ADDICTED")
else:
    print("\n🟢 Prediction: USER IS NOT ADDICTED")
