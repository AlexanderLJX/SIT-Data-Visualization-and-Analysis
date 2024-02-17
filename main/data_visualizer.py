import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def plot_distribution(feature, df):
    # Convert "NAN" to actual NaN and change dtype to float
    df[feature] = pd.to_numeric(df[feature], errors='coerce')

    # Drop NaN values for the plot (or you can fill them with a value like 0 or the mean)
    df = df.dropna()

    # Plotting
    plt.figure(figsize=(10, 6))  # Adjust the size as needed
    plt.hist(df[feature], bins=np.arange(0, 5.1, 0.25), edgecolor='k', alpha=0.7)
    plt.title('Distribution of'+feature)
    plt.xlabel(feature)
    plt.ylabel('Number of Restaurants')
    plt.grid(axis='y', alpha=0.75)

    plt.show()


def plot_hexbin(feature1, feature2, df):
    # Plotting the hexbin plot
    plt.figure(figsize=(12, 6))
    plt.hexbin(df[feature1], df[feature2], gridsize=25, cmap='Blues', bins='log')
    plt.colorbar(label='Count in Bin')
    plt.title('Density Plot of Average Opening Hours and Star Rating')
    plt.xlabel(feature1)
    plt.ylabel(feature2)
    plt.grid(True)
    plt.show()

def plot_linear_regression(feature1, feature2, df):
    # Split data into training and testing sets
    X = df[[feature1]]  # Independent variable
    y = df[feature2]  # Dependent variable

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Perform linear regression
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)

    # Plot results
    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color='blue', label='Actual data')  # Actual data points
    plt.plot(X_test, y_pred, color='red', linewidth=2, label='Linear regression line')  # Regression line
    plt.title('Relationship between', feature1, 'and', feature2)
    plt.xlabel(feature1)
    plt.ylabel(feature2)
    plt.legend()
    plt.show()