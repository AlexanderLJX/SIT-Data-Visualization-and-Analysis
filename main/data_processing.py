import pandas as pd
import ast  # To safely evaluate strings containing Python expressions from a string-based input

# download csv from hugging face
food_csv_url = "https://huggingface.co/datasets/AlexanderLJX/Dining-Insights/resolve/main/scraped_data_food_full.csv?download=true"
reviews_csv_url = "https://huggingface.co/datasets/AlexanderLJX/Dining-Insights/resolve/main/scraped_data_reviews_food_full.csv?download=true"
# Read the original main food CSV file
df = pd.read_csv(food_csv_url)
original_rows = len(df)
print("Number of rows in the original CSV file: %d" % len(df))

# Remove duplicate rows with the same 'href', and adjust the index accordingly
df.drop_duplicates(subset='href', inplace=True)
# Reset the index
df.reset_index(drop=True, inplace=True)

print("Number of rows after removing duplicates: %d" % len(df))
print("Number of rows removed: %d" % (original_rows - len(df)))

# Cleaning of dataset by categories
# Get list of unique categories, there should be no duplicates
original_category_list = df['Category'].tolist()
original_category_list.sort()

# print length of original category list
print("Length of Original Category List: "+ str(len(original_category_list)))


non_dine_in_categories = ["restaurant", "cafe", "bar", "takeaway", "food court", "bakery", "pub", "beer", "patisserie", 
                      "creperie", "diner", "bistro", "live music venue", "hawker", "grill", "kiosk", "stand", "BBQ","brewery",
                      "delicatessen", "deli"]

excluded_category_with_word_shop = ["shopping mall", "gift shop", "butcher shop", "chicken shop", "rice shop"]

excluded_category_with_word_store = ["convenience store", "fruit and vegetable store", "furniture store", "gourmet grocery store", "grocery store", "meat products store" ]

blacklisted_keywords = ["townhouse complex", "warehouse"]

excluded_categories = non_dine_in_categories + excluded_category_with_word_shop + excluded_category_with_word_store

# Remove excluded categories frome df
df = df[~df['Category'].isin(excluded_categories)]

# Remove all rows if any element contains any element of blacklisted_keywords
df = df[~df['Name'].str.contains('|'.join(blacklisted_keywords), case=False)]


df.reset_index(drop=True, inplace=True)


import constants

def find_region(row, places_dict):
    for region, areas in places_dict.items():
        for area, sub_areas in areas.items():
            if row['Planning Area'] in area:
                return region
    return None

# add a new column "Region" to the dataframe from based on the "Planning Area" column
df['Region'] = df.apply(find_region, axis=1, args=(constants.LIST_OF_PLACES,))


# Extracting useful information from About Column
# Assuming df is your DataFrame and it already exists

# Safely convert the string representation of list of strings into a list of strings
df['About'] = df['About'].apply(ast.literal_eval)
# print(df["About"])

# New Columns for Classifying Dining Options
df['Dine In'] = None
df['Takeaway'] = None
df['Delivery Service'] = None
df['Accept Reservations'] = None
df['Outdoor Seating'] = None

# New columns for Classifying Accessibility Options
df['Wheelchair Accessibility'] = None

# New columns for Classifying Customer Groups
df['Family Friendly'] = None
df['Groups'] = None
df['Good for Kids'] = None

# Define keywords for each column
keywords_mapping = {
    'Dine In': ['Dine-in'],
    'Takeaway': ['Takeaway'],
    'Delivery Service': ['Delivery'],
    'Accept Reservations': ['Accepts reservations'],
    'Outdoor Seating': ['Outdoor seating'],
    'Wheelchair Accessibility': ['Wheelchair-accessible car park', 'Wheelchair-accessible entrance', 'Wheelchair-accessible seating', 'Wheelchair-accessible toilet'],
    'Family Friendly': ['Family friendly'],
    'Groups': ['Groups'],
    'Good for Kids': ['Good for kids']
}

# Iterate over each column and set values based on keywords
for column, keywords in keywords_mapping.items():
    df[column] = df['About'].apply(lambda x: 'Yes' if any(keyword in x for keyword in keywords) else 'No')

# Temporary test column for time animation
# apply ast to convert string to dictionary
df['Opening Hours'] = df['Opening Hours'].apply(ast.literal_eval)
df['First Opening Time'] = None
# add a first opening time column
for index, row in df.iterrows():
    # if not empty dictionary
    try:
        # get the first opening time of friday
        first_opening_time = row['Opening Hours']['Friday'][0]['open']
        df.at[index, 'First Opening Time'] = first_opening_time
    except:
        first_opening_time = None
        df.at[index, 'First Opening Time'] = first_opening_time
# make time ISO string format if not None
df['First Opening Time'] = pd.to_datetime(df['First Opening Time'], errors='coerce').dt.strftime('%H:%M')

# convert to int
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
# convert to float, if not possible, convert to NaN
df['Average Star Rating'] = pd.to_numeric(df['Average Star Rating'], errors='coerce')
# Step 1: Calculate the overall average rating (m) and the average number of reviews (C)
m = df['Average Star Rating'].mean()
C = df['Reviews'].mean()

# Step 2: Define a function to calculate the Bayesian Rating
def calculate_bayesian_rating(N, R, C=C, m=m):
    return ((C * m) + (N * R)) / (C + N)

# Step 3: Apply the Bayesian Rating formula to each restaurant
df['Bayesian Rating'] = df.apply(lambda x: calculate_bayesian_rating(x['Reviews'], x['Average Star Rating']), axis=1)

# Now your DataFrame has a new column 'Bayesian Rating' with the calculated ratings for each restaurant.

# convert Price Rating to dollar sign
df['Price Rating'] = df['Price Rating'].replace(' Moderate', '$$')
df['Price Rating'] = df['Price Rating'].replace(' Inexpensive', '$')
df['Price Rating'] = df['Price Rating'].replace(' Very Expensive', '$$$$')
df['Price Rating'] = df['Price Rating'].replace(' Expensive', '$$$')
df['Price Rating'] = df['Price Rating'].replace('NAN', '')

# Update the CSV File
df.to_csv('main/main.csv', encoding='utf-8-sig', index=False)