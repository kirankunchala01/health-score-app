import streamlit as st

# Function to normalize values (0 to 1 scale)
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

    # Classify health condition
    if score <= 30:
        status = "✅ Healthy"
    elif score <= 50:
        status = "⚠️ Mild Risk (Monitor)"
    elif score <= 70:
        status = "⚠️ Moderate Risk (Medical Attention Needed)"
    else:
        status = "🚨 High Risk (Critical Condition)"

    return round(score, 2), status

# Streamlit UI
st.title("🩺 Health Severity Score Calculator")

# Create input fields
heart_rate = st.number_input("Heart Rate (bpm)", min_value=30, max_value=200, value=80)
blood_pressure = st.number_input("Blood Pressure (Systolic, mmHg)", min_value=50, max_value=250, value=110)
respiratory_rate = st.number_input("Respiratory Rate (breaths/min)", min_value=5, max_value=40, value=16)
oxygen_saturation = st.number_input("Oxygen Saturation (%)", min_value=50, max_value=100, value=95)
body_temperature = st.number_input("Body Temperature (°C)", min_value=30.0, max_value=42.0, value=37.0)
glucose = st.number_input("Glucose Level (mg/dL)", min_value=50, max_value=400, value=100)
age = st.number_input("Age (years)", min_value=0, max_value=120, value=50)

# Button to calculate
if st.button("Calculate Health Score"):
    score, status = calculate_health_score(heart_rate, blood_pressure, respiratory_rate, oxygen_saturation, body_temperature, glucose, age)
    st.subheader(f"**Health Severity Score: {score}%**")
    st.write(f"**Condition:** {status}")
    
    # Display progress bar based on severity
    st.progress(int(score))