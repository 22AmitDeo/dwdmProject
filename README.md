# Crop Price Volatility & Farmer Income Risk Analysis

## Project Overview
This project applies Data Warehousing and OLAP techniques to analyze agricultural commodity price volatility and its impact on farmer income stability.

## Project Structure
```
dwdmProject/
├── data/
│   └── cleaned_crop_prices.csv          # Preprocessed dataset
├── analysis/
│   ├── data_mining.py                   # Risk analysis & volatility metrics
│   ├── olap_operations.py               # OLAP roll-up, drill-down, slice, dice
│   ├── visualizations.py                # Charts and heatmaps
│   ├── insights.py                      # Key findings generation
│   └── price_analysis.py                # Basic analysis (existing)
├── results/
│   ├── data_mining/                     # Risk index, volatility analysis
│   ├── olap/                            # Roll-up, drill-down results
│   ├── visualizations/                  # PNG charts
│   ├── PROJECT_REPORT.txt               # Academic report
│   └── insights_summary.txt             # Key findings
├── run_analysis.py                      # Main execution script
└── README.md                            # This file
```

## Dataset Columns
- **Geographic**: State, District, Market
- **Temporal**: Arrival_Date (Year, Month extracted)
- **Product**: Commodity, Variety, Grade
- **Price**: Min_Price, Max_Price, Modal_Price
- **Engineered**: Volatility (Max - Min), Risk_Index (Volatility / Modal_Price)

## Key Features

### 1. Data Mining Module
- **Risk Classification**: Low/Medium/High based on Risk_Index
- **Volatility Analysis**: Identifies most volatile crops
- **State Comparison**: Geographic volatility patterns
- **Seasonal Analysis**: Monthly price variations
- **Supply-Price Correlation**: Market arrival vs price relationship

### 2. OLAP Operations
- **Roll-Up**: Market → District → State (aggregation)
- **Drill-Down**: Year → Month → Day (disaggregation)
- **Slice**: Single dimension filtering (e.g., specific commodity)
- **Dice**: Multi-dimension filtering (commodity + state + year)
- **Pivot**: Cross-dimensional comparison (commodity vs state)

### 3. Visualizations
- Crop volatility comparison (top 15)
- Price trends over years
- State-wise average prices
- Risk classification distribution
- Seasonal price patterns
- State-commodity volatility heatmap

### 4. Risk Index Calculation
```
Risk_Index = Volatility / Modal_Price

Risk Categories:
- Low Risk: ≤ 0.10
- Medium Risk: 0.10 - 0.25
- High Risk: > 0.25
```

## Running the Project

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn
```

### Execute Complete Analysis
```bash
python run_analysis.py
```

### Run Individual Modules
```bash
# Data Mining
python analysis/data_mining.py

# OLAP Analysis
python analysis/olap_operations.py

# Visualizations
python analysis/visualizations.py

# Insights
python analysis/insights.py
```

## Output Files

### Data Mining Results
- `data_with_risk_index.csv` - Full dataset with risk metrics
- `volatile_crops.csv` - Top 10 most volatile commodities
- `state_volatility.csv` - State-wise volatility comparison
- `monthly_pattern.csv` - Seasonal price patterns
- `supply_price_correlation.csv` - Supply-price relationships

### OLAP Results
- `rollup_market_level.csv` - Market-level aggregation
- `rollup_district_level.csv` - District-level aggregation
- `rollup_state_level.csv` - State-level aggregation
- `drilldown_year_level.csv` - Yearly trends
- `drilldown_month_level.csv` - Monthly details
- `drilldown_day_level.csv` - Daily granularity
- `slice_result.csv` - Single commodity analysis
- `dice_result.csv` - Multi-filter analysis
- `pivot_commodity_state.csv` - Cross-dimensional matrix

### Visualizations
- `01_volatility_comparison.png` - Top 15 crops by volatility
- `02_price_trend.png` - Price trends over years
- `03_state_average_price.png` - State-wise prices
- `04_risk_distribution.png` - Risk category distribution
- `05_seasonal_pattern.png` - Monthly patterns
- `06_state_volatility_heatmap.png` - State-commodity heatmap

### Reports
- `PROJECT_REPORT.txt` - Complete academic report
- `insights_summary.txt` - Key findings and implications

## Key Insights

1. **Volatility Concentration**: Top commodities show 2-3x higher volatility
2. **Geographic Disparities**: Regional variations require localized policies
3. **Seasonal Vulnerability**: Harvest season shows highest price volatility
4. **Supply-Demand Mismatch**: Inverse correlation between supply and prices
5. **Risk Distribution**: Significant portion of transactions classified as high-risk

## Policy Implications

- Commodity-specific support for high-volatility crops
- Price stabilization during harvest season
- Regional market information systems
- Storage infrastructure development
- Targeted crop insurance schemes
- Minimum support price mechanisms

## Technologies Used

- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Data Warehouse**: Star Schema (conceptual)
- **OLAP**: Pandas GroupBy operations
- **Analysis**: Statistical aggregation and correlation

## Report Structure

The project report includes:
1. Executive Summary
2. Data Collection methodology
3. Preprocessing steps
4. Data Warehouse design (Star Schema)
5. Data Mining analysis
6. OLAP operations explanation
7. Key findings
8. Policy recommendations
9. Methodology notes
10. Conclusions

## Author Notes

This project demonstrates practical application of:
- Data warehousing principles (dimensional modeling)
- OLAP techniques (multi-dimensional analysis)
- Data mining methods (risk classification, pattern discovery)
- Business intelligence (insights generation)

All code follows minimal implementation principle - only essential code for analysis.
