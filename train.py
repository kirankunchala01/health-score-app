import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# Function to normalize values
def normalize(value, normal, severe):
    return min(1, max(0, abs(value - normal) / severe))

# Function to calculate health severity score
def calculate_health_score(hr, bp, rr, spo2, temp, glucose, age):
    # Normalize values
    P1 = normalize(hr, 80, 50)        # Heart Rate
    P2 = normalize(bp, 110, 70)       # Blood Pressure
    P3 = normalize(rr, 16, 20)        # Respiratory Rate
    P4 = normalize(spo2, 95, 10)      # Oxygen Saturation
    P5 = normalize(temp, 37, 4)       # Body Temperature
    P6 = normalize(glucose, 100, 200) # Glucose Level
    P7 = normalize(age, 50, 25)       # Age

    # Assign weights
    weights = {
        "heart_rate": 0.15, "blood_pressure": 0.20, "respiratory_rate": 0.15,
        "oxygen_saturation": 0.15, "body_temperature": 0.10, "glucose": 0.10, "age": 0.15
    }

    # Calculate weighted sum
    score = (
        weights["heart_rate"] * P1 +
        weights["blood_pressure"] * P2 +
        weights["respiratory_rate"] * P3 +
        weights["oxygen_saturation"] * P4 +
        weights["body_temperature"] * P5 +
        weights["glucose"] * P6 +
        weights["age"] * P7
    ) * 100  # Convert to percentage

    return round(score, 2)

# Generate synthetic training data
np.random.seed(42)
data_size = 5000
df = pd.DataFrame({
    "heart_rate": np.random.randint(50, 180, size=data_size),
    "blood_pressure": np.random.randint(80, 200, size=data_size),
    "respiratory_rate": np.random.randint(10, 35, size=data_size),
    "oxygen_saturation": np.random.randint(85, 100, size=data_size),
    "body_temperature": np.random.uniform(35, 40, size=data_size),
    "glucose": np.random.randint(60, 300, size=data_size),
    "age": np.random.randint(18, 90, size=data_size)
})

# Calculate severity score for each patient
df["health_score"] = df.apply(lambda row: calculate_health_score(
    row["heart_rate"], row["blood_pressure"], row["respiratory_rate"],
    row["oxygen_saturation"], row["body_temperature"], row["glucose"], row["age"]
), axis=1)

# Train/Test Split
X = df.drop(columns=["health_score"])
y = df["health_score"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Machine Learning Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the Model
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"Model MAE: {mae:.2f}")

# Save the trained model
joblib.dump(model, "health_model.pkl")
print("Model saved as health_model.pkl")





