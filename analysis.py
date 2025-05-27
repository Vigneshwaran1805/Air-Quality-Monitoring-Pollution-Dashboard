import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load cleaned data
df = pd.read_csv("data/clean_air_quality_dataset.csv")

# AQI Trends Over Time
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x="Date", y="PM2.5", label="PM2.5", color="red")
sns.lineplot(data=df, x="Date", y="PM10", label="PM10", color="blue")
plt.title("Air Quality Index (PM2.5 & PM10) Trends Over Time")
plt.xlabel("Date")
plt.ylabel("Concentration (µg/m³)")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# City-Wise Pollution Comparison
city_avg = df.groupby("City")[["PM2.5", "PM10"]].mean().reset_index()
fig = px.bar(city_avg, x="City", y="PM2.5", title="City-wise PM2.5 Levels", color="PM2.5")
fig.show()
