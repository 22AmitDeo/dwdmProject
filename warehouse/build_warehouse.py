import pandas as pd
import os

DATA_PATH = "../data/cleaned_crop_prices.csv"
WAREHOUSE_PATH = "../warehouse"

def build_warehouse():

    df = pd.read_csv(DATA_PATH)

    os.makedirs(WAREHOUSE_PATH, exist_ok=True)

    # -------------------
    # Time Dimension
    # -------------------

    time_dim = df[["Arrival_Date","Year","Month","Day"]].drop_duplicates()
    time_dim["Time_ID"] = range(1, len(time_dim) + 1)

    time_dim.to_csv(f"{WAREHOUSE_PATH}/time_dimension.csv", index=False)

    # -------------------
    # Location Dimension
    # -------------------

    location_dim = df[["State","District","Market"]].drop_duplicates()
    location_dim["Location_ID"] = range(1, len(location_dim) + 1)

    location_dim.to_csv(f"{WAREHOUSE_PATH}/location_dimension.csv", index=False)

    # -------------------
    # Crop Dimension
    # -------------------

    crop_dim = df[["Commodity","Variety","Grade"]].drop_duplicates()
    crop_dim["Crop_ID"] = range(1, len(crop_dim) + 1)

    crop_dim.to_csv(f"{WAREHOUSE_PATH}/crop_dimension.csv", index=False)

    # -------------------
    # Fact Table
    # -------------------

    fact_table = df[[
        "Arrival_Date",
        "State",
        "District",
        "Market",
        "Commodity",
        "Min_Price",
        "Max_Price",
        "Modal_Price",
        "Volatility"
    ]]

    fact_table.to_csv(f"{WAREHOUSE_PATH}/fact_table.csv", index=False)

    print("Warehouse tables generated!")

if __name__ == "__main__":
    build_warehouse()