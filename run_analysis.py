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
        # 1. Data Mining
        print("\n[STEP 1/4] Running Data Mining Analysis...")
        from analysis.data_mining import run_data_mining
        df = run_data_mining()
        
        # 2. OLAP Operations
        print("\n[STEP 2/4] Running OLAP Analysis...")
        from analysis.olap_operations import run_olap_analysis
        run_olap_analysis()
        
        # 3. Visualizations
        print("\n[STEP 3/4] Generating Visualizations...")
        from analysis.visualizations import run_visualizations
        run_visualizations()
        
        # 4. Insights
        print("\n[STEP 4/4] Generating Insights...")
        from analysis.insights import generate_insights
        generate_insights()
        
        print("\n" + "=" * 80)
        print("✓ ALL ANALYSES COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("\nGenerated Outputs:")
        print("  • Data Mining Results: results/data_mining/")
        print("  • OLAP Analysis: results/olap/")
        print("  • Visualizations: results/visualizations/")
        print("  • Insights Summary: results/insights_summary.txt")
        print("  • Project Report: results/PROJECT_REPORT.txt")
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_all_analyses()
