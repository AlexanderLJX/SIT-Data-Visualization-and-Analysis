import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import IsolationForest
import seaborn as sns

def plot_distribution(feature, df):
    # Convert "NAN" to actual NaN and change dtype to float
    df[feature] = pd.to_numeric(df[feature], errors='coerce')
    # Convert "NAN" to actual NaN and change dtype to float
    df[feature] = pd.to_numeric(df[feature], errors='coerce')

    # Drop NaN values for the plot (or you can fill them with a value like 0 or the mean)
    df = df.dropna()
    # Plotting
    # get maximum value of the column
    max_value = max(df[feature])
    # get the range of the column
    range_value = max_value - min(df[feature])
    plt.hist(df[feature], bins=np.arange(0, max_value+0.1, range_value/20), edgecolor='k', alpha=0.7)
    plt.title('Distribution of '+feature)
    plt.xlabel(feature)
    plt.ylabel('Number of Restaurants')
    plt.grid(axis='y', alpha=0.75)

    # Return the figure object
    return plt.gcf()    


def plot_hexbin(feature1, feature2, df):
    # Plotting the hexbin plot
    plt.hexbin(df[feature1], df[feature2], gridsize=25, cmap='Blues', bins='log')
    plt.colorbar(label='Count in Bin')
    plt.title('Density Plot of ' + feature1 + ' and ' + feature2)
    plt.xlabel(feature1)
    plt.ylabel(feature2)
    plt.grid(True)
    # plt.show()

    return plt.gcf()

def plot_scatter(feature1, feature2, df):
    # Plotting the scatter plot
    plt.scatter(df[feature1], df[feature2], alpha=0.7)
    plt.title('Scatter Plot of ' + feature1 + ' and ' + feature2)
    plt.xlabel(feature1)
    plt.ylabel(feature2)
    plt.grid(True)
    # add margin at the bottom to fit the x-axis label
    plt.subplots_adjust(bottom=0.2)
    # plt.show()

    return plt.gcf()

def plot_violin(feature1, feature2, df):
    # Creating the violin plot
    sns.violinplot(x=df[feature1], y=df[feature2])
    plt.title('Violin Plot of ' + feature2 + ' by ' + feature1)
    plt.xlabel(feature1)
    plt.ylabel(feature2)
    plt.grid(True)
    plt.subplots_adjust(bottom=0.2)  # Add margin at the bottom to fit the x-axis label
    

    # Return the current figure instance
    return plt.gcf()

def plot_line_chart(feature1, feature2=None, df=None):
    if feature2:
        # Group the DataFrame by feature1 and calculate the mean of feature2 for each group
        aggregated_data = df.groupby(feature1)[feature2].mean().reset_index()

        # Sorting the aggregated data based on feature1 to ensure a proper line plot.
        # This step is particularly important if feature1 represents a sequential variable like time.
        aggregated_data = aggregated_data.sort_values(by=feature1)

        # Plotting the line chart
        # make plot larger
        plt.plot(aggregated_data[feature1], aggregated_data[feature2], marker='o', linestyle='-', alpha=0.7)
        plt.title(f'Line Chart of {feature1} and Mean of {feature2}')
        plt.xlabel(feature1)
        plt.ylabel(f'Mean of {feature2}')
        plt.grid(True)
    else:
        # Group the DataFrame by the feature and count the number of occurrences for each group
        aggregated_data = df.groupby(feature1).size().reset_index(name='Count')

        # Sorting the aggregated data based on the feature to ensure a proper line plot.
        # This step is particularly important if the feature represents a sequential variable like time.
        aggregated_data = aggregated_data.sort_values(by=feature1)

        # Plotting the line chart
        plt.plot(aggregated_data[feature1], aggregated_data['Count'], marker='o', linestyle='-', alpha=0.7)
        plt.title(f'Line Chart of {feature1} Count')
        plt.xlabel(feature1)
        plt.ylabel('Count')
        plt.grid(True)

    # Adjust the bottom margin if the labels are particularly long
    plt.subplots_adjust(bottom=0.2)

    return plt.gcf()

def plot_bar_chart(feature1, feature2=None, df=None, filter_json=""):
    if feature2 is None:
        # if feature1 is a string, count each value
        if df[feature1].dtype == 'object':
            value_counts = df[feature1].value_counts()
            x_labels = value_counts.index
            counts = value_counts.values
            plt.bar(x_labels, counts, alpha=0.7)
            plt.title(f'Counts of {feature1}')
            plt.xlabel(feature1)
            plt.ylabel('Counts')
        else:
            # Calculate the mean of the specified feature
            mean_value = df[feature1].mean()
            xticks_label = feature1
            # if filter_json is not a str
            if type(filter_json) != str:
                if "column" in filter_json and "operator" in filter_json and "value" in filter_json:
                    xticks_label += "\n" + filter_json['column'] + filter_json['operator'] + filter_json['value']
                
            # Plotting the mean as a single bar
            plt.bar(xticks_label, mean_value, alpha=0.7)
            plt.title(f'Mean of {feature1}')
            plt.ylabel(f'Mean of {feature1}')
            plt.xlabel(feature1)
            plt.ylabel('Mean of ' + feature1)
    else:
        # Original functionality for handling two features
        if df[feature2].dtype == 'object':  # if feature2 is a string, count each value
            count_df = df.groupby(feature1)[feature2].value_counts().unstack().fillna(0)
            count_df.plot(kind='bar', stacked=True, alpha=0.7)
            plt.title('Bar Chart of ' + feature1 + ' by Count of ' + feature2)
        else:  # if feature2 is an int or float, take the mean of each value
            mean_df = df.groupby(feature1)[feature2].mean().reset_index()
            plt.bar(mean_df[feature1], mean_df[feature2], alpha=0.7)
            plt.title('Bar Chart of ' + feature1 + ' and Mean of ' + feature2)
        plt.xlabel(feature1)
        plt.ylabel('Count' if feature2 is None or df[feature2].dtype == 'object' else 'Mean of ' + feature2)
    plt.grid(True)
    # if more than 20 values in x-axis then rotate the x-axis labels 90 degree
    if len(df[feature1].unique()) > 20:
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.35)
    elif len(df[feature1].unique()) > 10:
        plt.xticks(rotation=45)
        plt.subplots_adjust(bottom=0.32)
    else:
        plt.xticks(rotation=20)  # Rotate x-axis labels for better readability if needed
        plt.subplots_adjust(bottom=0.3)  # Adjust the bottom margin to fit the x-axis labels

    # if more the 10 values in legends then remove the legends
    if feature2 is not None and len(df[feature2].unique()) > 10:
        plt.legend().remove()
    # plt.show()

    return plt.gcf()


def plot_pie_chart(feature1, df):
    # Count the occurrence of each unique value in the feature1 column
    counts = df[feature1].value_counts()

    # Limit to top 100 unique names if there are more than 100
    if len(counts) > 100:
        counts = counts[:100]


    # Prepare data for the pie chart
    labels = counts.index
    sizes = counts.values

    # Plotting the pie chart
    fig, ax = plt.subplots()  # This allows for more customization, such as adding a legend
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Adding a title
    plt.title(f'Pie Chart of {feature1}')

    # Uncomment the following line if you want to display the plot directly
    # plt.show()

    # Return the figure object for further manipulation or saving
    return plt.gcf()


def plot_linear_regression(features, target, df):
    # drop all the rows with NaN values based on the features
    df = df.dropna(subset=features + [target])
    if len(features) == 1:
        X = df[features]  # Independent variable
        y = df[target]  # Dependent variable

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Perform linear regression
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Plot results
        plt.scatter(X, y, color='blue', label='Actual data')  # Actual data points
        plt.plot(X_test, y_pred, color='red', linewidth=2, label='Linear regression line')  # Regression line
        plt.title(f'Linear Regression of {features[0]} and {target}')
        plt.xlabel(features[0])
        plt.ylabel(target)
        plt.legend()
        plt.show()
    else:
        
        # Split data into training and testing sets
        X = df[features]  # Independent variables
        y = df[target]    # Dependent variable

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Perform linear regression
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)

        # Since we're now dealing with multiple features, we cannot directly plot a line as before.
        # Instead, we can compare actual vs. predicted values or use a scatter plot for individual features if needed.
        plt.scatter(y_test, y_pred, color='blue', label='Predicted vs Actual')
        plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4, color='red', label='Ideal Fit')
        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plt.title('Actual vs. Predicted Values')
        plt.legend()
        # plt.show()

    return plt.gcf()

def plot_random_forest(features, target, data):
    # drop all the rows with NaN values based on the features and target
    data = data.dropna(subset=features + [target])
    # Encode the all features column
    for feature in features:
        label_encoder = LabelEncoder()
        data[feature] = label_encoder.fit_transform(data[feature])
    
    # Split the data into features and target variable
    X = data[features]
    y = data[target]
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the RandomForest model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    # Actual vs Predicted scatter plot
    plt.scatter(y_test, y_pred, color='blue', label='Actual vs. Predicted')
    # Perfect predictions line
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4, label='Perfect Predictions')
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.title('RandomForestRegressor Predictions')
    plt.legend()
    plt.show()
    
    # Return the current figure
    return plt.gcf()

def plot_isolation_forest(features, df):
    # Drop all the rows with NaN values based on the features
    df_clean = df.dropna(subset=features)
    
    # Initialize the IsolationForest model with adjusted parameters
    iso_forest = IsolationForest(n_estimators=100, max_samples='auto', contamination=0.01, random_state=42)
    
    # Use all features for training
    X = df_clean[features]
    iso_forest.fit(X)
    
    # Predict anomalies (-1 for outliers, 1 for inliers)
    preds = iso_forest.predict(X)
    
    # # Plotting
    # for feature in features:
    # Plot inliers
    plt.plot(df_clean[features[0]][preds == 1], df_clean[features[1]][preds == 1], 'o', alpha=0.7, label=f" Inliers")
    # Plot outliers
    plt.scatter(df_clean[features[0]][preds == -1], df_clean[features[1]][preds == -1], color='r', label=f" Outliers")
    
    plt.title(f'Anomaly Detection for {features[0]} and {features[1]}')
    plt.xlabel(features[0])
    plt.ylabel(features[1])
    plt.legend()
    plt.grid(True)

    return plt.gcf()