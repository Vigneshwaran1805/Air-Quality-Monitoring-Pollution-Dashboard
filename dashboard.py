import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

# Load Cleaned Data
df = pd.read_csv("data/clean_air_quality_dataset.csv")
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Title
st.title("🌍 Environmental Air Quality & Pollution Dashboard")

# Sidebar Filters
st.sidebar.header("Filter Data")
selected_city = st.sidebar.selectbox("Select a City", df["City"].unique())
filtered_df = df[df["City"] == selected_city]

# ---- 1️⃣ AQI Trends Over Time ----
st.subheader(f"📈 AQI Trends Over Time for {selected_city}")
fig1 = px.line(filtered_df, x="Date", y=["PM2.5", "PM10"], 
               labels={"value": "Concentration (µg/m³)", "variable": "Pollutant"},
               title=f"PM2.5 & PM10 Levels in {selected_city}")
st.plotly_chart(fig1, use_container_width=True)

# ---- 2️⃣ City-Wise Pollution Comparison ----
st.subheader("🏙️ City-wise Pollution Comparison")
city_avg = df.groupby("City")[["PM2.5", "PM10"]].mean().reset_index()
fig2 = px.bar(city_avg, x="City", y="PM2.5", title="Average PM2.5 Levels by City", color="PM2.5")
st.plotly_chart(fig2, use_container_width=True)

# ---- 3️⃣ Correlation Between Temperature and Air Quality ----
st.subheader(f"🌡️ Correlation Between Temperature & Air Quality in {selected_city}")
fig3, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=filtered_df, x="Temperature", y="PM2.5", hue="PM2.5", palette="coolwarm", ax=ax)
ax.set_title(f"Temperature vs PM2.5 Levels in {selected_city}")
st.pyplot(fig3)

# ---- 4️⃣ Public Health Alerts ----
st.subheader("🚦 Public Health Alert System")

def aqi_alert(value):
    if value <= 50:
        return "✅ Good (Green)"
    elif value <= 100:
        return "🟡 Moderate (Yellow)"
    elif value <= 150:
        return "🟠 Unhealthy for Sensitive Groups (Orange)"
    elif value <= 200:
        return "🔴 Unhealthy (Red)"
    else:
        return "🟣 Hazardous (Purple)"

filtered_df["AQI_Alert"] = filtered_df["PM2.5"].apply(aqi_alert)
num_rows = st.slider("Select number of rows to display:", min_value=5, max_value=100, value=10, step=5)
st.write(filtered_df[["Date", "PM2.5", "AQI_Alert"]].tail(num_rows))

# ---- Run the dashboard ----
# ---- 5️⃣ City-Wide Public Health Alert System ----
st.subheader("🏙️ Overall Air Quality Status by City")

# Function to classify cities based on average PM2.5 levels
def city_aqi_alert(avg_pm25):
    if avg_pm25 <= 50:
        return "✅ Good (Green)"
    elif avg_pm25 <= 100:
        return "🟡 Moderate (Yellow)"
    elif avg_pm25 <= 150:
        return "🟠 Unhealthy for Sensitive Groups (Orange)"
    elif avg_pm25 <= 200:
        return "🔴 Unhealthy (Red)"
    else:
        return "🟣 Hazardous (Purple)"

# Calculate city-wise average PM2.5
city_avg_pm25 = df.groupby("City")["PM2.5"].mean().reset_index()
city_avg_pm25["AQI_Alert"] = city_avg_pm25["PM2.5"].apply(city_aqi_alert)

# Display city-wise air quality status
st.dataframe(city_avg_pm25.rename(columns={"PM2.5": "Avg PM2.5 Level", "AQI_Alert": "Health Alert"}), 
             height=400, use_container_width=True)
