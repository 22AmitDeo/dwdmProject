import pandas as pd
import os

DATA_PATH = "../data/crop_prices.csv"
OUTPUT_PATH = "../data/cleaned_crop_prices.csv"

def clean_dataset():

    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)

    print("Original shape:", df.shape)

    # Fix column names
    df.columns = df.columns.str.replace("_x0020_", "_")
    df.columns = df.columns.str.strip()

    # Rename columns
    rename_map = {
        "Min_Price": "Min_Price",
        "Max_Price": "Max_Price",
        "Modal_Price": "Modal_Price"
    }

    df.rename(columns=rename_map, inplace=True)

    # Convert date column
    df["Arrival_Date"] = pd.to_datetime(df["Arrival_Date"], errors="coerce")

    # Remove missing values
    df.dropna(subset=["Arrival_Date","Min_Price","Max_Price","Modal_Price"], inplace=True)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Add time features
    df["Year"] = df["Arrival_Date"].dt.year
    df["Month"] = df["Arrival_Date"].dt.month
    df["Day"] = df["Arrival_Date"].dt.day

    # Create volatility column
    df["Volatility"] = df["Max_Price"] - df["Min_Price"]

    print("Cleaned shape:", df.shape)

    os.makedirs("../data", exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("Cleaned dataset saved!")

if __name__ == "__main__":
    clean_dataset()