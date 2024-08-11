#!/usr/bin/env python
# coding: utf-8

# In[3]:


#Question1

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# 1. Load Data in Pandas
df = pd.read_csv('hepatitis_csv.csv')

# 2. Drop Columns That Aren’t Useful

# columns_to_drop = ['Column1', 'Column2']  # Adjust according to your data
# df = df.drop(columns=columns_to_drop)

# 3. Drop Rows with Missing Values
df = df.dropna()

# 4. Create Dummy Variables
df = pd.get_dummies(df, drop_first=True)

# 5. Take Care of Missing Data
# This step is not needed as we already dropped missing values. If additional handling is required, it should be done here.

# 6. Convert the Data Frame to NumPy
data = df.to_numpy()

# 7. Divide the Data Set into Training Data and Test Data
# Define features and target
X = data[:, :-1]  # Features
y = data[:, -1]   # Target

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(X,y)
# Print shapes of the splits to verify
print(f"Training data shape: {X_train.shape}, Test data shape: {X_test.shape}")
print(f"Training target shape: {y_train.shape}, Test target shape: {y_test.shape}")


# In[22]:


#question 2
#part a
import pandas as pd

# Create data
data = {
    'Study Time (hours)': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Score out of 10': [2, 3, 4, 4, 5, 6, 7, 7, 8, 9]
}

df_regression = pd.DataFrame(data)

df_regression.to_csv('study_time_scores.csv', index=False)


# In[5]:


#question2b
import numpy as np


df_regression = pd.read_csv('study_time_scores.csv')


X = df_regression['Study Time (hours)'].values
y = df_regression['Score out of 10'].values

# Add a column of ones for the intercept term
X = np.vstack((np.ones_like(X), X)).T
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
# Compute coefficients using normal equation
coefficients = np.linalg.inv(X.T @ X) @ X.T @ y
B0, B1 = coefficients

# Compute predictions
y_pred = X @ coefficients

# Compute RMSE
rmse = np.sqrt(np.mean((y - y_pred) ** 2))

print(f"Coefficients: B0 (intercept) = {B0}, B1 (slope) = {B1}")
print(f"RMSE = {rmse}")
print(f"Predicted responses: {y_pred}")


# In[6]:


#Question 2c
import matplotlib.pyplot as plt

# Scatter plot
plt.scatter(df_regression['Study Time (hours)'], df_regression['Score out of 10'], color='red', label='Data points')

# Plot regression line
x_vals = np.linspace(1, 10, 100)
y_vals = B0 + B1 * x_vals
plt.plot(x_vals, y_vals, color='blue', label='Regression line')

plt.xlabel('Study Time (hours)')
plt.ylabel('Score out of 10')
plt.legend()
plt.show()


# In[14]:


#question 2d

import numpy as np
import pandas as pd

# Load the CSV file
df_regression = pd.read_csv('study_time_scores.csv')

# Extract features and target
X = df_regression['Study Time (hours)'].values
y = df_regression['Score out of 10'].values
print(X.ndim)


# Pedhazur Formula
X_matrix = np.vstack((np.ones_like(X), X)).T
coefficients = np.linalg.inv(X_matrix.T @ X_matrix) @ X_matrix.T @ y
B0p, B1p = coefficients
print(f"Pedhazur Formula Coefficients: B0 (intercept) = {B0p}, B1 (slope) = {B1p}")

# Calculus Method
X_mean = np.mean(X)
y_mean = np.mean(y)


numerator = np.sum((X - X_mean) * (y - y_mean))
denominator = np.sum((X - X_mean) ** 2)
B1c = numerator / denominator


B0c = y_mean - B1c * X_mean
print(f"Calculus Method Coefficients: B0 (intercept) = {B0}, B1 (slope) = {B1}")


print(f"Pedhazur Formula Coefficients: B0 = {B0p}, B1 = {B1p}")
print(f"Calculus Method Coefficients: B0 = {B0c}, B1 = {B1c}")



# In[15]:


study_time = 10
predicted_score_pedhazur = B0p + B1p * study_time
print(f"Predicted score for {study_time} hours of study time (Pedhazur Formula): {predicted_score_pedhazur}")

# Predict score for 10 hours of study time using Calculus Method
predicted_score_calculus = B0c + B1c * study_time
print(f"Predicted score for {study_time} hours of study time (Calculus Method): {predicted_score_calculus}")


# In[20]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# File path
file_path = 'hepatitis_csv.csv'

# Check if the file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

# Load data from CSV
data = pd.read_csv(file_path)

# Print first few rows to understand data structure
print(data.head())

# Handle categorical and boolean columns
# Convert 'sex' from categorical to numeric
data['sex'] = pd.factorize(data['sex'])[0]  # Example: male=0, female=1

# Convert boolean columns to numeric
bool_columns = ['steroid', 'antivirals', 'fatigue', 'malaise', 'anorexia',
                'liver_big', 'liver_firm', 'spleen_palpable', 'spiders',
                'ascites', 'varices', 'histology']
data[bool_columns] = data[bool_columns].astype(int)

# Drop rows where target variable 'fatigue' is missing or non-numeric
data = data.dropna(subset=['fatigue'])
X = data[['age', 'sex']].values
y = data['fatigue'].values

# Add intercept term to X
X = np.hstack((np.ones((X.shape[0], 1)), X))

# a. Calculate Coefficients using Normal Equation (Pedhazur Formula)
try:
    B = np.linalg.inv(X.T @ X) @ X.T @ y
except np.linalg.LinAlgError as e:
    print(f"Matrix inversion error: {e}")
    B = np.zeros(X.shape[1])  # Default to zero coefficients in case of an error

# Extract B0 and B1
B0 = B[0]
B1 = B[1:]
print(f"Pedhazur Formula - Intercept (B0): {B0}, Slopes (B1): {B1}")

# Predict responses using the calculated coefficients
y_pred = X @ B

# Calculate RMSE
rmse = np.sqrt(((y - y_pred) ** 2).mean())
print(f"RMSE: {rmse}")

# b. Create Scatter Plot and Predicted Line
plt.scatter(data['age'], y, color='red', label='Data Points')

# Plot regression line
plt.plot(data['age'], y_pred, color='blue', label='Regression Line')

plt.xlabel('Age')
plt.ylabel('Fatigue')
plt.legend()
plt.show()

# c. Implement Gradient Descent Method
def compute_cost(X, y, B):
    m = len(y)
    predictions = X @ B
    cost = (1 / (2 * m)) * np.sum((predictions - y) ** 2)
    return cost

def gradient_descent(X, y, B, alpha, iterations):
    m = len(y)
    cost_history = np.zeros(iterations)
    
    for i in range(iterations):
        gradients = (1 / m) * (X.T @ (X @ B - y))
        B -= alpha * gradients
        cost_history[i] = compute_cost(X, y, B)
        
    return B, cost_history

# Initial parameters
alpha = 0.01
iterations = 1000
B_initial = np.zeros(X.shape[1])

# Run gradient descent
B_final, cost_history = gradient_descent(X, y, B_initial, alpha, iterations)
print(f"Gradient Descent - Intercept (B0): {B_final[0]}, Slopes (B1): {B_final[1:]}")

# d. Compare Coefficients
print("Pedhazur Coefficients:", B)
print("Gradient Descent Coefficients:", B_final)

# Predict y for a new data point using Pedhazur and Gradient Descent methods
new_data_point = np.array([1, 45, 0])  # Example data point: [Intercept, Age=45, Sex=0]
predicted_y_pedhazur = new_data_point @ B
predicted_y_gradient = new_data_point @ B_final
print(f"Predicted y for new data point using Pedhazur: {predicted_y_pedhazur}")
print(f"Predicted y for new data point using Gradient Descent: {predicted_y_gradient}")


# In[21]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# File path
file_path = 'hepatitis_csv.csv'

# Check if the file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

# Load data from CSV
data = pd.read_csv(file_path)

# Print first few rows to understand data structure
print(data.head())

# Handle categorical and boolean columns
# Convert 'sex' from categorical to numeric
data['sex'] = pd.factorize(data['sex'])[0]  # Example: male=0, female=1

# Handle missing values in boolean columns
bool_columns = ['steroid', 'antivirals', 'fatigue', 'malaise', 'anorexia',
                'liver_big', 'liver_firm', 'spleen_palpable', 'spiders',
                'ascites', 'varices', 'histology']

# Fill NaN values with False (or you could use any other default value)
data[bool_columns] = data[bool_columns].fillna(False)

# Convert boolean columns to integers
data[bool_columns] = data[bool_columns].astype(int)

# Drop rows where target variable 'fatigue' is missing
data = data.dropna(subset=['fatigue'])

# Extract features and target variable
X = data[['age', 'sex']].values
y = data['fatigue'].values

# Add intercept term to X
X = np.hstack((np.ones((X.shape[0], 1)), X))

# a. Calculate Coefficients using Normal Equation (Pedhazur Formula)
try:
    B = np.linalg.inv(X.T @ X) @ X.T @ y
except np.linalg.LinAlgError as e:
    print(f"Matrix inversion error: {e}")
    B = np.zeros(X.shape[1])  # Default to zero coefficients in case of an error

# Extract B0 and B1
B0 = B[0]
B1 = B[1:]
print(f"Pedhazur Formula - Intercept (B0): {B0}, Slopes (B1): {B1}")

# Predict responses using the calculated coefficients
y_pred = X @ B

# Calculate RMSE
rmse = np.sqrt(((y - y_pred) ** 2).mean())
print(f"RMSE: {rmse}")

# b. Create Scatter Plot and Predicted Line
plt.scatter(data['age'], y, color='red', label='Data Points')

# Plot regression line
plt.plot(data['age'], y_pred, color='blue', label='Regression Line')

plt.xlabel('Age')
plt.ylabel('Fatigue')
plt.legend()
plt.show()

# c. Implement Gradient Descent Method
def compute_cost(X, y, B):
    m = len(y)
    predictions = X @ B
    cost = (1 / (2 * m)) * np.sum((predictions - y) ** 2)
    return cost

def gradient_descent(X, y, B, alpha, iterations):
    m = len(y)
    cost_history = np.zeros(iterations)
    
    for i in range(iterations):
        gradients = (1 / m) * (X.T @ (X @ B - y))
        B -= alpha * gradients
        cost_history[i] = compute_cost(X, y, B)
        
    return B, cost_history

# Initial parameters
alpha = 0.01
iterations = 1000
B_initial = np.zeros(X.shape[1])

# Run gradient descent
B_final, cost_history = gradient_descent(X, y, B_initial, alpha, iterations)
print(f"Gradient Descent - Intercept (B0): {B_final[0]}, Slopes (B1): {B_final[1:]}")

# d. Compare Coefficients
print("Pedhazur Coefficients:", B)
print("Gradient Descent Coefficients:", B_final)

# Predict y for a new data point using Pedhazur and Gradient Descent methods
new_data_point = np.array([1, 45, 0])  # Example data point: [Intercept, Age=45, Sex=0]
predicted_y_pedhazur = new_data_point @ B
predicted_y_gradient = new_data_point @ B_final
print(f"Predicted y for new data point using Pedhazur: {predicted_y_pedhazur}")
print(f"Predicted y for new data point using Gradient Descent: {predicted_y_gradient}")


# In[ ]:




