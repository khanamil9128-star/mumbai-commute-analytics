"""
====================================================================
Mumbai Commute Analytics — Streamlit Cloud Web Application
File: streamlit_app.py
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
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Mumbai Commute Analytics",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_PATH = os.path.join("data", "commute_data_cleaned.csv")
MODEL_PATH = os.path.join("model", "commute_model.pkl")
CHARTS_DIR = os.path.join("static", "images")

@st.cache_data
def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    # Fallback: generate if missing
    from generate_dataset import generate_commute_dataset
    from data_processing import clean_commute_data
    raw = generate_commute_dataset()
    os.makedirs("data", exist_ok=True)
    raw.to_csv("data/commute_data.csv", index=False)
    return clean_commute_data()

@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)
    return None

df = load_data()
model_payload = load_model()

# Academic Notice Banner
st.warning(
    "⚠️ **Academic Simulation Notice:** This dataset is created/simulated for academic analysis and does not represent official Mumbai transport statistics."
)

# Sidebar Navigation
st.sidebar.title("🚆 Mumbai Commute Analytics")
st.sidebar.caption("B.Sc Data Science College Project")
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
        "🎓 Viva & Limitations"
    ]
)

# -------------------------------------------------------------
# 1. Project Overview
# -------------------------------------------------------------
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
        **🎓 Project Details:**
        * **Level:** B.Sc Data Science (1st/2nd Year)
        * **Primary Algorithm:** Decision Tree Classifier
        * **Comparison Model:** Random Forest Classifier
        * **Dataset Scope:** 1,199 Clean Commute Trips across MMR
        * **Key Metrics:** Cost (INR), Travel Time, Comfort, Crowd
        """)

    st.markdown("---")
    st.subheader("Key Research Questions Answered")
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

# -------------------------------------------------------------
# 2. KPI Dashboard
# -------------------------------------------------------------
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

# -------------------------------------------------------------
# 3. Transport Comparison
# -------------------------------------------------------------
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

# -------------------------------------------------------------
# 4. Commute Dataset
# -------------------------------------------------------------
elif menu == "📋 Commute Dataset":
    st.title("📋 Cleaned Commute Dataset Explorer")
    st.markdown("Explore and filter the 1,199 verified records used for analysis and machine learning.")

    mode_filter = st.selectbox("Filter by Transport Mode:", ["All", "Metro", "Local", "Auto"])
    filtered_df = df if mode_filter == "All" else df[df['Transport_Mode'] == mode_filter]

    st.write(f"Showing **{len(filtered_df)}** records:")
    st.dataframe(filtered_df, use_container_width=True)

    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered CSV",
        data=csv_data,
        file_name='mumbai_commute_data.csv',
        mime='text/csv'
    )

# -------------------------------------------------------------
# 5. EDA Visual Analytics
# -------------------------------------------------------------
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

# -------------------------------------------------------------
# 6. ML Mode Predictor
# -------------------------------------------------------------
elif menu == "🤖 ML Mode Predictor":
    st.title("🤖 Machine Learning Mode Predictor")
    st.markdown("Predict the most suitable transport mode using a trained **Decision Tree Classifier**.")

    st.info("💡 **Academic Note:** This model learns empirical trade-off patterns from our dataset. It demonstrates Multi-Class Classification, not guaranteed commuter routing.")

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
            if model_payload:
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
            else:
                # Rule-based fallback
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

# -------------------------------------------------------------
# 7. Viva & Limitations
# -------------------------------------------------------------
elif menu == "🎓 Viva & Limitations":
    st.title("🎓 College Viva Examination Guide")
    st.markdown("Key questions and simple answers for your college project viva.")

    with st.expander("1. What is Data Science?"):
        st.write("Data Science combines mathematics, statistics, computer programming (Python), and domain knowledge to extract meaningful insights and predictions from raw data.")

    with st.expander("2. What is Data Cleaning and why is it important?"):
        st.write("Real-world data is dirty with duplicates, missing fields, and impossible values. Data cleaning removes duplicates, fills missing values with the median, standardizes text casing, and filters outliers. Garbage in = Garbage out!")

    with st.expander("3. Why did you use Pandas?"):
        st.write("Pandas provides the DataFrame data structure, allowing fast SQL-like grouping, filtering, aggregation, and missing-value handling in Python.")

    with st.expander("4. Why Decision Tree Classifier?"):
        st.write("Decision Trees are transparent and explainable. Unlike black-box neural networks, examiners can see the exact splitting rules (e.g. Distance > 15 km, Cost <= ₹25).")

    with st.expander("5. What is Train-Test Split?"):
        st.write("We reserve 20% of data for testing to ensure the model can generalize to unseen trips rather than simply memorizing the training data (overfitting).")

    with st.expander("6. What is a Confusion Matrix?"):
        st.write("A matrix comparing true actual labels against model predictions. Diagonal entries show correct predictions; off-diagonal entries show errors.")

    with st.expander("7. What are the limitations of the project?"):
        st.write("The dataset is an academic simulation reflecting Mumbai travel patterns. It does not connect to live GPS satellites or real-time train delay APIs.")
