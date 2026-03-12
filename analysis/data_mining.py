import pandas as pd
import numpy as np
import os

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_crop_prices.csv")
RESULT_PATH = os.path.join(BASE_DIR, "results", "data_mining")

def calculate_risk_index(df):
    """Calculate Risk Index = Volatility / Modal_Price"""
    df['Risk_Index'] = df['Volatility'] / df['Modal_Price']
    df['Risk_Category'] = pd.cut(df['Risk_Index'], 
                                   bins=[0, 0.1, 0.25, 1.0],
                                   labels=['Low Risk', 'Medium Risk', 'High Risk'])
    return df

def identify_volatile_crops(df, top_n=10):
    """Identify most volatile crops"""
    volatile_crops = df.groupby('Commodity').agg({
        'Volatility': 'mean',
        'Modal_Price': 'mean',
        'Risk_Index': 'mean'
    }).sort_values('Volatility', ascending=False).head(top_n)
    return volatile_crops

def state_volatility_comparison(df):
    """Compare volatility across states"""
    state_volatility = df.groupby('State').agg({
        'Volatility': ['mean', 'std', 'max'],
        'Modal_Price': 'mean',
        'Risk_Index': 'mean'
    }).round(2)
    state_volatility.columns = ['Avg_Volatility', 'Std_Volatility', 'Max_Volatility', 
                                 'Avg_Price', 'Avg_Risk_Index']
    return state_volatility.sort_values('Avg_Volatility', ascending=False)

def seasonal_price_variation(df):
    """Analyze seasonal patterns in prices"""
    monthly_pattern = df.groupby('Month').agg({
        'Modal_Price': 'mean',
        'Volatility': 'mean'
    }).round(2)
    return monthly_pattern

def supply_price_relationship(df):
    """Analyze relationship between supply (arrival) and price"""
    supply_price = df.groupby(['Commodity', 'Year', 'Month']).agg({
        'Modal_Price': 'mean',
        'Volatility': 'mean',
        'Market': 'count'
    }).reset_index()
    supply_price.rename(columns={'Market': 'Supply_Indicator'}, inplace=True)
    
    correlation = supply_price.groupby('Commodity').apply(
        lambda x: x['Supply_Indicator'].corr(x['Modal_Price'])
    ).sort_values()
    return correlation

def run_data_mining():
    """Execute all data mining analyses"""
    print("=" * 60)
    print("DATA MINING MODULE - Farmer Income Risk Analysis")
    print("=" * 60)
    
    df = pd.read_csv(DATA_PATH)
    os.makedirs(RESULT_PATH, exist_ok=True)
    
    df = calculate_risk_index(df)
    df.to_csv(f"{RESULT_PATH}/data_with_risk_index.csv", index=False)
    
    print("\n[1/5] Risk Distribution:")
    print(df['Risk_Category'].value_counts())
    
    print("\n[2/5] Top 10 Most Volatile Crops:")
    volatile_crops = identify_volatile_crops(df)
    print(volatile_crops)
    volatile_crops.to_csv(f"{RESULT_PATH}/volatile_crops.csv")
    
    print("\n[3/5] State-wise Volatility:")
    state_volatility = state_volatility_comparison(df)
    print(state_volatility.head(10))
    state_volatility.to_csv(f"{RESULT_PATH}/state_volatility.csv")
    
    print("\n[4/5] Monthly Price Pattern:")
    monthly_pattern = seasonal_price_variation(df)
    print(monthly_pattern)
    monthly_pattern.to_csv(f"{RESULT_PATH}/monthly_pattern.csv")
    
    print("\n[5/5] Supply-Price Correlation:")
    correlation = supply_price_relationship(df)
    print(correlation.head(10))
    correlation.to_csv(f"{RESULT_PATH}/supply_price_correlation.csv")
    
    print("\n" + "=" * 60)
    print("Data Mining Analysis Completed!")
    print("=" * 60)
    
    return df

if __name__ == "__main__":
    run_data_mining()
