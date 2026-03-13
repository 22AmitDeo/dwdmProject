"""
Main execution script for DWDM Project
Runs all analysis modules: data mining, OLAP, visualizations, and insights
"""

import sys
import os

def run_all_analyses():
    """Execute all analysis modules"""
    print("\n" + "=" * 80)
    print("CROP PRICE VOLATILITY & FARMER INCOME RISK ANALYSIS")
    print("Data Warehousing and OLAP Techniques - Complete Analysis")
    print("=" * 80)
    
    try:
        # 1. Time-Series Analysis (Monthly OLAP Drill-Down)
        print("\n[STEP 1/6] Running Monthly Time-Series Analysis...")
        from analysis.time_series_analysis import run_time_series_analysis
        run_time_series_analysis()
        
        # 2. Advanced Visualizations (Distribution & Geographical)
        print("\n[STEP 2/6] Running Advanced Visualizations...")
        from analysis.advanced_visualizations import run_advanced_visualizations
        run_advanced_visualizations()
        
        # 3. Data Mining
        print("\n[STEP 3/6] Running Data Mining Analysis...")
        from analysis.data_mining import run_data_mining
        df = run_data_mining()
        
        # 4. OLAP Operations
        print("\n[STEP 4/6] Running OLAP Analysis...")
        from analysis.olap_operations import run_olap_analysis
        run_olap_analysis()
        
        # 5. Visualizations
        print("\n[STEP 5/6] Generating Visualizations...")
        from analysis.visualizations import run_visualizations
        run_visualizations()
        
        # 6. Insights
        print("\n[STEP 6/6] Generating Insights...")
        from analysis.insights import generate_insights
        generate_insights()
        
        print("\n" + "=" * 80)
        print("[OK] ALL ANALYSES COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("\nGenerated Outputs:")
        print("  • Time-Series Analysis: results/time_series/")
        print("  • Advanced Visualizations: results/advanced_visualizations/")
        print("  • Data Mining Results: results/data_mining/")
        print("  • OLAP Analysis: results/olap/")
        print("  • Visualizations: results/visualizations/")
        print("  • Insights Summary: results/insights_summary.txt")
        print("  • Project Report: results/PROJECT_REPORT.txt")
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_all_analyses()
