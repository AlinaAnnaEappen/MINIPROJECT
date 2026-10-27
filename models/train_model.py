import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, mean_absolute_error, r2_score
)

def prepare_data(filepath="data/Perception_of_Safety_Updated.xlsx"):
    df = pd.read_excel(filepath)
    
    # Clean column names
    col_mapping = {
        'CCTV surveillance': 'cctv',
        'Female staff presence': 'female_staff',
        'Lighting at stops': 'lighting',
        'Emergency buttons': 'emergency_buttons',
        'Driver background verification': 'driver_verified',
        'Perceived Safety Score (1-10)': 'safety_score',
        'Crowd Density': 'crowd_density',
        'Time of Day': 'time_of_day'
    }
    # Handle the encoding issue in 'Reserved women’s seats'
    for c in df.columns:
        if 'Reserved women' in c or 'women' in c.lower() and 'seat' in c.lower():
            col_mapping[c] = 'reserved_seats'
        if 'Public awareness' in c:
            col_mapping[c] = 'announcements'

    df = df.rename(columns=col_mapping)
    
    # Feature transformations to binary / numerical
    # 1. cctv: Present -> 1, Absent -> 0
    df['cctv'] = df['cctv'].apply(lambda x: 1 if str(x).strip().lower() == 'present' else 0)
    
    # 2. female_staff: Present -> 1, NaN/other -> 0
    df['female_staff'] = df['female_staff'].apply(lambda x: 1 if str(x).strip().lower() == 'present' else 0)
    
    # 3. lighting: Adequate -> 1, Poor -> 0
    df['lighting'] = df['lighting'].apply(lambda x: 1 if str(x).strip().lower() == 'adequate' else 0)
    
    # 4. emergency_buttons: Present -> 1, Absent -> 0
    df['emergency_buttons'] = df['emergency_buttons'].apply(lambda x: 1 if 'present' in str(x).strip().lower() else 0)
    
    # 5. reserved_seats: Strictly enforced -> 1, Poorly enforced -> 0
    if 'reserved_seats' in df.columns:
        df['reserved_seats'] = df['reserved_seats'].apply(lambda x: 1 if 'strict' in str(x).strip().lower() else 0)
    else:
        df['reserved_seats'] = 0

    # 6. announcements: Frequent -> 1, NaN -> 0
    if 'announcements' in df.columns:
        df['announcements'] = df['announcements'].apply(lambda x: 1 if 'frequent' in str(x).strip().lower() else 0)
    else:
        df['announcements'] = 0

    # 7. driver_verified: Displayed -> 1, Not visible -> 0
    df['driver_verified'] = df['driver_verified'].apply(lambda x: 1 if 'display' in str(x).strip().lower() else 0)
    
    # 8. crowd_density: High -> 1, Low -> 0
    df['crowd_high'] = df['crowd_density'].apply(lambda x: 1 if str(x).strip().lower() == 'high' else 0)
    
    # 9. time_of_day: Night -> 1, Day -> 0 (is_night)
    df['is_night'] = df['time_of_day'].apply(lambda x: 1 if str(x).strip().lower() == 'night' else 0)

    # Feature List
    feature_cols = [
        'cctv', 'female_staff', 'lighting', 'emergency_buttons',
        'reserved_seats', 'announcements', 'driver_verified',
        'crowd_high', 'is_night'
    ]
    
    X = df[feature_cols]
    y_raw = df['safety_score']  # 1 - 10
    
    # Normalized score to 0-100 percentage
    y_pct = ((y_raw - 1) / 9.0) * 100.0
    
    # 3-Class Categorization:
    # Class 0: Caution / Lower Comfort (Score <= 6, approx < 55%)
    # Class 1: Moderate Comfort (Score 7, approx 55% - 74%)
    # Class 2: High Comfort / Favorable (Score >= 8, approx >= 75%)
    def categorize(score):
        if score <= 6:
            return 0  # Caution
        elif score == 7:
            return 1  # Moderate
        else:
            return 2  # Favorable
            
    y_class = y_raw.apply(categorize)
    
    return X, y_pct, y_class, feature_cols

def train_and_evaluate():
    print("=== Training SHE SHIELD Machine Learning Models ===")
    X, y_pct, y_class, feature_cols = prepare_data()
    print(f"Loaded dataset: {X.shape[0]} samples with {X.shape[1]} features.")
    
    # Split
    X_train, X_test, y_reg_train, y_reg_test, y_cls_train, y_cls_test = train_test_split(
        X, y_pct, y_class, test_size=0.20, random_state=42, stratify=y_class
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 1. Baseline Model: Logistic Regression
    log_reg = LogisticRegression(max_iter=1000, random_state=42)
    log_reg.fit(X_train_scaled, y_cls_train)
    log_preds = log_reg.predict(X_test_scaled)
    log_acc = accuracy_score(y_cls_test, log_preds)
    log_f1 = f1_score(y_cls_test, log_preds, average='weighted')
    
    # 2. Final Model: Gradient Boosting Classifier
    gb_clf = GradientBoostingClassifier(n_estimators=120, learning_rate=0.08, max_depth=3, random_state=42)
    gb_clf.fit(X_train, y_cls_train)
    gb_preds = gb_clf.predict(X_test)
    gb_acc = accuracy_score(y_cls_test, gb_preds)
    gb_prec = precision_score(y_cls_test, gb_preds, average='weighted', zero_division=0)
    gb_rec = recall_score(y_cls_test, gb_preds, average='weighted', zero_division=0)
    gb_f1 = f1_score(y_cls_test, gb_preds, average='weighted', zero_division=0)
    cm = confusion_matrix(y_cls_test, gb_preds).tolist()
    
    # 3. Continuous Regressor for smooth probability calibration
    gb_reg = GradientBoostingRegressor(n_estimators=120, learning_rate=0.08, max_depth=3, random_state=42)
    gb_reg.fit(X_train, y_reg_train)
    reg_preds = gb_reg.predict(X_test)
    mae = mean_absolute_error(y_reg_test, reg_preds)
    r2 = r2_score(y_reg_test, reg_preds)
    
    # Feature Importances
    feature_importances = dict(zip(feature_cols, [round(float(v), 4) for v in gb_clf.feature_importances_]))
    sorted_importances = dict(sorted(feature_importances.items(), key=lambda item: item[1], reverse=True))
    
    print("\n--- Model Evaluation Summary ---")
    print(f"Logistic Regression (Baseline) Accuracy: {log_acc * 100:.2f}%, F1: {log_f1:.4f}")
    print(f"Gradient Boosting Classifier Accuracy:   {gb_acc * 100:.2f}%")
    print(f"Gradient Boosting Precision (Weighted): {gb_prec:.4f}")
    print(f"Gradient Boosting Recall (Weighted):    {gb_rec:.4f}")
    print(f"Gradient Boosting F1 Score (Weighted):  {gb_f1:.4f}")
    print(f"Gradient Boosting Regressor MAE:        {mae:.2f}% (R^2: {r2:.3f})")
    print("\nConfusion Matrix (Classes: 0=Caution, 1=Moderate, 2=Favorable):")
    print(np.array(cm))
    print("\nFeature Importances:")
    for f, imp in sorted_importances.items():
        print(f"  {f:20s}: {imp:.4f}")
        
    # Serialize Models
    os.makedirs("models", exist_ok=True)
    joblib.dump(gb_clf, "models/transit_safety_model.pkl")
    joblib.dump(gb_reg, "models/transit_safety_regressor.pkl")
    joblib.dump(log_reg, "models/logistic_model.pkl")
    joblib.dump(scaler, "models/transit_scaler.pkl")
    
    report = {
        "dataset_name": "Empirical Public Transit Safety Perception Dataset",
        "sample_size": len(X),
        "features": feature_cols,
        "classes": ["Caution (<=6/10)", "Moderate (7/10)", "Favorable (>=8/10)"],
        "baseline_logistic_regression": {
            "accuracy": round(float(log_acc), 4),
            "f1_score": round(float(log_f1), 4)
        },
        "gradient_boosting_classifier": {
            "accuracy": round(float(gb_acc), 4),
            "precision_weighted": round(float(gb_prec), 4),
            "recall_weighted": round(float(gb_rec), 4),
            "f1_score_weighted": round(float(gb_f1), 4),
            "confusion_matrix": cm,
            "feature_importances": sorted_importances
        },
        "gradient_boosting_regressor": {
            "mae_percentage": round(float(mae), 2),
            "r2_score": round(float(r2), 4)
        }
    }
    
    with open("models/model_evaluation_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    print("\nSaved models and evaluation report to models/ directory successfully!")

if __name__ == "__main__":
    train_and_evaluate()
