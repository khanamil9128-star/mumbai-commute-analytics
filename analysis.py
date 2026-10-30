"""
====================================================================
Mumbai Commute Analytics — Step 3: Exploratory Data Analysis (EDA)
File: analysis.py
Author: B.Sc Data Science Student Project
====================================================================
Academic Disclaimer:
"This dataset is created/simulated for academic analysis and does not
represent official Mumbai transport statistics."
====================================================================
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual style for clean academic presentations
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

CHARTS_DIR = os.path.join("static", "images")

def run_exploratory_data_analysis(clean_csv="data/commute_data_cleaned.csv"):
    if not os.path.exists(clean_csv):
        raise FileNotFoundError(f"Cleaned dataset '{clean_csv}' not found. Run data_processing.py first.")

    os.makedirs(CHARTS_DIR, exist_ok=True)
    df = pd.read_csv(clean_csv)

    print("=" * 70)
    print("MUMBAI COMMUTE ANALYTICS: EXPLORATORY DATA ANALYSIS (EDA)")
    print("=" * 70)
    print(f"Total Clean Records Analysed: {len(df)}")
    print(f"Modes Observed: {df['Transport_Mode'].unique().tolist()}\n")

    # -------------------------------------------------------------
    # 1. Transport Mode Comparison Summary
    # -------------------------------------------------------------
    print("-" * 70)
    print("1. OVERALL METRICS BY TRANSPORT MODE")
    print("-" * 70)
    summary_by_mode = df.groupby('Transport_Mode').agg(
        Total_Trips=('Commute_ID', 'count'),
        Avg_Travel_Time=('Travel_Time_min', 'mean'),
        Avg_Cost_INR=('Cost_INR', 'mean'),
        Avg_Waiting_Time=('Waiting_Time_min', 'mean'),
        Avg_Delay_min=('Delay_min', 'mean'),
        Avg_Distance_km=('Distance_km', 'mean'),
        Avg_Comfort_Rating=('Comfort_Rating', 'mean'),
        Avg_User_Rating=('User_Rating', 'mean')
    ).round(2)

    print(summary_by_mode)
    print()

    # -------------------------------------------------------------
    # 2. Peak vs Non-Peak Analysis
    # -------------------------------------------------------------
    print("-" * 70)
    print("2. PEAK VS NON-PEAK COMMUTE ANALYSIS")
    print("-" * 70)
    peak_summary = df.groupby(['Transport_Mode', 'Peak_Hour']).agg(
        Avg_Travel_Time=('Travel_Time_min', 'mean'),
        Avg_Delay=('Delay_min', 'mean'),
        Avg_Cost=('Cost_INR', 'mean')
    ).round(2)
    print(peak_summary)
    print()

    # -------------------------------------------------------------
    # 3. Crowd Level Distribution by Mode
    # -------------------------------------------------------------
    print("-" * 70)
    print("3. CROWD LEVEL DISTRIBUTION ACROSS MODES")
    print("-" * 70)
    crowd_crosstab = pd.crosstab(df['Transport_Mode'], df['Crowd_Level'], normalize='index') * 100
    print(crowd_crosstab.round(1))
    print()

    # -------------------------------------------------------------
    # 4. Top Routes by Average Commute Time
    # -------------------------------------------------------------
    print("-" * 70)
    print("4. TOP 5 LONGEST COMMUTE ROUTES (BY AVERAGE TIME)")
    print("-" * 70)
    df['Route'] = df['Starting_Area'] + " -> " + df['Destination']
    top_routes = df.groupby('Route').agg(
        Trips=('Commute_ID', 'count'),
        Avg_Time=('Travel_Time_min', 'mean'),
        Avg_Cost=('Cost_INR', 'mean')
    ).sort_values(by='Avg_Time', ascending=False).head(5).round(2)
    print(top_routes)
    print()

    # =============================================================
    # PLOTTING AND SAVING SEABORN/MATPLOTLIB CHARTS
    # =============================================================

    # Chart 1: Average Travel Time & Cost Comparison (Bar Charts)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    palette = {'Metro': '#198754', 'Local': '#0d6efd', 'Auto': '#ffc107'}

    sns.barplot(
        x='Transport_Mode', y='Travel_Time_min', data=df,
        ax=axes[0], palette=palette, errorbar=None
    )
    axes[0].set_title("Average Travel Time by Mode (Minutes)", fontsize=13, weight='bold')
    axes[0].set_xlabel("Transport Mode")
    axes[0].set_ylabel("Travel Time (min)")
    for p in axes[0].patches:
        axes[0].annotate(f"{p.get_height():.1f}m", (p.get_x() + p.get_width() / 2., p.get_height() / 2),
                         ha='center', va='center', color='black' if p.get_facecolor()[0] > 0.8 else 'white', weight='bold')

    sns.barplot(
        x='Transport_Mode', y='Cost_INR', data=df,
        ax=axes[1], palette=palette, errorbar=None
    )
    axes[1].set_title("Average Commute Cost by Mode (INR ₹)", fontsize=13, weight='bold')
    axes[1].set_xlabel("Transport Mode")
    axes[1].set_ylabel("Cost (₹)")
    for p in axes[1].patches:
        axes[1].annotate(f"₹{p.get_height():.0f}", (p.get_x() + p.get_width() / 2., p.get_height() / 2),
                         ha='center', va='center', color='black' if p.get_facecolor()[0] > 0.8 else 'white', weight='bold')

    plt.tight_layout()
    chart1_path = os.path.join(CHARTS_DIR, "travel_time_and_cost.png")
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print(f"Saved: {chart1_path}")

    # Chart 2: Distance vs Travel Time (Scatter Plot with Hue)
    plt.figure(figsize=(9, 5.5))
    sns.scatterplot(
        x='Distance_km', y='Travel_Time_min', hue='Transport_Mode',
        data=df, palette=palette, alpha=0.75, s=60
    )
    sns.regplot(
        x='Distance_km', y='Travel_Time_min', data=df,
        scatter=False, ax=plt.gca(), color='gray', line_kws={'linestyle': '--', 'linewidth': 1.2}
    )
    plt.title("Distance vs Travel Time (With Linear Trendline)", fontsize=13, weight='bold')
    plt.xlabel("Distance (km)")
    plt.ylabel("Travel Time (minutes)")
    plt.legend(title="Mode")
    plt.tight_layout()
    chart2_path = os.path.join(CHARTS_DIR, "distance_vs_time.png")
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print(f"Saved: {chart2_path}")

    # Chart 3: Distance vs Cost (Scatter Plot)
    plt.figure(figsize=(9, 5.5))
    sns.scatterplot(
        x='Distance_km', y='Cost_INR', hue='Transport_Mode',
        data=df, palette=palette, alpha=0.75, s=60
    )
    plt.title("Distance vs Commute Cost (Fare Dynamics)", fontsize=13, weight='bold')
    plt.xlabel("Distance (km)")
    plt.ylabel("Cost in INR (₹)")
    plt.legend(title="Mode")
    plt.tight_layout()
    chart3_path = os.path.join(CHARTS_DIR, "distance_vs_cost.png")
    plt.savefig(chart3_path, dpi=300)
    plt.close()
    print(f"Saved: {chart3_path}")

    # Chart 4: Peak vs Non-Peak Travel Time Impact
    plt.figure(figsize=(8, 5))
    sns.barplot(
        x='Transport_Mode', y='Travel_Time_min', hue='Peak_Hour',
        data=df, palette=['#6c757d', '#dc3545'], errorbar=None
    )
    plt.title("Impact of Peak Hours on Travel Time", fontsize=13, weight='bold')
    plt.xlabel("Transport Mode")
    plt.ylabel("Average Travel Time (min)")
    plt.legend(title="Peak Hour?")
    plt.tight_layout()
    chart4_path = os.path.join(CHARTS_DIR, "peak_hour_impact.png")
    plt.savefig(chart4_path, dpi=300)
    plt.close()
    print(f"Saved: {chart4_path}")

    # Chart 5: Crowd Level Distribution
    plt.figure(figsize=(8, 5))
    crowd_order = ['Low', 'Medium', 'High', 'Extreme']
    sns.countplot(
        x='Transport_Mode', hue='Crowd_Level',
        data=df, palette='Blues', hue_order=crowd_order
    )
    plt.title("Crowd Level Frequency by Transport Mode", fontsize=13, weight='bold')
    plt.xlabel("Transport Mode")
    plt.ylabel("Number of Commutes")
    plt.legend(title="Crowd Level")
    plt.tight_layout()
    chart5_path = os.path.join(CHARTS_DIR, "crowd_distribution.png")
    plt.savefig(chart5_path, dpi=300)
    plt.close()
    print(f"Saved: {chart5_path}")

    # Chart 6: Comfort Rating vs User Rating Boxplots
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    sns.boxplot(x='Transport_Mode', y='Comfort_Rating', data=df, ax=axes[0], palette=palette)
    axes[0].set_title("Comfort Rating (1 = Poor, 5 = Excellent)", weight='bold')
    axes[0].set_ylabel("Comfort Rating (1-5)")

    sns.boxplot(x='Transport_Mode', y='User_Rating', data=df, ax=axes[1], palette=palette)
    axes[1].set_title("Overall User Satisfaction Rating", weight='bold')
    axes[1].set_ylabel("User Rating (out of 5)")

    plt.tight_layout()
    chart6_path = os.path.join(CHARTS_DIR, "ratings_distribution.png")
    plt.savefig(chart6_path, dpi=300)
    plt.close()
    print(f"Saved: {chart6_path}")

    print("=" * 70)
    print("EDA Complete. All visual charts generated in static/images/.")
    print("=" * 70)

if __name__ == "__main__":
    run_exploratory_data_analysis()

