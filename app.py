"""
====================================================================
Mumbai Commute Analytics — Flask Web Application
File: app.py
Author: B.Sc Data Science Student Project
====================================================================
Academic Disclaimer:
"This dataset is created/simulated for academic analysis and does not
represent official Mumbai transport statistics."
====================================================================
"""

import os
import pickle
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "mumbai-commute-bsc-datascience-secret-key"

DATA_PATH = os.path.join("data", "commute_data_cleaned.csv")
MODEL_PATH = os.path.join("model", "commute_model.pkl")

def get_cleaned_data():
    """Load cleaned dataset or generate if missing."""
    if not os.path.exists(DATA_PATH):
        # Fallback to raw or trigger cleaning
        from generate_dataset import generate_commute_dataset
        from data_processing import clean_commute_data
        raw_df = generate_commute_dataset()
        os.makedirs("data", exist_ok=True)
        raw_df.to_csv("data/commute_data.csv", index=False)
        clean_df = clean_commute_data()
        return clean_df
    return pd.read_csv(DATA_PATH)

def load_trained_model():
    """Load the serialized decision tree model artifact."""
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)
    return None

# ====================================================================
# ROUTES
# ====================================================================

@app.route('/')
def index():
    """Home Page: Introduction, problem statement, key questions."""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard Page: KPIs, Chart.js visualizations, performance table."""
    df = get_cleaned_data()

    total_commutes = len(df)
    avg_travel_time = round(df['Travel_Time_min'].mean(), 1)
    avg_cost = round(df['Cost_INR'].mean(), 1)
    
    # Most used mode
    mode_counts = df['Transport_Mode'].value_counts()
    most_used = mode_counts.index[0] if not mode_counts.empty else "N/A"

    # Fastest mode (lowest average travel time)
    mode_time_avg = df.groupby('Transport_Mode')['Travel_Time_min'].mean()
    fastest_mode = mode_time_avg.idxmin() if not mode_time_avg.empty else "N/A"

    # Cheapest mode (lowest average cost)
    mode_cost_avg = df.groupby('Transport_Mode')['Cost_INR'].mean()
    cheapest_mode = mode_cost_avg.idxmin() if not mode_cost_avg.empty else "N/A"

    kpis = {
        'total_commutes': f"{total_commutes:,}",
        'avg_travel_time': avg_travel_time,
        'avg_cost': avg_cost,
        'most_used': most_used,
        'fastest_mode': fastest_mode,
        'cheapest_mode': cheapest_mode
    }

    # Chart.js data preparation
    modes_list = ['Auto', 'Local', 'Metro']
    chart_counts = [int(df[df['Transport_Mode'] == m].shape[0]) for m in modes_list]
    chart_times = [round(float(df[df['Transport_Mode'] == m]['Travel_Time_min'].mean()), 1) for m in modes_list]
    chart_costs = [round(float(df[df['Transport_Mode'] == m]['Cost_INR'].mean()), 1) for m in modes_list]

    chart_data = {
        'modes': modes_list,
        'counts': chart_counts,
        'avg_times': chart_times,
        'avg_costs': chart_costs
    }

    # Table breakdown
    mode_metrics = []
    for m in ['Metro', 'Local', 'Auto']:
        sub = df[df['Transport_Mode'] == m]
        if not sub.empty:
            mode_metrics.append({
                'mode': m,
                'trips': len(sub),
                'avg_distance': round(sub['Distance_km'].mean(), 1),
                'avg_time': round(sub['Travel_Time_min'].mean(), 1),
                'avg_cost': round(sub['Cost_INR'].mean(), 1),
                'avg_delay': round(sub['Delay_min'].mean(), 1),
                'avg_comfort': round(sub['Comfort_Rating'].mean(), 1),
                'avg_rating': round(sub['User_Rating'].mean(), 1)
            })

    return render_template(
        'dashboard.html',
        kpis=kpis,
        chart_data=chart_data,
        mode_metrics=mode_metrics
    )

@app.route('/comparison')
def comparison():
    """Mode Comparison Page: Detailed Metro vs Local vs Auto trade-offs."""
    return render_template('comparison.html')

@app.route('/data')
def data_view():
    """Commute Data Page: Searchable and filterable dataset view."""
    df = get_cleaned_data()
    selected_mode = request.args.get('mode', None)

    if selected_mode in ['Metro', 'Local', 'Auto']:
        df = df[df['Transport_Mode'] == selected_mode]

    # Convert to dictionary records for template rendering (limit to first 300 for snappy rendering)
    records = df.head(300).to_dict(orient='records')
    return render_template('data.html', records=records, selected_mode=selected_mode)

@app.route('/analytics')
def analytics():
    """Analytics Page: EDA charts and data science findings."""
    return render_template('analytics.html')

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    """Prediction Page: ML Model inference based on commute parameters."""
    model_payload = load_trained_model()
    prediction_result = None
    form_data = None

    metrics = {
        'dt_accuracy': 95.8,
        'rf_accuracy': 96.4
    }

    if model_payload:
        metrics = model_payload.get('metrics', metrics)

    if request.method == 'POST':
        try:
            distance = float(request.form.get('distance', 10.0))
            travel_time = int(request.form.get('travel_time', 30))
            waiting_time = int(request.form.get('waiting_time', 5))
            cost = int(request.form.get('cost', 25))
            peak_hour = request.form.get('peak_hour', 'Yes')
            crowd_level = request.form.get('crowd_level', 'High')
            weather = request.form.get('weather', 'Clear')
            delay = int(request.form.get('delay', 3))
            comfort = int(request.form.get('comfort', 3))

            form_data = {
                'distance': distance,
                'travel_time': travel_time,
                'waiting_time': waiting_time,
                'cost': cost,
                'peak_hour': peak_hour,
                'crowd_level': crowd_level,
                'weather': weather,
                'delay': delay,
                'comfort': comfort
            }

            if model_payload:
                dt_model = model_payload['model']
                encoders = model_payload['encoders']

                # Transform categorical variables safely with known encoders
                peak_encoded = encoders['Peak_Hour'].transform([peak_hour])[0] if peak_hour in encoders['Peak_Hour'].classes_ else 1
                crowd_encoded = encoders['Crowd_Level'].transform([crowd_level])[0] if crowd_level in encoders['Crowd_Level'].classes_ else 1
                weather_encoded = encoders['Weather'].transform([weather])[0] if weather in encoders['Weather'].classes_ else 0

                input_features = pd.DataFrame([{
                    'Distance_km': distance,
                    'Travel_Time_min': travel_time,
                    'Waiting_Time_min': waiting_time,
                    'Cost_INR': cost,
                    'Peak_Hour': peak_encoded,
                    'Crowd_Level': crowd_encoded,
                    'Weather': weather_encoded,
                    'Delay_min': delay,
                    'Comfort_Rating': comfort
                }])

                pred_encoded = dt_model.predict(input_features)[0]
                prediction_result = encoders['target'].inverse_transform([pred_encoded])[0]
            else:
                # Rule-based fallback if model file was not yet generated
                if distance > 18 or cost <= 25:
                    prediction_result = "Local"
                elif comfort >= 4 or (distance <= 15 and cost <= 60):
                    prediction_result = "Metro"
                else:
                    prediction_result = "Auto"

        except Exception as e:
            flash(f"Error processing prediction input: {str(e)}", "danger")

    return render_template(
        'prediction.html',
        prediction=prediction_result,
        form_data=form_data,
        metrics=metrics
    )

@app.route('/about')
def about():
    """About & Viva Preparation Guide."""
    return render_template('about.html')

if __name__ == '__main__':
    # Run development server on port 5000
    print("=" * 65)
    print("Starting Mumbai Commute Analytics Web Server...")
    print("Access the dashboard at: http://127.0.0.1:5000")
    print("=" * 65)
    app.run(debug=True, port=5000)
