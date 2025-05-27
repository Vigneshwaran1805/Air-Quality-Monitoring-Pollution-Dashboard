import pandas as pd

def load_and_clean_data(file_path):
    df = pd.read_csv(file_path)

    # Convert date to datetime format
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Handle missing values using forward fill
    df.fillna(method='ffill', inplace=True)

    # Convert numeric columns
    numeric_cols = ["PM2.5", "PM10", "CO", "NO2", "Ozone", "Temperature"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove invalid values
    df = df[(df["PM2.5"] >= 0) & (df["PM10"] >= 0) & (df["CO"] >= 0)]
    
    return df

df = load_and_clean_data("data/air_quality_dataset.csv")
df.to_csv("data/clean_air_quality_dataset.csv", index=False)

print("Data cleaning complete! Cleaned file saved in /data/")
