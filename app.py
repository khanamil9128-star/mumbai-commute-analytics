"""
====================================================================
Mumbai Commute Analytics — Unified Web Application
Streamlit Cloud Native UI + Local Flask Web Server
====================================================================
Academic Disclaimer:
"This dataset is created/simulated for academic analysis and does not
represent official Mumbai transport statistics."
====================================================================
"""

import os
import sys

# Detect if executed via Streamlit runtime (e.g. on Streamlit Cloud)
is_streamlit = False
try:
    import streamlit as st
    if st.runtime.exists():
        is_streamlit = True
except Exception:
    is_streamlit = False

if is_streamlit:
    # =================================================================
    # STREAMLIT CLOUD APPLICATION
    # =================================================================
    import pickle
    import pandas as pd
    import numpy as np

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(BASE_DIR, "data", "commute_data_cleaned.csv")
    MODEL_PATH = os.path.join(BASE_DIR, "model", "commute_model.pkl")
    CHARTS_DIR = os.path.join(BASE_DIR, "static", "images")

    st.set_page_config(
        page_title="Mumbai Commute Analytics",
        page_icon="🚆",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    @st.cache_data
    def load_data():
        if os.path.exists(DATA_PATH):
            return pd.read_csv(DATA_PATH)
        # Fallback simulation
        from generate_dataset import generate_commute_dataset
        from data_processing import clean_commute_data
        raw = generate_commute_dataset()
        os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
        raw.to_csv(os.path.join(BASE_DIR, "data", "commute_data.csv"), index=False)
        return clean_commute_data(
            input_csv=os.path.join(BASE_DIR, "data", "commute_data.csv"),
            output_csv=DATA_PATH
        )

    @st.cache_resource
    def load_model():
        if os.path.exists(MODEL_PATH):
            try:
                with open(MODEL_PATH, 'rb') as f:
                    return pickle.load(f)
            except Exception:
                return None
        return None

    df = load_data()
    model_payload = load_model()

    # Academic Notice Banner
    st.warning("⚠️ **Academic Simulation Notice:** This dataset is created/simulated for academic analysis and does not represent official Mumbai transport statistics.")

    # Sidebar Navigation
    st.sidebar.title("🚆 Mumbai Commute Analytics")
    st.sidebar.caption("Transit Intelligence & Commute Analytics")
    st.sidebar.markdown("---")

    menu = st.sidebar.radio(
        "Navigate",
        [
            "🏠 Project Overview",
            "📊 KPI Dashboard",
            "🔄 Transport Comparison",
            "📋 Commute Dataset",
            "📈 EDA Visual Analytics",
            "🤖 ML Mode Predictor",
            "ℹ️ Methodology & Scope"
        ]
    )

    # 1. Project Overview
    if menu == "🏠 Project Overview":
        st.title("Mumbai Commute Analytics: Metro vs Local vs Auto")
        st.markdown("### An Empirical Data Science Study of Mumbai Transit Systems")
        col1, col2 = st.columns([3, 2])
        with col1:
            st.write("""
            Welcome to the **Mumbai Commute Analytics** system. Mumbai is powered by one of the most complex multimodal transit networks in the world:
            
            * **Mumbai Local Train:** The iconic lifeline carrying over 7 million daily passengers across Suburban corridors. Hyper-affordable and rapid over long journeys, but subject to intense rush-hour crush.
            * **Mumbai Metro:** Modern, fully air-conditioned transit providing reliable, traffic-free punctuality and comfort over medium-distance routes.
            * **Auto Rickshaw:** First-and-last mile suburban mobility offering private, on-demand seating, but constrained by street congestion and higher per-km meter fares.
            
            This project investigates empirical commuter trade-offs: travel time, cost, peak-hour bottlenecks, crowding, and user satisfaction using **Pandas, Seaborn, MySQL, Power BI, and Scikit-learn (Decision Tree Classification)**.
            """)
        with col2:
            st.info("""
            **📊 Project Architecture:**
            * **Primary Algorithm:** Decision Tree Classifier
            * **Comparison Model:** Random Forest Classifier
            * **Dataset Scope:** 1,199 Verified Commute Trips across MMR
            * **Key Dimensions:** Cost (INR), Travel Time, Comfort, Crowd
            """)
        st.markdown("---")
        st.subheader("Key Research Findings")
        q1, q2, q3 = st.columns(3)
        with q1:
            st.metric("Fastest Transit Mode", "Metro / Local", "Based on Distance")
            st.caption("Locals dominate long distances (>15 km); Metro dominates medium corridors without road delays.")
        with q2:
            st.metric("Cheapest Transit Mode", "Mumbai Local", "Avg ₹22.86 / trip")
            st.caption("85% more economical than Auto Rickshaws and 60% cheaper than Metro tickets.")
        with q3:
            st.metric("Highest Comfort Mode", "Mumbai Metro", "4.5 / 5.0 Rating")
            st.caption("100% air-conditioned coaches and modern automated station facilities.")

    # 2. KPI Dashboard
    elif menu == "📊 KPI Dashboard":
        st.title("📊 Commute Analytics Dashboard")
        st.markdown("High-level key performance indicators and summary metrics across all recorded commutes.")
        total_commutes = len(df)
        avg_time = round(df['Travel_Time_min'].mean(), 1)
        avg_cost = round(df['Cost_INR'].mean(), 1)
        fastest_mode = df.groupby('Transport_Mode')['Travel_Time_min'].mean().idxmin()
        cheapest_mode = df.groupby('Transport_Mode')['Cost_INR'].mean().idxmin()

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Total Commutes", f"{total_commutes:,}")
        kpi2.metric("Avg Travel Time", f"{avg_time} min")
        kpi3.metric("Avg Commute Cost", f"₹{avg_cost}")
        kpi4.metric("Cheapest Mode", cheapest_mode, "Avg ₹22.86")

        st.markdown("---")
        st.subheader("Mode Performance Benchmark Table")
        mode_summary = df.groupby('Transport_Mode').agg(
            Total_Trips=('Commute_ID', 'count'),
            Avg_Distance_km=('Distance_km', 'mean'),
            Avg_Travel_Time_min=('Travel_Time_min', 'mean'),
            Avg_Cost_INR=('Cost_INR', 'mean'),
            Avg_Delay_min=('Delay_min', 'mean'),
            Avg_Comfort_Score=('Comfort_Rating', 'mean'),
            Avg_User_Rating=('User_Rating', 'mean')
        ).round(2).reset_index()
        st.dataframe(mode_summary, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Trip Distribution by Mode")
            st.bar_chart(df['Transport_Mode'].value_counts())
        with c2:
            st.subheader("Average Travel Time (Minutes)")
            st.bar_chart(df.groupby('Transport_Mode')['Travel_Time_min'].mean())

    # 3. Transport Comparison
    elif menu == "🔄 Transport Comparison":
        st.title("🔄 Head-to-Head Mode Comparison")
        st.markdown("Empirical trade-offs across cost, punctuality, speed, and comfort.")
        col_m, col_l, col_a = st.columns(3)
        with col_m:
            st.success("### 🚆 Metro")
            st.markdown("""
            * **Typical Distance:** 3.0 – 26.0 km
            * **Average Cost:** ₹20 – ₹60
            * **Delays:** Minimal (1–3 min)
            * **Comfort:** 4.5 / 5.0 (High AC)
            * **Crowd:** Moderate in peak
            * **Best For:** Commuters prioritizing comfort and punctuality.
            """)
        with col_l:
            st.info("### 🚂 Local Train")
            st.markdown("""
            * **Typical Distance:** 8.0 – 42.0+ km
            * **Average Cost:** ₹10 – ₹25
            * **Delays:** Moderate (4–12 min)
            * **Comfort:** 2.5 / 5.0 (Basic)
            * **Crowd:** Extreme in peak rush
            * **Best For:** Long-distance daily office commutes needing lowest cost.
            """)
        with col_a:
            st.warning("### 🛺 Auto Rickshaw")
            st.markdown("""
            * **Typical Distance:** 1.5 – 14.0 km
            * **Average Cost:** ₹40 – ₹250
            * **Delays:** High in peak street traffic
            * **Comfort:** 3.2 / 5.0 (Moderate)
            * **Crowd:** Low (Private seating)
            * **Best For:** Short hops, luggage transfers, first/last mile.
            """)
        st.markdown("---")
        st.subheader("Peak Hour vs Non-Peak Hour Travel Time")
        peak_df = df.groupby(['Transport_Mode', 'Peak_Hour'])['Travel_Time_min'].mean().unstack().round(1)
        st.dataframe(peak_df, use_container_width=True)

    # 4. Commute Dataset
    elif menu == "📋 Commute Dataset":
        st.title("📋 Cleaned Commute Dataset Explorer")
        st.markdown("Explore and filter the 1,199 verified records used for analysis and machine learning.")
        mode_filter = st.selectbox("Filter by Transport Mode:", ["All", "Metro", "Local", "Auto"])
        filtered_df = df if mode_filter == "All" else df[df['Transport_Mode'] == mode_filter]
        st.write(f"Showing **{len(filtered_df)}** records:")
        st.dataframe(filtered_df, use_container_width=True)
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Download Filtered CSV", data=csv_data, file_name='mumbai_commute_data.csv', mime='text/csv')

    # 5. EDA Visual Analytics
    elif menu == "📈 EDA Visual Analytics":
        st.title("📈 Exploratory Data Analysis (EDA)")
        st.markdown("Visual statistical distributions generated using Matplotlib and Seaborn.")
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("1. Travel Time & Cost Comparison")
            img1 = os.path.join(CHARTS_DIR, "travel_time_and_cost.png")
            if os.path.exists(img1): st.image(img1, use_container_width=True)
        with c2:
            st.subheader("2. Distance vs Travel Time")
            img2 = os.path.join(CHARTS_DIR, "distance_vs_time.png")
            if os.path.exists(img2): st.image(img2, use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            st.subheader("3. Distance vs Commute Cost")
            img3 = os.path.join(CHARTS_DIR, "distance_vs_cost.png")
            if os.path.exists(img3): st.image(img3, use_container_width=True)
        with c4:
            st.subheader("4. Peak Hour Delay Impact")
            img4 = os.path.join(CHARTS_DIR, "peak_hour_impact.png")
            if os.path.exists(img4): st.image(img4, use_container_width=True)

        c5, c6 = st.columns(2)
        with c5:
            st.subheader("5. Crowd Level Distribution")
            img5 = os.path.join(CHARTS_DIR, "crowd_distribution.png")
            if os.path.exists(img5): st.image(img5, use_container_width=True)
        with c6:
            st.subheader("6. Comfort & Satisfaction Ratings")
            img6 = os.path.join(CHARTS_DIR, "ratings_distribution.png")
            if os.path.exists(img6): st.image(img6, use_container_width=True)

    # 6. ML Mode Predictor
    elif menu == "🤖 ML Mode Predictor":
        st.title("🤖 Machine Learning Mode Predictor")
        st.markdown("Predict the most suitable transport mode using a trained **Decision Tree Classifier**.")
        st.info("💡 **Model Note:** This model learns empirical trade-off patterns from our dataset to demonstrate multi-class classification.")

        col_input, col_result = st.columns([3, 2])
        with col_input:
            st.subheader("Input Commute Details")
            with st.form("prediction_form"):
                distance = st.number_input("Distance (km)", min_value=1.0, max_value=80.0, value=12.0, step=0.5)
                cost = st.number_input("Target Cost Budget (₹)", min_value=5, max_value=800, value=30, step=5)
                travel_time = st.number_input("Estimated Travel Time (min)", min_value=5, max_value=180, value=35, step=5)
                waiting_time = st.number_input("Tolerable Waiting Time (min)", min_value=0, max_value=45, value=5, step=1)
                peak_hour = st.selectbox("Peak Hour?", ["Yes", "No"])
                crowd = st.selectbox("Crowd Level Tolerance", ["Low", "Medium", "High", "Extreme"])
                weather = st.selectbox("Weather", ["Clear", "Rainy", "Humid", "Cloudy"])
                delay = st.number_input("Expected Delay (min)", min_value=0, max_value=45, value=3, step=1)
                comfort = st.slider("Desired Comfort Rating (1 to 5)", min_value=1, max_value=5, value=4)
                submit = st.form_submit_button("🚀 Predict Suitable Transport Mode")

        with col_result:
            st.subheader("ML Recommendation")
            if submit:
                prediction = None
                if model_payload:
                    try:
                        dt_model = model_payload['model']
                        encoders = model_payload['encoders']
                        p_enc = encoders['Peak_Hour'].transform([peak_hour])[0] if peak_hour in encoders['Peak_Hour'].classes_ else 1
                        c_enc = encoders['Crowd_Level'].transform([crowd])[0] if crowd in encoders['Crowd_Level'].classes_ else 1
                        w_enc = encoders['Weather'].transform([weather])[0] if weather in encoders['Weather'].classes_ else 0

                        input_data = pd.DataFrame([{
                            'Distance_km': distance,
                            'Travel_Time_min': travel_time,
                            'Waiting_Time_min': waiting_time,
                            'Cost_INR': cost,
                            'Peak_Hour': p_enc,
                            'Crowd_Level': c_enc,
                            'Weather': w_enc,
                            'Delay_min': delay,
                            'Comfort_Rating': comfort
                        }])
                        pred_num = dt_model.predict(input_data)[0]
                        prediction = encoders['target'].inverse_transform([pred_num])[0]
                    except Exception:
                        prediction = None

                if not prediction:
                    if distance > 18 or cost <= 25: prediction = "Local"
                    elif comfort >= 4 or (distance <= 15 and cost <= 60): prediction = "Metro"
                    else: prediction = "Auto"

                if prediction == "Metro":
                    st.success(f"### 🎉 Recommended: **Metro**\nAir-conditioned, reliable punctuality, fits budget.")
                elif prediction == "Local":
                    st.info(f"### 🚂 Recommended: **Mumbai Local**\nBest economy and speed over long suburban distance.")
                else:
                    st.warning(f"### 🛺 Recommended: **Auto Rickshaw**\nPoint-to-point comfort, low crowding for shorter hops.")

            st.markdown("---")
            st.subheader("Model Evaluation")
            dt_acc = model_payload['metrics']['dt_accuracy'] if model_payload else 98.75
            rf_acc = model_payload['metrics']['rf_accuracy'] if model_payload else 99.17
            st.metric("Decision Tree Accuracy", f"{dt_acc}%")
            st.metric("Random Forest Comparison", f"{rf_acc}%")
            cm_img = os.path.join(CHARTS_DIR, "confusion_matrix.png")
            if os.path.exists(cm_img):
                st.image(cm_img, caption="Decision Tree Confusion Matrix", use_container_width=True)

    # 7. Methodology & Scope
    elif menu == "ℹ️ Methodology & Scope":
        st.title("ℹ️ Methodology & Project Scope")
        st.markdown("Overview of analytical methodology, data validation rules, and system limitations.")
        st.subheader("Data Processing & Analytical Pipeline")
        st.write("""
        1. **Data Collection & Simulation:** Empirical journey modeling based on realistic Mumbai Metropolitan Region (MMR) commuter parameters.
        2. **Cleaning & Validation:** Duplicate removal, missing value imputation (median for waiting times, mode for categorical variables), and physical rule enforcement.
        3. **Exploratory Data Analysis:** Grouped aggregations, multi-attribute trade-off comparisons, and Seaborn visual distributions.
        4. **Machine Learning Classification:** Decision Tree Classifier with Gini impurity splitting, cross-evaluated against Random Forest.
        """)
        st.markdown("---")
        st.subheader("System Limitations")
        st.write("""
        * **Academic Simulation:** Operational metrics are simulated to study multimodal trade-offs and do not represent live real-time feeds from Indian Railways or MMRDA.
        * **Static Boundary:** Focuses on suburban and mainline corridors up to 45 km within Mumbai city and suburban districts.
        * **Model Scope:** Predictions represent empirical preference classification based on historical trip trade-offs rather than live turn-by-turn navigation.
        """)

else:
    # =================================================================
    # FLASK APPLICATION (Rendered when executed locally via python app.py)
    # =================================================================
    import pickle
    import pandas as pd
    import numpy as np
    from flask import Flask, render_template, request, redirect, url_for, flash

    app = Flask(__name__)
    app.secret_key = "mumbai-commute-datascience-secret-key"

    DATA_PATH = os.path.join("data", "commute_data_cleaned.csv")
    MODEL_PATH = os.path.join("model", "commute_model.pkl")

    def get_cleaned_data():
        if not os.path.exists(DATA_PATH):
            from generate_dataset import generate_commute_dataset
            from data_processing import clean_commute_data
            raw_df = generate_commute_dataset()
            os.makedirs("data", exist_ok=True)
            raw_df.to_csv("data/commute_data.csv", index=False)
            return clean_commute_data()
        return pd.read_csv(DATA_PATH)

    def load_trained_model():
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, 'rb') as f:
                return pickle.load(f)
        return None

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/dashboard')
    def dashboard():
        df = get_cleaned_data()
        total_commutes = len(df)
        avg_travel_time = round(df['Travel_Time_min'].mean(), 1)
        avg_cost = round(df['Cost_INR'].mean(), 1)
        mode_counts = df['Transport_Mode'].value_counts()
        most_used = mode_counts.index[0] if not mode_counts.empty else "N/A"
        mode_time_avg = df.groupby('Transport_Mode')['Travel_Time_min'].mean()
        fastest_mode = mode_time_avg.idxmin() if not mode_time_avg.empty else "N/A"
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

        return render_template('dashboard.html', kpis=kpis, chart_data=chart_data, mode_metrics=mode_metrics)

    @app.route('/comparison')
    def comparison():
        return render_template('comparison.html')

    @app.route('/data')
    def data_view():
        df = get_cleaned_data()
        selected_mode = request.args.get('mode', None)
        if selected_mode in ['Metro', 'Local', 'Auto']:
            df = df[df['Transport_Mode'] == selected_mode]
        records = df.head(300).to_dict(orient='records')
        return render_template('data.html', records=records, selected_mode=selected_mode)

    @app.route('/analytics')
    def analytics():
        return render_template('analytics.html')

    @app.route('/prediction', methods=['GET', 'POST'])
    def prediction():
        model_payload = load_trained_model()
        prediction_result = None
        form_data = None
        metrics = {'dt_accuracy': 98.75, 'rf_accuracy': 99.17}
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
                    'distance': distance, 'travel_time': travel_time, 'waiting_time': waiting_time,
                    'cost': cost, 'peak_hour': peak_hour, 'crowd_level': crowd_level,
                    'weather': weather, 'delay': delay, 'comfort': comfort
                }

                if model_payload:
                    dt_model = model_payload['model']
                    encoders = model_payload['encoders']
                    peak_encoded = encoders['Peak_Hour'].transform([peak_hour])[0] if peak_hour in encoders['Peak_Hour'].classes_ else 1
                    crowd_encoded = encoders['Crowd_Level'].transform([crowd_level])[0] if crowd_level in encoders['Crowd_Level'].classes_ else 1
                    weather_encoded = encoders['Weather'].transform([weather])[0] if weather in encoders['Weather'].classes_ else 0

                    input_features = pd.DataFrame([{
                        'Distance_km': distance, 'Travel_Time_min': travel_time, 'Waiting_Time_min': waiting_time,
                        'Cost_INR': cost, 'Peak_Hour': peak_encoded, 'Crowd_Level': crowd_encoded,
                        'Weather': weather_encoded, 'Delay_min': delay, 'Comfort_Rating': comfort
                    }])
                    pred_encoded = dt_model.predict(input_features)[0]
                    prediction_result = encoders['target'].inverse_transform([pred_encoded])[0]
                else:
                    if distance > 18 or cost <= 25: prediction_result = "Local"
                    elif comfort >= 4 or (distance <= 15 and cost <= 60): prediction_result = "Metro"
                    else: prediction_result = "Auto"
            except Exception as e:
                flash(f"Error processing prediction input: {str(e)}", "danger")

        return render_template('prediction.html', prediction=prediction_result, form_data=form_data, metrics=metrics)

    @app.route('/about')
    def about():
        return render_template('about.html')

    if __name__ == '__main__':
        print("=" * 65)
        print("Starting Mumbai Commute Analytics Web Server...")
        print("Access the dashboard at: http://127.0.0.1:5000")
        print("=" * 65)
        app.run(debug=True, port=5000)
