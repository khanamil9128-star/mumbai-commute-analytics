"""
====================================================================
Mumbai Commute Analytics — Step 4: Machine Learning Model Training
File: train_model.py
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
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder

MODEL_DIR = "model"
CHARTS_DIR = os.path.join("static", "images")

def train_commute_classifier(clean_csv="data/commute_data_cleaned.csv"):
    if not os.path.exists(clean_csv):
        raise FileNotFoundError(f"Cleaned dataset '{clean_csv}' not found. Run data_processing.py first.")

    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(CHARTS_DIR, exist_ok=True)

    print("=" * 70)
    print("STEP 1: Loading Cleaned Dataset for Model Training")
    print("=" * 70)
    df = pd.read_csv(clean_csv)
    print(f"Total samples available: {len(df)}")

    # -------------------------------------------------------------
    # 2. Select Features (X) and Target (y)
    # -------------------------------------------------------------
    # Feature columns:
    # - Distance_km (float)
    # - Travel_Time_min (int)
    # - Waiting_Time_min (int)
    # - Cost_INR (int)
    # - Peak_Hour (categorical: Yes/No)
    # - Crowd_Level (categorical: Low/Medium/High/Extreme)
    # - Weather (categorical: Clear/Rainy/Humid/Cloudy)
    # - Delay_min (int)
    # - Comfort_Rating (int)
    feature_cols = [
        'Distance_km',
        'Travel_Time_min',
        'Waiting_Time_min',
        'Cost_INR',
        'Peak_Hour',
        'Crowd_Level',
        'Weather',
        'Delay_min',
        'Comfort_Rating'
    ]

    target_col = 'Transport_Mode'

    X = df[feature_cols].copy()
    y = df[target_col].copy()

    # -------------------------------------------------------------
    # 3. Categorical Encoding
    # -------------------------------------------------------------
    # We maintain individual LabelEncoders so we can cleanly invert or transform
    # inputs coming from user web form in Flask.
    encoders = {}

    categorical_features = ['Peak_Hour', 'Crowd_Level', 'Weather']
    for cat in categorical_features:
        le = LabelEncoder()
        X[cat] = le.fit_transform(X[cat].astype(str))
        encoders[cat] = le

    # Encode target variable
    target_encoder = LabelEncoder()
    y_encoded = target_encoder.fit_transform(y)
    encoders['target'] = target_encoder

    print("\nCategorical mappings learned:")
    for cat in categorical_features:
        mapping = dict(zip(encoders[cat].classes_, encoders[cat].transform(encoders[cat].classes_)))
        print(f"  {cat}: {mapping}")
    print(f"  Target Classes: {dict(zip(target_encoder.classes_, target_encoder.transform(target_encoder.classes_)))}\n")

    # -------------------------------------------------------------
    # 4. Train - Test Split
    # -------------------------------------------------------------
    # 80% Training Data, 20% Testing Data, stratified to preserve class ratios
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.20, random_state=42, stratify=y_encoded
    )
    print(f"Training Set Size: {len(X_train)} samples")
    print(f"Testing Set Size:  {len(X_test)} samples\n")

    # -------------------------------------------------------------
    # 5. Primary Model: Decision Tree Classifier
    # -------------------------------------------------------------
    # max_depth=5 helps keep the tree explainable and prevents overfitting
    dt_model = DecisionTreeClassifier(
        criterion='gini',
        max_depth=5,
        min_samples_split=10,
        random_state=42
    )
    dt_model.fit(X_train, y_train)

    # Evaluation
    y_pred_dt = dt_model.predict(X_test)
    dt_accuracy = accuracy_score(y_test, y_pred_dt)

    print("=" * 70)
    print("PRIMARY MODEL: DECISION TREE CLASSIFIER RESULTS")
    print("=" * 70)
    print(f"Decision Tree Accuracy: {dt_accuracy * 100:.2f}%\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred_dt, target_names=target_encoder.classes_))

    # Confusion Matrix Plot
    cm_dt = confusion_matrix(y_test, y_pred_dt)
    plt.figure(figsize=(7, 5.5))
    sns.heatmap(
        cm_dt, annot=True, fmt='d', cmap='Blues',
        xticklabels=target_encoder.classes_,
        yticklabels=target_encoder.classes_
    )
    plt.title("Decision Tree Confusion Matrix", fontsize=13, weight='bold')
    plt.xlabel("Predicted Mode")
    plt.ylabel("Actual Mode")
    plt.tight_layout()
    cm_path = os.path.join(CHARTS_DIR, "confusion_matrix.png")
    plt.savefig(cm_path, dpi=300)
    plt.close()
    print(f"Saved: {cm_path}")

    # Feature Importance Plot
    importances = dt_model.feature_importances_
    feat_df = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)

    print("\nFeature Importances (Decision Tree):")
    for idx, row in feat_df.iterrows():
        print(f"  {row['Feature']:<18}: {row['Importance']:.4f}")

    plt.figure(figsize=(8, 4.5))
    sns.barplot(x='Importance', y='Feature', data=feat_df, palette='viridis')
    plt.title("Feature Importance in Transport Mode Selection", fontsize=12, weight='bold')
    plt.xlabel("Relative Importance Score")
    plt.tight_layout()
    fi_path = os.path.join(CHARTS_DIR, "feature_importance.png")
    plt.savefig(fi_path, dpi=300)
    plt.close()
    print(f"Saved: {fi_path}")

    # -------------------------------------------------------------
    # 6. Optional Comparison Model: Random Forest Classifier
    # -------------------------------------------------------------
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        random_state=42
    )
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    rf_accuracy = accuracy_score(y_test, y_pred_rf)

    print("\n" + "=" * 70)
    print("OPTIONAL COMPARISON MODEL: RANDOM FOREST CLASSIFIER RESULTS")
    print("=" * 70)
    print(f"Random Forest Accuracy: {rf_accuracy * 100:.2f}%")
    print(f"Comparison: Random Forest ({rf_accuracy*100:.2f}%) vs Decision Tree ({dt_accuracy*100:.2f}%)")

    # -------------------------------------------------------------
    # 7. Save Model Artifacts
    # -------------------------------------------------------------
    model_payload = {
        'model': dt_model,
        'rf_model': rf_model,
        'feature_cols': feature_cols,
        'encoders': encoders,
        'metrics': {
            'dt_accuracy': round(dt_accuracy * 100, 2),
            'rf_accuracy': round(rf_accuracy * 100, 2),
            'feature_importance': feat_df.to_dict(orient='records')
        }
    }

    model_filepath = os.path.join(MODEL_DIR, "commute_model.pkl")
    with open(model_filepath, 'wb') as f:
        pickle.dump(model_payload, f)

    print("\n" + "=" * 70)
    print(f"SUCCESS: Trained model and preprocessing pipeline saved to: {model_filepath}")
    print("Academic Note: The model learns empirical commute trade-offs from the simulated dataset")
    print("and is intended for academic evaluation, not absolute real-world routing.")
    print("=" * 70)

    return model_payload

if __name__ == "__main__":
    train_commute_classifier()

