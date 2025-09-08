# Wine Classification Challenge 🍷

**Status**: ✅ **COMPLETED** - Achieved 100% Recall (Target: >95%)

## Challenge Overview

This project implements a machine learning solution to classify wine samples by cultivar using 12 numeric features. The dataset contains 3 wine varieties (classes 0, 1, 2) from the UCI Machine Learning Repository.

## 🎯 Results Summary

| Model | Recall Score | Target Achieved |
|-------|--------------|----------------|
| **Random Forest** | **100.0%** | ✅ **YES** |
| Logistic Regression | 96.7% | ✅ YES |
| SVM | 96.7% | ✅ YES |

## 📁 Project Structure

```
03-wine-classification-challenge/
├── wine_classification_challenge.ipynb  # Complete Jupyter notebook
├── test_wine_classification.py          # Validation script
├── requirements.txt                     # Python dependencies
├── wine-env/                           # Virtual environment
└── README.md                           # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment support

### Setup & Run

```bash
# Navigate to project directory
cd 03-wine-classification-challenge

# Activate virtual environment
source wine-env/bin/activate

# Run test script
python test_wine_classification.py

# Or start Jupyter for interactive notebook
jupyter notebook wine_classification_challenge.ipynb
```

## 🧪 What the Solution Demonstrates

1. **Data Loading & Exploration**
   - Uses sklearn's built-in wine dataset
   - Exploratory data analysis with visualizations
   - Statistical summaries and class distribution analysis

2. **Data Preprocessing**
   - Feature scaling using StandardScaler
   - Train/test split with stratification
   - Proper data preparation practices

3. **Model Comparison**
   - Random Forest Classifier
   - Logistic Regression
   - Support Vector Machine (SVM)
   - Cross-validation for robust evaluation

4. **Performance Evaluation**
   - Recall scoring (macro-averaged)
   - Classification reports
   - Confusion matrix visualization
   - Model comparison charts

5. **Real-world Application**
   - Predictions on new wine samples
   - Challenge sample classification:
     - Sample 1: `class_0`
     - Sample 2: `class_1`

## 📊 Technical Details

**Dataset**: Wine Recognition Dataset from UCI ML Repository
- **Samples**: 178 wines
- **Features**: 13 chemical properties
- **Classes**: 3 wine cultivars
- **Source**: Originally collected by Forina, M. et al.

**Best Model**: Random Forest
- **Parameters**: 100 estimators, random_state=42
- **Performance**: 100% recall on test set
- **Validation**: 5-fold cross-validation

## 📈 Model Performance Breakdown

The Random Forest classifier achieved perfect classification on the test set:
- **Precision**: 100% across all classes
- **Recall**: 100% across all classes  
- **F1-Score**: 100% across all classes
- **Accuracy**: 100%

## 🎓 Learning Objectives Met

✅ Data exploration and visualization  
✅ Multiple ML algorithm implementation  
✅ Model comparison and selection  
✅ Performance evaluation with proper metrics  
✅ Target recall >95% achieved (100%)  
✅ Real-world prediction capability  

## 🔗 Related Resources

- [Original Microsoft Challenge](https://github.com/MicrosoftDocs/ml-basics/blob/master/challenges/03%20-%20Wine%20Classification%20Challenge.ipynb)
- [UCI Wine Dataset](https://archive.ics.uci.edu/ml/datasets/wine)
- [Scikit-learn Documentation](https://scikit-learn.org/stable/)

## 📝 Notes

This implementation exceeds the challenge requirements with perfect recall performance. The solution demonstrates proper machine learning practices including data preprocessing, model comparison, cross-validation, and comprehensive evaluation.

---

*Part of Azure AI Engineer Learning Journey - Machine Learning Fundamentals Module*