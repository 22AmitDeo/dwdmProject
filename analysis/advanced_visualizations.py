import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_crop_prices.csv")
RESULT_PATH = os.path.join(BASE_DIR, "results", "advanced_visualizations")

def setup_style():
    """Configure visualization style"""
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (14, 8)
    plt.rcParams['font.size'] = 10

def plot_price_distribution_histogram(df):
    """
    Histogram / Distribution Graph
    Shows how frequently certain price ranges occur and overall variability
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Modal Price Distribution
    axes[0, 0].hist(df['Modal_Price'], bins=50, color='#3498db', edgecolor='black', alpha=0.7)
    axes[0, 0].set_xlabel('Modal Price (Rs.)', fontsize=11, fontweight='bold')
    axes[0, 0].set_ylabel('Frequency', fontsize=11, fontweight='bold')
    axes[0, 0].set_title('Distribution of Modal Prices', fontsize=12, fontweight='bold')
    axes[0, 0].axvline(df['Modal_Price'].mean(), color='red', linestyle='--', 
                       linewidth=2, label=f'Mean: Rs.{df["Modal_Price"].mean():.2f}')
    axes[0, 0].axvline(df['Modal_Price'].median(), color='green', linestyle='--', 
                       linewidth=2, label=f'Median: Rs.{df["Modal_Price"].median():.2f}')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Volatility Distribution
    axes[0, 1].hist(df['Volatility'], bins=50, color='#e74c3c', edgecolor='black', alpha=0.7)
    axes[0, 1].set_xlabel('Volatility (Rs.)', fontsize=11, fontweight='bold')
    axes[0, 1].set_ylabel('Frequency', fontsize=11, fontweight='bold')
    axes[0, 1].set_title('Distribution of Price Volatility', fontsize=12, fontweight='bold')
    axes[0, 1].axvline(df['Volatility'].mean(), color='red', linestyle='--', 
                       linewidth=2, label=f'Mean: Rs.{df["Volatility"].mean():.2f}')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. Min Price Distribution
    axes[1, 0].hist(df['Min_Price'], bins=50, color='#2ecc71', edgecolor='black', alpha=0.7)
    axes[1, 0].set_xlabel('Minimum Price (Rs.)', fontsize=11, fontweight='bold')
    axes[1, 0].set_ylabel('Frequency', fontsize=11, fontweight='bold')
    axes[1, 0].set_title('Distribution of Minimum Prices', fontsize=12, fontweight='bold')
    axes[1, 0].grid(True, alpha=0.3)
    
    # 4. Max Price Distribution
    axes[1, 1].hist(df['Max_Price'], bins=50, color='#f39c12', edgecolor='black', alpha=0.7)
    axes[1, 1].set_xlabel('Maximum Price (Rs.)', fontsize=11, fontweight='bold')
    axes[1, 1].set_ylabel('Frequency', fontsize=11, fontweight='bold')
    axes[1, 1].set_title('Distribution of Maximum Prices', fontsize=12, fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.suptitle('Price Distribution Analysis - Frequency and Variability', 
                 fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig(f"{RESULT_PATH}/01_price_distribution_histogram.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("[OK] Saved: 01_price_distribution_histogram.png")

def plot_price_vs_arrival_date(df):
    """
    Line Graph - Price vs Arrival Date
    Illustrates price fluctuations over time, identifying seasonal variations
    """
    df['Arrival_Date'] = pd.to_datetime(df['Arrival_Date'])
    df_sorted = df.sort_values('Arrival_Date')
    
    # Get top 5 commodities
    top_commodities = df['Commodity'].value_counts().head(5).index.tolist()
    
    fig, axes = plt.subplots(2, 1, figsize=(16, 12))
    
    # 1. Overall Price Trend
    daily_avg = df_sorted.groupby('Arrival_Date')['Modal_Price'].agg(['mean', 'std']).reset_index()
    
    axes[0].plot(daily_avg['Arrival_Date'], daily_avg['mean'], 
                 marker='o', color='#3498db', linewidth=2, markersize=6, label='Average Price')
    axes[0].fill_between(daily_avg['Arrival_Date'], 
                         daily_avg['mean'] - daily_avg['std'],
                         daily_avg['mean'] + daily_avg['std'],
                         alpha=0.2, color='#3498db', label='±1 Std Dev')
    axes[0].set_xlabel('Arrival Date', fontsize=11, fontweight='bold')
    axes[0].set_ylabel('Modal Price (Rs.)', fontsize=11, fontweight='bold')
    axes[0].set_title('Price Fluctuations Over Time - All Commodities', fontsize=12, fontweight='bold')
    axes[0].legend(loc='best', fontsize=10)
    axes[0].grid(True, alpha=0.3)
    axes[0].tick_params(axis='x', rotation=45)
    
    # 2. Commodity-wise Price Trends
    for commodity in top_commodities:
        commodity_data = df_sorted[df_sorted['Commodity'] == commodity]
        commodity_daily = commodity_data.groupby('Arrival_Date')['Modal_Price'].mean().reset_index()
        axes[1].plot(commodity_daily['Arrival_Date'], commodity_daily['Modal_Price'], 
                     marker='o', linewidth=2, markersize=5, label=commodity)
    
    axes[1].set_xlabel('Arrival Date', fontsize=11, fontweight='bold')
    axes[1].set_ylabel('Modal Price (Rs.)', fontsize=11, fontweight='bold')
    axes[1].set_title('Price Trends by Commodity - Top 5 Commodities', fontsize=12, fontweight='bold')
    axes[1].legend(loc='best', fontsize=10)
    axes[1].grid(True, alpha=0.3)
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.suptitle('Temporal Price Analysis - Seasonal Variations and Long-term Trends', 
                 fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(f"{RESULT_PATH}/02_price_vs_arrival_date.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("[OK] Saved: 02_price_vs_arrival_date.png")

def plot_geographical_price_variation(df):
    """
    Bar Chart / Box Plot - Price variation across markets and districts
    Shows geographical variations in agricultural pricing
    """
    fig, axes = plt.subplots(2, 2, figsize=(18, 14))
    
    # 1. Average Price by State (Bar Chart)
    state_prices = df.groupby('State')['Modal_Price'].mean().sort_values(ascending=False).head(15)
    colors = plt.cm.viridis(np.linspace(0, 1, len(state_prices)))
    axes[0, 0].barh(range(len(state_prices)), state_prices.values, color=colors)
    axes[0, 0].set_yticks(range(len(state_prices)))
    axes[0, 0].set_yticklabels(state_prices.index)
    axes[0, 0].set_xlabel('Average Modal Price (Rs.)', fontsize=11, fontweight='bold')
    axes[0, 0].set_ylabel('State', fontsize=11, fontweight='bold')
    axes[0, 0].set_title('Average Price by State (Top 15)', fontsize=12, fontweight='bold')
    axes[0, 0].grid(axis='x', alpha=0.3)
    
    # 2. Average Price by District (Bar Chart)
    district_prices = df.groupby('District')['Modal_Price'].mean().sort_values(ascending=False).head(15)
    colors = plt.cm.plasma(np.linspace(0, 1, len(district_prices)))
    axes[0, 1].barh(range(len(district_prices)), district_prices.values, color=colors)
    axes[0, 1].set_yticks(range(len(district_prices)))
    axes[0, 1].set_yticklabels(district_prices.index)
    axes[0, 1].set_xlabel('Average Modal Price (Rs.)', fontsize=11, fontweight='bold')
    axes[0, 1].set_ylabel('District', fontsize=11, fontweight='bold')
    axes[0, 1].set_title('Average Price by District (Top 15)', fontsize=12, fontweight='bold')
    axes[0, 1].grid(axis='x', alpha=0.3)
    
    # 3. Price Distribution by State (Box Plot)
    top_states = df['State'].value_counts().head(8).index.tolist()
    state_data = df[df['State'].isin(top_states)]
    state_data_sorted = state_data.sort_values('State')
    
    bp1 = axes[1, 0].boxplot([state_data_sorted[state_data_sorted['State'] == state]['Modal_Price'].values 
                               for state in sorted(top_states)],
                              labels=sorted(top_states),
                              patch_artist=True,
                              showmeans=True)
    
    for patch, color in zip(bp1['boxes'], plt.cm.Set3(np.linspace(0, 1, len(top_states)))):
        patch.set_facecolor(color)
    
    axes[1, 0].set_xlabel('State', fontsize=11, fontweight='bold')
    axes[1, 0].set_ylabel('Modal Price (Rs.)', fontsize=11, fontweight='bold')
    axes[1, 0].set_title('Price Distribution by State (Box Plot)', fontsize=12, fontweight='bold')
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].grid(axis='y', alpha=0.3)
    
    # 4. Price Distribution by District (Box Plot)
    top_districts = df['District'].value_counts().head(8).index.tolist()
    district_data = df[df['District'].isin(top_districts)]
    district_data_sorted = district_data.sort_values('District')
    
    bp2 = axes[1, 1].boxplot([district_data_sorted[district_data_sorted['District'] == district]['Modal_Price'].values 
                               for district in sorted(top_districts)],
                              labels=sorted(top_districts),
                              patch_artist=True,
                              showmeans=True)
    
    for patch, color in zip(bp2['boxes'], plt.cm.Set2(np.linspace(0, 1, len(top_districts)))):
        patch.set_facecolor(color)
    
    axes[1, 1].set_xlabel('District', fontsize=11, fontweight='bold')
    axes[1, 1].set_ylabel('Modal Price (Rs.)', fontsize=11, fontweight='bold')
    axes[1, 1].set_title('Price Distribution by District (Box Plot)', fontsize=12, fontweight='bold')
    axes[1, 1].tick_params(axis='x', rotation=45)
    axes[1, 1].grid(axis='y', alpha=0.3)
    
    plt.suptitle('Geographical Price Variation Analysis - Regional Market Conditions', 
                 fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(f"{RESULT_PATH}/03_geographical_price_variation.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("[OK] Saved: 03_geographical_price_variation.png")

def plot_market_price_comparison(df):
    """
    Additional: Market-level price comparison
    Shows price differences across specific markets
    """
    fig, axes = plt.subplots(1, 2, figsize=(18, 7))
    
    # 1. Average Price by Market (Top 20)
    market_prices = df.groupby('Market')['Modal_Price'].mean().sort_values(ascending=False).head(20)
    colors = plt.cm.coolwarm(np.linspace(0, 1, len(market_prices)))
    axes[0].barh(range(len(market_prices)), market_prices.values, color=colors)
    axes[0].set_yticks(range(len(market_prices)))
    axes[0].set_yticklabels(market_prices.index, fontsize=9)
    axes[0].set_xlabel('Average Modal Price (Rs.)', fontsize=11, fontweight='bold')
    axes[0].set_ylabel('Market', fontsize=11, fontweight='bold')
    axes[0].set_title('Average Price by Market (Top 20)', fontsize=12, fontweight='bold')
    axes[0].grid(axis='x', alpha=0.3)
    
    # 2. Volatility by Market (Top 20)
    market_volatility = df.groupby('Market')['Volatility'].mean().sort_values(ascending=False).head(20)
    colors = plt.cm.RdYlGn_r(np.linspace(0, 1, len(market_volatility)))
    axes[1].barh(range(len(market_volatility)), market_volatility.values, color=colors)
    axes[1].set_yticks(range(len(market_volatility)))
    axes[1].set_yticklabels(market_volatility.index, fontsize=9)
    axes[1].set_xlabel('Average Volatility (Rs.)', fontsize=11, fontweight='bold')
    axes[1].set_ylabel('Market', fontsize=11, fontweight='bold')
    axes[1].set_title('Price Volatility by Market (Top 20)', fontsize=12, fontweight='bold')
    axes[1].grid(axis='x', alpha=0.3)
    
    plt.suptitle('Market-Level Price Analysis - Demand, Supply, and Transportation Factors', 
                 fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(f"{RESULT_PATH}/04_market_price_comparison.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("[OK] Saved: 04_market_price_comparison.png")

def plot_price_range_analysis(df):
    """
    Additional: Price range analysis showing Min, Modal, Max prices
    """
    top_commodities = df['Commodity'].value_counts().head(10).index.tolist()
    commodity_prices = df[df['Commodity'].isin(top_commodities)].groupby('Commodity').agg({
        'Min_Price': 'mean',
        'Modal_Price': 'mean',
        'Max_Price': 'mean'
    }).sort_values('Modal_Price', ascending=False)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    x = np.arange(len(commodity_prices))
    width = 0.25
    
    bars1 = ax.bar(x - width, commodity_prices['Min_Price'], width, 
                   label='Min Price', color='#2ecc71', alpha=0.8)
    bars2 = ax.bar(x, commodity_prices['Modal_Price'], width, 
                   label='Modal Price', color='#3498db', alpha=0.8)
    bars3 = ax.bar(x + width, commodity_prices['Max_Price'], width, 
                   label='Max Price', color='#e74c3c', alpha=0.8)
    
    ax.set_xlabel('Commodity', fontsize=11, fontweight='bold')
    ax.set_ylabel('Price (Rs.)', fontsize=11, fontweight='bold')
    ax.set_title('Price Range Analysis - Min, Modal, and Max Prices by Commodity', 
                 fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(commodity_prices.index, rotation=45, ha='right')
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{RESULT_PATH}/05_price_range_analysis.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("[OK] Saved: 05_price_range_analysis.png")

def generate_geographical_analysis_summary(df):
    """Generate summary statistics for geographical analysis"""
    summary = []
    
    summary.append("=" * 80)
    summary.append("GEOGRAPHICAL PRICE VARIATION ANALYSIS - SUMMARY")
    summary.append("=" * 80)
    
    # State-level analysis
    summary.append("\n1. STATE-LEVEL ANALYSIS")
    summary.append("-" * 80)
    state_stats = df.groupby('State')['Modal_Price'].agg(['mean', 'std', 'min', 'max', 'count'])
    state_stats = state_stats.sort_values('mean', ascending=False).head(10)
    summary.append("\nTop 10 States by Average Price:")
    summary.append(state_stats.to_string())
    
    # District-level analysis
    summary.append("\n\n2. DISTRICT-LEVEL ANALYSIS")
    summary.append("-" * 80)
    district_stats = df.groupby('District')['Modal_Price'].agg(['mean', 'std', 'min', 'max', 'count'])
    district_stats = district_stats.sort_values('mean', ascending=False).head(10)
    summary.append("\nTop 10 Districts by Average Price:")
    summary.append(district_stats.to_string())
    
    # Market-level analysis
    summary.append("\n\n3. MARKET-LEVEL ANALYSIS")
    summary.append("-" * 80)
    market_stats = df.groupby('Market')['Modal_Price'].agg(['mean', 'std', 'min', 'max', 'count'])
    market_stats = market_stats.sort_values('mean', ascending=False).head(10)
    summary.append("\nTop 10 Markets by Average Price:")
    summary.append(market_stats.to_string())
    
    # Price variation analysis
    summary.append("\n\n4. PRICE VARIATION ACROSS REGIONS")
    summary.append("-" * 80)
    summary.append(f"\nOverall Price Statistics:")
    summary.append(f"  - National Average Price: Rs.{df['Modal_Price'].mean():.2f}")
    summary.append(f"  - National Std Deviation: Rs.{df['Modal_Price'].std():.2f}")
    summary.append(f"  - Coefficient of Variation: {(df['Modal_Price'].std() / df['Modal_Price'].mean() * 100):.2f}%")
    
    summary.append(f"\n  - Highest State Average: Rs.{state_stats['mean'].iloc[0]:.2f} ({state_stats.index[0]})")
    summary.append(f"  - Lowest State Average: Rs.{state_stats['mean'].iloc[-1]:.2f} ({state_stats.index[-1]})")
    summary.append(f"  - State Price Range: Rs.{state_stats['mean'].iloc[0] - state_stats['mean'].iloc[-1]:.2f}")
    
    # Factors affecting geographical variation
    summary.append("\n\n5. FACTORS AFFECTING GEOGRAPHICAL PRICE VARIATION")
    summary.append("-" * 80)
    summary.append("""
Demand Factors:
  - Population density and urban concentration
  - Consumer preferences and dietary habits
  - Income levels and purchasing power
  - Festival and seasonal demand patterns

Supply Factors:
  - Local production and crop yields
  - Storage and warehousing facilities
  - Agricultural infrastructure
  - Climatic conditions and soil quality

Transportation Costs:
  - Distance from production centers
  - Road connectivity and infrastructure
  - Fuel costs and logistics
  - Cold chain availability for perishables

Regional Market Conditions:
  - Market competition and trader networks
  - Government interventions and subsidies
  - Minimum Support Price (MSP) implementation
  - Market information systems
  - Local taxes and regulations
    """)
    
    summary.append("\n6. KEY INSIGHTS")
    summary.append("-" * 80)
    
    # Calculate price disparity
    max_state_price = state_stats['mean'].max()
    min_state_price = state_stats['mean'].min()
    price_disparity = ((max_state_price - min_state_price) / min_state_price) * 100
    
    summary.append(f"\n  - Price Disparity Across States: {price_disparity:.1f}%")
    summary.append(f"  - Number of States Analyzed: {df['State'].nunique()}")
    summary.append(f"  - Number of Districts Analyzed: {df['District'].nunique()}")
    summary.append(f"  - Number of Markets Analyzed: {df['Market'].nunique()}")
    
    summary.append("\n  - Geographical variations reflect:")
    summary.append("    * Regional supply-demand imbalances")
    summary.append("    * Transportation and logistics costs")
    summary.append("    * Local market efficiency")
    summary.append("    * Infrastructure development levels")
    
    summary.append("\n" + "=" * 80)
    
    return "\n".join(summary)

def run_advanced_visualizations():
    """Execute all advanced visualizations"""
    print("\n" + "=" * 70)
    print("ADVANCED VISUALIZATIONS - DISTRIBUTION & GEOGRAPHICAL ANALYSIS")
    print("=" * 70)
    
    df = pd.read_csv(DATA_PATH)
    os.makedirs(RESULT_PATH, exist_ok=True)
    setup_style()
    
    print("\nGenerating visualizations...")
    
    # 1. Price Distribution Histogram
    print("\n[1/5] Creating price distribution histograms...")
    plot_price_distribution_histogram(df)
    
    # 2. Price vs Arrival Date
    print("\n[2/5] Creating temporal price analysis...")
    plot_price_vs_arrival_date(df)
    
    # 3. Geographical Price Variation
    print("\n[3/5] Creating geographical price variation analysis...")
    plot_geographical_price_variation(df)
    
    # 4. Market Price Comparison
    print("\n[4/5] Creating market-level price comparison...")
    plot_market_price_comparison(df)
    
    # 5. Price Range Analysis
    print("\n[5/5] Creating price range analysis...")
    plot_price_range_analysis(df)
    
    # Generate summary
    print("\n[6/6] Generating geographical analysis summary...")
    summary = generate_geographical_analysis_summary(df)
    with open(f"{RESULT_PATH}/GEOGRAPHICAL_ANALYSIS_SUMMARY.txt", 'w', encoding='utf-8') as f:
        f.write(summary)
    print("[OK] Saved: GEOGRAPHICAL_ANALYSIS_SUMMARY.txt")
    
    print("\n" + "=" * 70)
    print("ADVANCED VISUALIZATIONS COMPLETED!")
    print(f"Results saved to: {RESULT_PATH}")
    print("=" * 70)
    
    print("\nGenerated Files:")
    print("  1. 01_price_distribution_histogram.png - Price frequency and variability")
    print("  2. 02_price_vs_arrival_date.png - Temporal price fluctuations")
    print("  3. 03_geographical_price_variation.png - Regional price differences")
    print("  4. 04_market_price_comparison.png - Market-level analysis")
    print("  5. 05_price_range_analysis.png - Min/Modal/Max price ranges")
    print("  6. GEOGRAPHICAL_ANALYSIS_SUMMARY.txt - Detailed summary report")

if __name__ == "__main__":
    run_advanced_visualizations()
