import pandas as pd
import os

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_crop_prices.csv")
RESULT_PATH = os.path.join(BASE_DIR, "results")

def generate_insights():
    """Generate key insights from data mining analysis"""
    print("\n" + "=" * 70)
    print("FINAL INSIGHTS - FARMER INCOME RISK ANALYSIS")
    print("=" * 70)
    
    df = pd.read_csv(DATA_PATH)
    
    # Calculate Risk Index
    df['Risk_Index'] = df['Volatility'] / df['Modal_Price']
    df['Risk_Category'] = pd.cut(df['Risk_Index'], 
                                   bins=[0, 0.1, 0.25, 1.0],
                                   labels=['Low Risk', 'Medium Risk', 'High Risk'])
    
    insights = []
    
    # 1. Highest Volatility Crops
    print("\n[1] CROPS WITH HIGHEST VOLATILITY")
    print("-" * 70)
    volatile_crops = df.groupby('Commodity')['Volatility'].mean().sort_values(ascending=False).head(5)
    for crop, volatility in volatile_crops.items():
        print(f"   • {crop}: {volatility:.2f}")
        insights.append(f"Crop '{crop}' shows highest volatility ({volatility:.2f}), indicating high income risk for farmers.")
    
    # 2. Most Unstable States
    print("\n[2] STATES WITH UNSTABLE PRICES")
    print("-" * 70)
    unstable_states = df.groupby('State')['Volatility'].mean().sort_values(ascending=False).head(5)
    for state, volatility in unstable_states.items():
        print(f"   • {state}: {volatility:.2f}")
        insights.append(f"State '{state}' exhibits high price volatility ({volatility:.2f}), affecting farmer income stability.")
    
    # 3. Seasonal Patterns
    print("\n[3] SEASONAL PRICE PATTERNS")
    print("-" * 70)
    monthly_pattern = df.groupby('Month')['Modal_Price'].mean()
    peak_month = monthly_pattern.idxmax()
    low_month = monthly_pattern.idxmin()
    print(f"   • Peak prices in Month {peak_month}: ₹{monthly_pattern[peak_month]:.2f}")
    print(f"   • Lowest prices in Month {low_month}: ₹{monthly_pattern[low_month]:.2f}")
    price_diff = ((monthly_pattern[peak_month] - monthly_pattern[low_month]) / monthly_pattern[low_month]) * 100
    print(f"   • Seasonal variation: {price_diff:.1f}%")
    insights.append(f"Seasonal patterns show {price_diff:.1f}% price variation between peak and low months.")
    
    # 4. Risk Distribution
    print("\n[4] FARMER INCOME RISK CLASSIFICATION")
    print("-" * 70)
    risk_dist = df['Risk_Category'].value_counts()
    for risk_cat, count in risk_dist.items():
        pct = (count / len(df)) * 100
        print(f"   • {risk_cat}: {count} records ({pct:.1f}%)")
    insights.append(f"Risk analysis shows {risk_dist.get('High Risk', 0)} high-risk transactions affecting farmer income.")
    
    # 5. State-wise Risk
    print("\n[5] STATE-WISE RISK ASSESSMENT")
    print("-" * 70)
    state_risk = df.groupby('State')['Risk_Index'].mean().sort_values(ascending=False).head(5)
    for state, risk_idx in state_risk.items():
        print(f"   • {state}: Risk Index {risk_idx:.3f}")
        insights.append(f"State '{state}' has elevated risk index ({risk_idx:.3f}), requiring policy intervention.")
    
    # 6. Supply-Price Relationship
    print("\n[6] SUPPLY-PRICE RELATIONSHIP")
    print("-" * 70)
    supply_price = df.groupby(['Commodity', 'Year', 'Month']).agg({
        'Modal_Price': 'mean',
        'Market': 'count'
    }).reset_index()
    supply_price.rename(columns={'Market': 'Supply_Indicator'}, inplace=True)
    
    correlation = supply_price.groupby('Commodity').apply(
        lambda x: x['Supply_Indicator'].corr(x['Modal_Price'])
    ).sort_values()
    
    print(f"   • Negative correlation (supply ↑ → price ↓): {(correlation < -0.3).sum()} commodities")
    print(f"   • Positive correlation (supply ↑ → price ↑): {(correlation > 0.3).sum()} commodities")
    insights.append("Supply-price relationship shows inverse correlation for most commodities.")
    
    # 7. Price Range Analysis
    print("\n[7] PRICE RANGE ANALYSIS")
    print("-" * 70)
    price_range = df.groupby('Commodity').agg({
        'Min_Price': 'mean',
        'Max_Price': 'mean',
        'Modal_Price': 'mean'
    }).round(2)
    price_range['Range'] = price_range['Max_Price'] - price_range['Min_Price']
    price_range = price_range.sort_values('Range', ascending=False).head(5)
    print(price_range)
    insights.append("Wide price ranges indicate market inefficiency and farmer vulnerability.")
    
    # Save insights
    with open(f"{RESULT_PATH}/insights_summary.txt", 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("FARMER INCOME RISK ANALYSIS - KEY INSIGHTS\n")
        f.write("=" * 70 + "\n\n")
        for i, insight in enumerate(insights, 1):
            f.write(f"{i}. {insight}\n")
    
    print("\n" + "=" * 70)
    print("Insights saved to: insights_summary.txt")
    print("=" * 70)
    
    return insights

if __name__ == "__main__":
    generate_insights()
