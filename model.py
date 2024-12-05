import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import pickle

# Load dataset
dataset = pd.read_csv('diabetes.csv')

# Replace 0s with NaN and handle missing data
dataset[["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]] = dataset[["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]].replace(0, np.NaN)
dataset["Glucose"].fillna(dataset["Glucose"].mean(), inplace=True)
dataset["BloodPressure"].fillna(dataset["BloodPressure"].mean(), inplace=True)
dataset["SkinThickness"].fillna(dataset["SkinThickness"].mean(), inplace=True)
dataset["Insulin"].fillna(dataset["Insulin"].mean(), inplace=True)
dataset["BMI"].fillna(dataset["BMI"].mean(), inplace=True)

# Feature selection and scaling
X = dataset.iloc[:, [1, 4, 5, 7]].values  # Glucose, Insulin, BMI, Age
Y = dataset.iloc[:, 8].values  # Outcome
scaler = MinMaxScaler(feature_range=(0, 1))
X_scaled = scaler.fit_transform(X)

# Split dataset
X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.20, random_state=42, stratify=dataset['Outcome'])

# Train K-Nearest Neighbors classifier
knn = KNeighborsClassifier(n_neighbors=24, metric='minkowski', p=2)
knn.fit(X_train, Y_train)

# Save the model and scaler
pickle.dump(knn, open('model.pkl', 'wb'))
pickle.dump(scaler, open('scaler.pkl', 'wb'))
