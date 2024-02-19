# Imports and Constants
import pandas as pd
import ast  # To safely evaluate strings containing Python expressions from a string-based input
import constants
from datetime import datetime
from util import readfile
import os

## Data Loading and Preprocessing
# check if file exists
main_csv_path = 'main/main_preprocessed.csv'
review_csv_path = 'main/review_preprocessed.csv'
if os.path.isfile(main_csv_path):
    df = pd.read_csv(main_csv_path)
else:
    df = readfile(constants.FOOD_CSV_URL)
    df.to_csv(main_csv_path, encoding='utf-8-sig', index=False)
if os.path.isfile(review_csv_path):
    review_df = pd.read_csv(review_csv_path, encoding='utf-8-sig')
else:
    review_df = pd.read_csv(constants.REVIEW_CSV_URL, encoding='utf-8-sig')
    review_df.to_csv(review_csv_path, encoding='utf-8-sig', index=False)

# drop duplicates
df.drop_duplicates(subset='href', inplace=True)
df.reset_index(drop=True, inplace=True)
review_df.drop_duplicates(subset=['Review ID'], inplace=True)
review_df.reset_index(drop=True, inplace=True)

## Data Cleaning
# print all unique values in the 'Category' column
print(df['Category'].unique())

# remove all categories that are NOT in constants.INCLUDED_CATEGORIES_KEYWORDS
df = df[df['Category'].str.contains('|'.join(constants.INCLUDED_CATEGORIES_KEYWORDS), case=False)]
# Remove excluded categories
df = df[~df['Category'].str.contains('|'.join(constants.EXCLUDED_CATEGORIES), case=False)]

df.reset_index(drop=True, inplace=True)

# Process the 'Date' column to keep only the date part
review_df['Date'] = pd.to_datetime(review_df['Date']).dt.date

## Feature Engineering
# keywords_mapping = {
#     'Dine In': ['Dine-in'], 'Takeaway': ['Takeaway'], 'Delivery Service': ['Delivery'], 
#     'Accept Reservations': ['Accepts reservations'], 'Outdoor Seating': ['Outdoor seating'], 
#     'Wheelchair Accessibility': ['Wheelchair-accessible car park', 'Wheelchair-accessible entrance', 
#                                  'Wheelchair-accessible seating', 'Wheelchair-accessible toilet'], 
#     'Family Friendly': ['Family friendly'], 'Groups': ['Groups'], 'Good for Kids': ['Good for kids']
# }
# for column, keywords in keywords_mapping.items():
#     df[column] = df['About'].apply(lambda x: 'Yes' if any(keyword in x for keyword in keywords) else 'No')

# Create new column region
def find_region(row, places_dict):
    for region, areas in places_dict.items():
        for area in areas:
            if row['Planning Area'] in area:
                return region
    return None

df['Region'] = df.apply(find_region, axis=1, args=(constants.LIST_OF_PLACES,))

# add new columns to df based on the review_df metadata
# Safely convert the string representation of list of strings into a list of strings
def process_value(value, key):
    if "$" in value or key == "Price per person":
        value = value.replace("$", "").replace("RM ", "").replace("SGD ", "")
        if "+" in value:
            value = value.replace("+", "")
            return float(value)*1.5
        if "–" in value:
            parts = value.split("–")
            return sum(float(part) for part in parts) / len(parts)
        # if value is float
        if value.replace(".", "").isdigit():
            return float(value)
        else:
            return value
    if value.isdigit():
        return int(value)
    return value
def process_metadata(review_df): # convert metadata column into multiple columns
    for index, metadata_list in enumerate(review_df['Metadata']):
        for item in metadata_list:
            # if key has no value or no ": "
            if item == "" or ": " not in item:
                continue
            key, value = item.split(": ", 1)
            if key == "Service":
                # check if the string value can be converted to a int
                if value.isdigit():
                    int(value)
                    key = "Service Rating"
                else:
                    key = "Service Type"
            review_df.at[index, key] = process_value(value, key)
        if (index+1) % 10000 == 0:
            print(f"Processed {(index+1)} rows")
    # Drop the columns in which there is less than 20% of non-null values
    review_df.dropna(thresh=len(review_df) * 0.2, axis=1, inplace=True)
    # Drop the original 'Metadata' column
    review_df.drop(columns=['Metadata'], inplace=True)

    return review_df

# convert reivew_df metadata column into list
review_df['Metadata'] = review_df['Metadata'].apply(ast.literal_eval)
# # cut to 1000 rows for testing
# review_df = review_df.head(1000)
review_df = process_metadata(review_df)

# First, rename 'href of Place' in review_df to 'href' to match the column name in df
review_df.rename(columns={'href of Place': 'href'}, inplace=True)

# drop all columns except href, Service Rating, Food, Atmosphere, Price per person, Recommended dishes
review_df = review_df[['href', 'Service Rating', 'Food', 'Atmosphere', 'Price per person', 'Recommended dishes']]

# Now perform the aggregation on merged_df
aggregated_df = review_df.groupby('href').agg({
    'Service Rating': 'mean',
    'Food': 'mean',
    'Atmosphere': 'mean',
    'Price per person': 'mean',
    # convert to list
    'Recommended dishes': lambda x: ', '.join(x.dropna()).replace(' and ', ', ').split(', ')
}).reset_index()

# save to csv
aggregated_df.to_csv('main/review.csv', encoding='utf-8-sig', index=False)

# If you want to join this aggregated information back to the original df DataFrame:
df = pd.merge(df, aggregated_df, on='href', how='left')

# Assuming you want to rename some columns to match your original naming
df.rename(columns={
    'Food': 'Food Rating',
    'Price per person': 'Price Per Person',
    'Recommended dishes': 'Recommended Dishes'
}, inplace=True)





# process opening hours .replace(". Hide open hours for the week", "").strip()
df['Opening Hours'] = df['Opening Hours'].apply(lambda x: x.replace(". Hide open hours for the week", "").strip() if isinstance(x, str) else x)

# convert to str
df['Opening Hours'] = df['Opening Hours'].astype(str)

# convert str to dict and nan to empty dict
df['Opening Hours'] = df['Opening Hours'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else {})

# drop if open is Closed
for index, row in df.iterrows():
    for key, item in row['Opening Hours'].items():
            for x in item:
                if x['open'] == 'Closed':
                    df.at[index, 'Opening Hours'][key].remove(x)

def convert_to_24_hour(time_str, am_pm=None):
    if time_str == 'Closed':
        return time_str
    # if time_str does not have a am or pm
    if 'am' not in time_str and 'pm' not in time_str:
        time_str = time_str + ' ' + am_pm
    # format for parsing example: 12 pm or 11:30 am
    fmt = '%I %p'
    fmt2 = '%I:%M %p'
    try:
        time = datetime.strptime(time_str, fmt)
    except:
        time = datetime.strptime(time_str, fmt2)

    return time.strftime('%H:%M')

# create new column "First Opening Time"
df['First Opening Time'] = None
# Iterate through DataFrame rows
for index, row in df.iterrows():
    if not row['Opening Hours']:  # Check if 'Opening Hours' is empty
        df.at[index, 'First Opening Time'] = None
        continue
    
    first_opening_time = None
    for day, timings in row['Opening Hours'].items():
        if timings:  # Ensure there are timings for the day
            opening_time_str = timings[0]['open']  # Get opening time string
            closing_time_str = timings[0]['close']  # Get closing time string
            am_pm = None
            # get am or pm of close
            if 'am' in closing_time_str:
                am_pm = 'am'
            elif 'pm' in closing_time_str:
                am_pm = 'pm'
            opening_time_24hr = convert_to_24_hour(opening_time_str, am_pm)  # Convert to 24-hour format
            if opening_time_24hr and opening_time_24hr != 'Closed':  # Ensure conversion was successful
                # Update first_opening_time if it's either not set or later than the current opening time
                if first_opening_time is None or opening_time_24hr < first_opening_time:
                    first_opening_time = opening_time_24hr
    
    df.at[index, 'First Opening Time'] = first_opening_time

# create new column "Last Closing Time"
df['Last Closing Time'] = None
# Iterate through DataFrame rows
for index, row in df.iterrows():
    if not row['Opening Hours']:  # Check if 'Opening Hours' is empty
        df.at[index, 'Last Closing Time'] = None
        continue
    
    last_closing_time = None
    for day, timings in row['Opening Hours'].items():
        if timings:  # Ensure there are timings for the day
            closing_time_str = timings[0]['close']  # Get closing time string
            am_pm = None
            # get am or pm of open
            if 'am' in timings[0]['open']:
                am_pm = 'am'
            elif 'pm' in timings[0]['open']:
                am_pm = 'pm'
            closing_time_24hr = convert_to_24_hour(closing_time_str, am_pm)  # Convert to 24-hour format
            if closing_time_24hr and closing_time_24hr != 'Closed':  # Ensure conversion was successful
                # Update last_closing_time if it's either not set or earlier than the current closing time
                if last_closing_time is None or closing_time_24hr > last_closing_time:
                    last_closing_time = closing_time_24hr
    
    df.at[index, 'Last Closing Time'] = last_closing_time

# create new column "Average Opening Hours"
def calculate_hours(open_close_times):
    if open_close_times['open'] == 'Closed':
        return 0
    elif open_close_times['open'] == '12 am' and open_close_times['close'] == '12 am':
        return 24
    else:
        # if open close times does not have a am or pm
        if 'am' not in open_close_times['open'] and 'pm' not in open_close_times['open']:
            open_close_times['open'] = open_close_times['open'] + ' pm'
        # format for parsing example: 12 pm or 11:30 am
        fmt = '%I %p'
        fmt2 = '%I:%M %p'
        try:
            open_time = datetime.strptime(open_close_times['open'], fmt)
        except:
            open_time = datetime.strptime(open_close_times['open'], fmt2)
        try:
            close_time = datetime.strptime(open_close_times['close'], fmt)
        except:
            close_time = datetime.strptime(open_close_times['close'], fmt2)
        delta = close_time - open_time
        return delta.seconds / 3600  # Convert seconds to hours

df['Average Opening Hours'] = None
for index, row in df.iterrows():
    # if not empty dictionary
    if row['Opening Hours'] == {}:
        df.at[index, 'Average Opening Hours'] = None
        continue
    total_hours = 0
    # loop through dict row['Opening Hours']
    for key, item in row['Opening Hours'].items():
        for x in item:
            total_hours += calculate_hours(x)

    df.at[index, 'Average Opening Hours'] = total_hours / len(row['Opening Hours'])

## Analysis and Calculations
# Calculate bayesian rating based on the number of reviews and the average star rating
def calculate_bayesian_rating(N, R, C=5, m=3):
    return ((C * m) + (N * R)) / (C + N)

df['Bayesian Rating'] = df.apply(lambda x: calculate_bayesian_rating(x['Reviews'], x['Average Star Rating']), axis=1)

## Exporting Data
df.to_csv('main/main.csv', encoding='utf-8-sig', index=False)