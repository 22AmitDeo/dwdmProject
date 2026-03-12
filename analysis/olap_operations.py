import pandas as pd
import os

DATA_PATH = "../data/cleaned_crop_prices.csv"
RESULT_PATH = "../results/olap"

def olap_rollup(df):
    """ROLL-UP: Market → District → State"""
    print("\n" + "=" * 60)
    print("ROLL-UP: Market → District → State")
    print("=" * 60)
    
    market_level = df.groupby(['State', 'District', 'Market']).agg({
        'Modal_Price': 'mean',
        'Volatility': 'mean'
    }).round(2)
    print(f"\nMarket Level (sample):\n{market_level.head()}")
    
    district_level = df.groupby(['State', 'District']).agg({
        'Modal_Price': 'mean',
        'Volatility': 'mean'
    }).round(2)
    print(f"\nDistrict Level (sample):\n{district_level.head()}")
    
    state_level = df.groupby('State').agg({
        'Modal_Price': 'mean',
        'Volatility': 'mean'
    }).round(2)
    print(f"\nState Level:\n{state_level.head()}")
    
    return market_level, district_level, state_level

def olap_drilldown(df):
    """DRILL-DOWN: Year → Month → Day"""
    print("\n" + "=" * 60)
    print("DRILL-DOWN: Year → Month → Day")
    print("=" * 60)
    
    df['Day'] = pd.to_datetime(df['Arrival_Date']).dt.day
    
    year_level = df.groupby('Year').agg({
        'Modal_Price': 'mean',
        'Volatility': 'mean'
    }).round(2)
    print(f"\nYear Level:\n{year_level}")
    
    month_level = df.groupby(['Year', 'Month']).agg({
        'Modal_Price': 'mean',
        'Volatility': 'mean'
    }).round(2)
    print(f"\nMonth Level (sample):\n{month_level.head(10)}")
    
    day_level = df.groupby(['Year', 'Month', 'Day']).agg({
        'Modal_Price': 'mean',
        'Volatility': 'mean'
    }).round(2)
    print(f"\nDay Level (sample):\n{day_level.head(10)}")
    
    return year_level, month_level, day_level

def olap_slice(df, commodity=None):
    """SLICE: Select a single dimension value"""
    if commodity is None:
        commodity = df['Commodity'].value_counts().index[0]
    
    print("\n" + "=" * 60)
    print(f"SLICE: Commodity = '{commodity}'")
    print("=" * 60)
    
    sliced_data = df[df['Commodity'] == commodity]
    slice_summary = sliced_data.groupby(['State', 'Year']).agg({
        'Modal_Price': 'mean',
        'Volatility': 'mean'
    }).round(2)
    
    print(f"\n{commodity} Analysis (sample):\n{slice_summary.head(10)}")
    print(f"Total records: {len(sliced_data)}")
    
    return sliced_data, slice_summary

def olap_dice(df, commodity=None, state=None, year=None):
    """DICE: Multiple dimension filters"""
    if commodity is None:
        commodity = df['Commodity'].value_counts().index[0]
    if state is None:
        state = df['State'].value_counts().index[0]
    if year is None:
        year = df['Year'].max()
    
    print("\n" + "=" * 60)
    print(f"DICE: Commodity='{commodity}', State='{state}', Year={year}")
    print("=" * 60)
    
    diced_data = df[
        (df['Commodity'] == commodity) & 
        (df['State'] == state) & 
        (df['Year'] == year)
    ]
    
    if len(diced_data) > 0:
        dice_summary = diced_data.groupby(['Month', 'District']).agg({
            'Modal_Price': ['mean', 'min', 'max'],
            'Volatility': 'mean'
        }).round(2)
        print(f"\nDiced Data Summary:\n{dice_summary}")
        print(f"Total records: {len(diced_data)}")
    else:
        print(f"No data found for specified filters.")
        dice_summary = pd.DataFrame()
    
    return diced_data, dice_summary

def olap_pivot(df):
    """PIVOT: Commodity vs State"""
    print("\n" + "=" * 60)
    print("PIVOT: Commodity vs State (Average Modal Price)")
    print("=" * 60)
    
    pivot_table = df.pivot_table(
        values='Modal_Price',
        index='Commodity',
        columns='State',
        aggfunc='mean'
    ).round(2)
    
    print(f"\nPivot Table (sample):\n{pivot_table.head()}")
    return pivot_table

def run_olap_analysis():
    """Execute all OLAP operations"""
    print("\n" + "=" * 70)
    print("OLAP ANALYSIS MODULE")
    print("=" * 70)
    
    df = pd.read_csv(DATA_PATH)
    os.makedirs(RESULT_PATH, exist_ok=True)
    
    market_level, district_level, state_level = olap_rollup(df)
    market_level.to_csv(f"{RESULT_PATH}/rollup_market_level.csv")
    district_level.to_csv(f"{RESULT_PATH}/rollup_district_level.csv")
    state_level.to_csv(f"{RESULT_PATH}/rollup_state_level.csv")
    
    year_level, month_level, day_level = olap_drilldown(df)
    year_level.to_csv(f"{RESULT_PATH}/drilldown_year_level.csv")
    month_level.to_csv(f"{RESULT_PATH}/drilldown_month_level.csv")
    day_level.to_csv(f"{RESULT_PATH}/drilldown_day_level.csv")
    
    sliced_data, slice_summary = olap_slice(df)
    slice_summary.to_csv(f"{RESULT_PATH}/slice_result.csv")
    
    diced_data, dice_summary = olap_dice(df)
    if len(dice_summary) > 0:
        dice_summary.to_csv(f"{RESULT_PATH}/dice_result.csv")
    
    pivot_table = olap_pivot(df)
    pivot_table.to_csv(f"{RESULT_PATH}/pivot_commodity_state.csv")
    
    print("\n" + "=" * 70)
    print("OLAP Operations Explained:")
    print("=" * 70)
    print("""
1. ROLL-UP: Aggregates from Market → District → State
   Reduces granularity by climbing hierarchy

2. DRILL-DOWN: Disaggregates from Year → Month → Day
   Increases granularity by descending hierarchy

3. SLICE: Selects single dimension value (e.g., specific crop)
   Creates sub-cube with one dimension fixed

4. DICE: Selects multiple dimension values
   Creates smaller sub-cube with multiple constraints

5. PIVOT: Rotates data for different perspectives
   Rows and columns interchanged for comparison
    """)
    
    print("\nOLAP Analysis Completed!")
    print(f"Results saved to: {RESULT_PATH}")

if __name__ == "__main__":
    run_olap_analysis()
