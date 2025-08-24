#!/usr/bin/env python3
"""
Test script for Wine Classification Challenge
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, recall_score
from sklearn.datasets import load_wine
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt

def main():
    print("🍷 Wine Classification Challenge Test")
    print("=" * 50)
    
    # Load the wine dataset
    wine = load_wine()
    data = pd.DataFrame(wine.data, columns=wine.feature_names)
    data['target'] = wine.target
    
    print(f"✅ Dataset loaded successfully!")
    print(f"   Shape: {data.shape}")
    print(f"   Classes: {wine.target_names}")
    print(f"   Class distribution: {data['target'].value_counts().to_dict()}")
    
    # Prepare data
    X = data.drop('target', axis=1)
    y = data['target']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"✅ Data prepared successfully!")
    print(f"   Training set: {X_train_scaled.shape}")
    print(f"   Test set: {X_test_scaled.shape}")
    
    # Test models
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'SVM': SVC(random_state=42)
    }
    
    results = {}
    best_recall = 0
    best_model_name = ""
    
    print(f"\n🧪 Testing models:")
    print("-" * 30)
    
    for name, model in models.items():
        # Train model
        model.fit(X_train_scaled, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test_scaled)
        
        # Calculate recall
        recall = recall_score(y_test, y_pred, average='macro')
        
        results[name] = {
            'model': model,
            'recall': recall
        }
        
        if recall > best_recall:
            best_recall = recall
            best_model_name = name
        
        print(f"   {name}: {recall:.4f}")
    
    print(f"\n🏆 Best Model: {best_model_name}")
    print(f"   Recall Score: {best_recall:.4f}")
    print(f"   Target (>95%) achieved: {'✅ YES' if best_recall > 0.95 else '❌ NO'}")
    
    # Test on challenge samples
    sample_1 = [13.72, 1.43, 2.5, 16.7, 108, 3.4, 3.67, 0.19, 2.04, 6.8, 0.89, 2.87, 1285]
    sample_2 = [12.37, 0.94, 1.36, 10.6, 88, 1.98, 0.57, 0.28, 0.42, 1.95, 1.05, 1.82, 520]
    
    new_samples = pd.DataFrame([sample_1, sample_2], columns=X.columns)
    new_samples_scaled = scaler.transform(new_samples)
    
    best_model = results[best_model_name]['model']
    predictions = best_model.predict(new_samples_scaled)
    
    print(f"\n🎯 Challenge Sample Predictions:")
    print(f"   Sample 1: {wine.target_names[predictions[0]]}")
    print(f"   Sample 2: {wine.target_names[predictions[1]]}")
    
    print(f"\n✅ Wine Classification Challenge completed successfully!")
    return True

if __name__ == "__main__":
    main()