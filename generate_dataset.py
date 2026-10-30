"""
Mumbai Commute Analytics — Dataset Generator
Academic Simulation Script

NOTE & DISCLAIMER:
"This dataset is created/simulated for academic analysis and does not represent official Mumbai transport statistics."
"""

import os
import random
import numpy as np
import pandas as pd

def generate_commute_dataset(n_samples=1200, random_seed=42):
    np.random.seed(random_seed)
    random.seed(random_seed)

    areas = [
        "Andheri", "Bandra", "Borivali", "Dadar", "Churchgate",
        "CSMT", "Ghatkopar", "Kurla", "Thane", "Colaba",
        "Powai", "Malad", "Vashi", "BKC", "Worli", "Goregaon"
    ]

    modes = ["Metro", "Local", "Auto"]
    weather_options = ["Clear", "Rainy", "Humid", "Cloudy"]
    crowd_levels = ["Low", "Medium", "High", "Extreme"]

    records = []

    for i in range(1, n_samples + 1):
        commute_id = f"MUM_{1000 + i}"
        start = random.choice(areas)
        dest = random.choice([a for a in areas if a != start])
        mode = random.choice(modes)

        # Peak hours: 08:30-11:30 AM or 05:30-08:30 PM
        is_peak = random.choice(["Yes", "No"])
        weather = random.choice(weather_options)

        # Tailor metrics based on mode to simulate real Mumbai commute conditions
        if mode == "Local":
            # Mumbai Local trains: Long distance, super cheap, high crowd, frequent delays
            distance = round(np.random.uniform(8.0, 42.0), 1)
            # Speed approx 35-45 km/h + stops
            base_time = (distance / 35.0) * 60.0
            delay = int(np.random.exponential(scale=6.0)) if is_peak == "Yes" else int(np.random.exponential(scale=2.5))
            travel_time = round(base_time + delay + np.random.uniform(2, 8))
            waiting_time = random.randint(3, 12)
            # Ticket pricing: 10, 15, 20 INR for regular second class
            cost = random.choice([10, 15, 20, 25]) if distance <= 25 else random.choice([20, 25, 30])
            crowd = random.choice(["High", "Extreme"]) if is_peak == "Yes" else random.choice(["Medium", "High"])
            comfort = random.choice([1, 2, 3]) if is_peak == "Yes" else random.choice([2, 3, 4])
            user_rating = round(np.random.uniform(2.5, 4.5), 1)

        elif mode == "Metro":
            # Metro lines: Medium distance, moderate fare, AC comfort, punctuality
            distance = round(np.random.uniform(3.0, 26.0), 1)
            base_time = (distance / 32.0) * 60.0
            delay = int(np.random.exponential(scale=1.5))
            travel_time = round(base_time + delay + np.random.uniform(1, 5))
            waiting_time = random.randint(2, 6)
            # Metro fare: Rs 20 to Rs 60 based on distance
            cost = int(20 + (distance * 1.5))
            crowd = random.choice(["Medium", "High"]) if is_peak == "Yes" else random.choice(["Low", "Medium"])
            comfort = random.choice([4, 5])  # AC, clean coaches
            user_rating = round(np.random.uniform(3.8, 4.9), 1)

        else: # Auto Rickshaw
            # Auto: Short to medium distance, meter fare, road congestion impacts peak hours
            distance = round(np.random.uniform(1.5, 14.0), 1)
            # Speed heavily impacted by traffic: 15-20 km/h in peak, 25 km/h non-peak
            avg_speed = np.random.uniform(12.0, 18.0) if is_peak == "Yes" else np.random.uniform(20.0, 28.0)
            base_time = (distance / avg_speed) * 60.0
            delay = int(np.random.exponential(scale=5.0)) if is_peak == "Yes" else int(np.random.exponential(scale=1.5))
            travel_time = round(base_time + delay + np.random.uniform(2, 6))
            waiting_time = random.randint(4, 15)  # Finding an auto / refusals
            # Meter fare: Base Rs 28 for first 1.5 km, then approx Rs 18.5/km
            cost = int(28 + max(0.0, distance - 1.5) * 18.5)
            crowd = "Low" # Only 1-3 people in an auto
            comfort = random.choice([2, 3, 4])
            user_rating = round(np.random.uniform(2.8, 4.2), 1)

        # Date across a realistic semester/academic timeframe
        month = random.randint(1, 6)
        day = random.randint(1, 28)
        date_str = f"2024-{month:02d}-{day:02d}"

        records.append({
            "Commute_ID": commute_id,
            "Date": date_str,
            "Starting_Area": start,
            "Destination": dest,
            "Transport_Mode": mode,
            "Distance_km": distance,
            "Travel_Time_min": int(travel_time),
            "Waiting_Time_min": int(waiting_time),
            "Cost_INR": int(cost),
            "Peak_Hour": is_peak,
            "Crowd_Level": crowd,
            "Delay_min": int(delay),
            "Weather": weather,
            "Comfort_Rating": int(comfort),
            "User_Rating": user_rating
        })

    df = pd.DataFrame(records)

    # -------------------------------------------------------------
    # Inject deliberate dirty data to teach and show Data Cleaning:
    # 1. Duplicates
    # 2. Inconsistent casing
    # 3. Missing values (NaN)
    # 4. Outliers/Impossible values
    # -------------------------------------------------------------
    duplicate_rows = df.sample(n=25, random_state=101)
    df = pd.concat([df, duplicate_rows], ignore_index=True)

    # Inconsistent transport names (e.g. 'metro', 'LOCAL', 'auto')
    dirty_indices_mode = np.random.choice(df.index, size=30, replace=False)
    for idx in dirty_indices_mode[:10]:
        df.at[idx, "Transport_Mode"] = "metro"
    for idx in dirty_indices_mode[10:20]:
        df.at[idx, "Transport_Mode"] = "LOCAL"
    for idx in dirty_indices_mode[20:]:
        df.at[idx, "Transport_Mode"] = "auto"

    # Missing values
    missing_indices_wait = np.random.choice(df.index, size=15, replace=False)
    df.loc[missing_indices_wait, "Waiting_Time_min"] = np.nan

    missing_indices_weather = np.random.choice(df.index, size=10, replace=False)
    df.loc[missing_indices_weather, "Weather"] = np.nan

    # Impossible/erroneous values for outlier detection
    err_idx = np.random.choice(df.index, size=4, replace=False)
    df.at[err_idx[0], "Cost_INR"] = -50          # Impossible negative cost
    df.at[err_idx[1], "Travel_Time_min"] = -15    # Impossible negative time
    df.at[err_idx[2], "Distance_km"] = 999.0      # Outlier impossible distance
    df.at[err_idx[3], "Cost_INR"] = 12000         # Extreme outlier cost

    return df

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df_raw = generate_commute_dataset(n_samples=1200)
    output_path = os.path.join("data", "commute_data.csv")
    df_raw.to_csv(output_path, index=False)
    print(f"Generated raw dataset successfully: {output_path} with {len(df_raw)} rows.")
    print("Academic Disclaimer: This dataset is simulated for academic demonstration and does not represent official Mumbai transport statistics.")

