import pandas as pd
import os

DATA_PATH = "../data/cleaned_crop_prices.csv"
RESULT_PATH = "../results"

def run_analysis():

    df = pd.read_csv(DATA_PATH)

    os.makedirs(RESULT_PATH, exist_ok=True)

    # -----------------------
    # Volatility by crop
    # -----------------------

    volatility_by_crop = df.groupby("Commodity")["Volatility"].mean().sort_values(ascending=False)

    print("\nAverage Volatility by Crop:")
    print(volatility_by_crop)

    volatility_by_crop.to_csv(f"{RESULT_PATH}/volatility_by_crop.csv")

    # -----------------------
    # State wise price
    # -----------------------

    state_price = df.groupby("State")["Modal_Price"].mean().sort_values(ascending=False)

    print("\nAverage Price by State:")
    print(state_price)

    state_price.to_csv(f"{RESULT_PATH}/state_price_analysis.csv")

    # -----------------------
    # Yearly price trend
    # -----------------------

    yearly_trend = df.groupby(["Year","Commodity"])["Modal_Price"].mean()

    yearly_trend.to_csv(f"{RESULT_PATH}/yearly_price_trend.csv")

    print("\nAnalysis completed!")

if __name__ == "__main__":
    run_analysis()