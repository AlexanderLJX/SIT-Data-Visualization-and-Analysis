import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

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
    plt.figure(figsize=(20, 20))
    plt.hist(df[feature], bins=np.arange(0, max_value+0.1, range_value/20), edgecolor='k', alpha=0.7)
    plt.title('Distribution of '+feature)
    plt.xlabel(feature)
    plt.ylabel('Number of Restaurants')
    plt.grid(axis='y', alpha=0.75)

    # Return the figure object
    return plt.gcf()    


def plot_hexbin(feature1, feature2, df):
    # Plotting the hexbin plot
    plt.figure(figsize=(20, 20))
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
    plt.figure(figsize=(20, 20))
    plt.scatter(df[feature1], df[feature2], alpha=0.7)
    plt.title('Scatter Plot of Average Opening Hours and Star Rating')
    plt.xlabel(feature1)
    plt.ylabel(feature2)
    plt.grid(True)
    # add margin at the bottom to fit the x-axis label
    plt.subplots_adjust(bottom=0.2)
    # plt.show()

    return plt.gcf()

def plot_line_chart(feature1, feature2, df):
    # Group the DataFrame by feature1 and calculate the mean of feature2 for each group
    aggregated_data = df.groupby(feature1)[feature2].mean().reset_index()

    # Sorting the aggregated data based on feature1 to ensure a proper line plot.
    # This step is particularly important if feature1 represents a sequential variable like time.
    aggregated_data = aggregated_data.sort_values(by=feature1)

    # Plotting the line chart
    # make plot larger
    plt.figure(figsize=(20, 20))
    plt.plot(aggregated_data[feature1], aggregated_data[feature2], marker='o', linestyle='-', alpha=0.7)
    plt.title(f'Line Chart of {feature1} and Mean of {feature2}')
    plt.xlabel(feature1)
    plt.ylabel(f'Mean of {feature2}')
    plt.grid(True)

    # Adjust the bottom margin if the labels are particularly long
    plt.subplots_adjust(bottom=0.2)

    return plt.gcf()

def plot_bar_chart(feature1, feature2=None, df=None, filter_json=None):
    if feature2 is None:
        # Calculate the mean of the specified feature
        mean_value = df[feature1].mean()
        if filter_json is not None:
            xticks_label = feature1
            for filter in filter_json:
                xticks_label += "\n" + filter['column'] + filter['operator'] + filter['value']
            
        # Plotting the mean as a single bar
        plt.bar(xticks_label, mean_value, alpha=0.7)
        plt.title(f'Mean of {feature1}')
        plt.ylabel(f'Mean of {feature1}')
        # Adjusting plot aesthetics for clarity
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
    
    plt.figure(figsize=(20, 20))
    plt.xlabel(feature1)
    plt.ylabel('Count' if feature2 is None or df[feature2].dtype == 'object' else 'Mean of ' + feature2)
    plt.grid(True)
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

    # Prepare data for the pie chart
    labels = counts.index
    sizes = counts.values

    # Plotting the pie chart
    plt.figure(figsize=(20, 20))
    fig, ax = plt.subplots()  # This allows for more customization, such as adding a legend
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Adding a title
    plt.title(f'Pie Chart of {feature1}')

    # Uncomment the following line if you want to display the plot directly
    # plt.show()

    # Return the figure object for further manipulation or saving
    return plt.gcf()


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
    plt.figure(figsize=(20, 20))
    plt.scatter(X, y, color='blue', label='Actual data')  # Actual data points
    plt.plot(X_test, y_pred, color='red', linewidth=2, label='Linear regression line')  # Regression line
    plt.title('Relationship between', feature1, 'and', feature2)
    plt.xlabel(feature1)
    plt.ylabel(feature2)
    plt.legend()
    # plt.show()

    return plt.gcf()

def plot_anomaly_detection(feature, df):
    # Convert "NAN" to actual NaN and change dtype to float
    df[feature] = pd.to_numeric(df[feature], errors='coerce')

    # Drop NaN values for the plot (or you can fill them with a value like 0 or the mean)
    df = df.dropna()

    # Plotting
    plt.plot(df[feature], alpha=0.7)
    plt.title('Anomaly Detection of ' + feature)
    plt.xlabel('Index')
    plt.ylabel(feature)
    plt.grid(True)
    # plt.show()

    return plt.gcf()