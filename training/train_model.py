import os
import sys
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def train_crop_model():
    dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'crop_data.csv')
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'model')
    model_path = os.path.join(model_dir, 'crop_model.pkl')
    
    print(f"--- Loading dataset from: {dataset_path} ---")
    if not os.path.exists(dataset_path):
        print(f"ERROR: Dataset file not found at {dataset_path}")
        sys.exit(1)
        
    df = pd.read_csv(dataset_path)
    
    required_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label']
    for col in required_cols:
        if col not in df.columns:
            print(f"ERROR: Missing required column '{col}' in dataset.")
            sys.exit(1)
            
    print(f"Dataset Shape: {df.shape}")
    print(f"Number of Missing Values:\n{df.isnull().sum()}")
    
    # Handle missing values if any
    df = df.dropna()
    
    feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    X = df[feature_cols]
    y = df['label']
    
    print(f"Unique Crops ({len(y.unique())}): {sorted(y.unique())}")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("--- Training Random Forest Classifier ---")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    y_pred = rf_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n==========================================")
    print(f"Model Training Completed Successfully!")
    print(f"Test Accuracy: {accuracy * 100:.2f}%")
    print(f"==========================================\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(rf_model, model_path)
    print(f"Trained model saved to: {model_path}")
    print("Feature Order preserved:", feature_cols)

if __name__ == '__main__':
    train_crop_model()
