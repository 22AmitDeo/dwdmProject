import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

DATA_PATH = "../data/cleaned_crop_prices.csv"
RESULT_PATH = "../results/visualizations"

def setup_style():
    """Configure visualization style"""
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (14, 8)
    plt.rcParams['font.size'] = 10

def plot_volatility_comparison(df):
    """Crop price volatility comparison chart"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    volatility_by_crop = df.groupby('Commodity')['Volatility'].mean().sort_values(ascending=False).head(15)
    
    colors = plt.cm.RdYlGn_r(range(len(volatility_by_crop)))
    volatility_by_crop.plot(kind='barh', ax=ax, color=colors)
    
    ax.set_xlabel('Average Volatility (Max_Price - Min_Price)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Commodity', fontsize=11, fontweight='bold')
    ax.set_title('Top 15 Crops by Price Volatility', fontsize=13, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{RESULT_PATH}/01_volatility_comparison.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 01_volatility_comparison.png")

def plot_price_trend(df):
    """Price trend over years"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    yearly_trend = df.groupby(['Year', 'Commodity'])['Modal_Price'].mean().reset_index()
    
    for commodity in yearly_trend['Commodity'].unique()[:8]:
        data = yearly_trend[yearly_trend['Commodity'] == commodity]
        ax.plot(data['Year'], data['Modal_Price'], marker='o', label=commodity, linewidth=2)
    
    ax.set_xlabel('Year', fontsize=11, fontweight='bold')
    ax.set_ylabel('Average Modal Price', fontsize=11, fontweight='bold')
    ax.set_title('Price Trends Over Years (Top 8 Commodities)', fontsize=13, fontweight='bold')
    ax.legend(loc='best', fontsize=9)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{RESULT_PATH}/02_price_trend.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 02_price_trend.png")

def plot_state_average_price(df):
    """State-wise average price chart"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    state_price = df.groupby('State')['Modal_Price'].mean().sort_values(ascending=False)
    
    colors = plt.cm.viridis(range(len(state_price)))
    state_price.plot(kind='bar', ax=ax, color=colors)
    
    ax.set_xlabel('State', fontsize=11, fontweight='bold')
    ax.set_ylabel('Average Modal Price', fontsize=11, fontweight='bold')
    ax.set_title('Average Crop Price by State', fontsize=13, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(f"{RESULT_PATH}/03_state_average_price.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 03_state_average_price.png")

def plot_risk_distribution(df):
    """Risk classification distribution"""
    df['Risk_Index'] = df['Volatility'] / df['Modal_Price']
    df['Risk_Category'] = pd.cut(df['Risk_Index'], 
                                   bins=[0, 0.1, 0.25, 1.0],
                                   labels=['Low Risk', 'Medium Risk', 'High Risk'])
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Pie chart
    risk_counts = df['Risk_Category'].value_counts()
    colors_pie = ['#2ecc71', '#f39c12', '#e74c3c']
    axes[0].pie(risk_counts, labels=risk_counts.index, autopct='%1.1f%%', 
                colors=colors_pie, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
    axes[0].set_title('Risk Classification Distribution', fontsize=12, fontweight='bold')
    
    # Bar chart
    risk_counts.plot(kind='bar', ax=axes[1], color=colors_pie)
    axes[1].set_xlabel('Risk Category', fontsize=11, fontweight='bold')
    axes[1].set_ylabel('Count', fontsize=11, fontweight='bold')
    axes[1].set_title('Risk Category Counts', fontsize=12, fontweight='bold')
    axes[1].grid(axis='y', alpha=0.3)
    plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(f"{RESULT_PATH}/04_risk_distribution.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 04_risk_distribution.png")

def plot_seasonal_pattern(df):
    """Seasonal price variation"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    monthly_pattern = df.groupby('Month').agg({
        'Modal_Price': 'mean',
        'Volatility': 'mean'
    })
    
    ax2 = ax.twinx()
    
    line1 = ax.plot(monthly_pattern.index, monthly_pattern['Modal_Price'], 
                    marker='o', color='#3498db', linewidth=2.5, markersize=8, label='Avg Price')
    line2 = ax2.plot(monthly_pattern.index, monthly_pattern['Volatility'], 
                     marker='s', color='#e74c3c', linewidth=2.5, markersize=8, label='Avg Volatility')
    
    ax.set_xlabel('Month', fontsize=11, fontweight='bold')
    ax.set_ylabel('Average Modal Price', fontsize=11, fontweight='bold', color='#3498db')
    ax2.set_ylabel('Average Volatility', fontsize=11, fontweight='bold', color='#e74c3c')
    ax.set_title('Seasonal Price and Volatility Pattern', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(range(1, 13))
    
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, loc='upper left', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f"{RESULT_PATH}/05_seasonal_pattern.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 05_seasonal_pattern.png")

def plot_state_volatility_heatmap(df):
    """State-wise volatility heatmap"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    state_commodity_volatility = df.pivot_table(
        values='Volatility',
        index='State',
        columns='Commodity',
        aggfunc='mean'
    )
    
    sns.heatmap(state_commodity_volatility.iloc[:, :15], annot=False, cmap='YlOrRd', 
                ax=ax, cbar_kws={'label': 'Volatility'})
    
    ax.set_title('State-Commodity Volatility Heatmap', fontsize=13, fontweight='bold')
    ax.set_xlabel('Commodity', fontsize=11, fontweight='bold')
    ax.set_ylabel('State', fontsize=11, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(f"{RESULT_PATH}/06_state_volatility_heatmap.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 06_state_volatility_heatmap.png")

def run_visualizations():
    """Generate all visualizations"""
    print("\n" + "=" * 60)
    print("VISUALIZATION MODULE")
    print("=" * 60)
    
    df = pd.read_csv(DATA_PATH)
    os.makedirs(RESULT_PATH, exist_ok=True)
    setup_style()
    
    print("\nGenerating visualizations...")
    plot_volatility_comparison(df)
    plot_price_trend(df)
    plot_state_average_price(df)
    plot_risk_distribution(df)
    plot_seasonal_pattern(df)
    plot_state_volatility_heatmap(df)
    
    print("\n" + "=" * 60)
    print("All visualizations completed!")
    print(f"Saved to: {RESULT_PATH}")
    print("=" * 60)

if __name__ == "__main__":
    run_visualizations()
