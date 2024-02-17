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


LIST_OF_PLACES = {
    'Central Region': {'Bishan': ['Bishan East', 'Marymount', 'Upper Thomson'], 'Bukit Merah': ['Alexandra Hill', 'Alexandra North', 'Bukit Ho Swee', 'Bukit Merah', 'City Terminals', 'Depot Road', 'Everton Park', 'Henderson Hill', 'Kampong Tiong Bahru', 'Maritime Square', 'Redhill', 'Singapore General Hospital', 'Telok Blangah Drive', 'Telok Blangah Rise', 'Telok Blangah Way', 'Tiong Bahru', 'Tiong Bahru Station'], 'Bukit Timah': ['Anak Bukit', 'Coronation Road', 'Farrer Court', 'Hillcrest', 'Holland Road', 'Leedon Park', 'Swiss Club', 'Ulu Pandan'], 'Downtown Core': ['Anson', 'Bayfront Subzone', 'Bugis', 'Cecil', 'Central Subzone', 'City Hall', 'Clifford Pier', 'Marina Centre', 'Maxwell', 'Nicoll', 'Phillip', 'Raffles Place', 'Tanjong Pagar'], 'Geylang': ['Aljunied', 'Geylang East', 'Kallang Way', 'Kampong Ubi', 'MacPherson'], 'Kallang': ['Bendemeer', 'Boon Keng', 'Crawford', 'Geylang Bahru', 'Kallang Bahru', 'Kampong Bugis', 'Kampong Java', 'Lavender', 'Tanjong Rhu'], 'Marina East': ['Marina East'], 'Marina South': ['Marina South'], 'Marine Parade': ['East Coast', 'Katong', 'Marina East', 'Marine Parade', 'Mountbatten'], 'Museum': ['Bras Basah', 'Dhoby Ghaut', 'Fort Canning'], 'Newton': ['Cairnhill', 'Goodwood Park', 'Istana Negara', "Monk's Hill", 'Newton Circus', 'Orange Grove'], 'Novena': ['Balestier', 'Dunearn', 'Malcolm', 'Moulmein', 'Mount Pleasant'], 'Orchard': ['Boulevard', 'Somerset', 'Tanglin'], 'Outram': ['China Square', 'Chinatown', "Pearl's Hill", "People's Park"], 'Queenstown': ['Commonwealth', 'Dover', 'Ghim Moh', 'Holland Drive', 'Kent Ridge', 'Margaret Drive', 'Mei Chin', 'National University of Singapore', 'one-north', 'Pasir Panjang 1', 'Pasir Panjang 2', 'Port', 'Queensway', 'Singapore Polytechnic', 'Tanglin Halt'], 'River Valley': ['Institution Hill', 'Leonie Hill', 'One Tree Hill', 'Oxley', 'Paterson'], 'Rochor': ['Bencoolen', 'Farrer Park', 'Kampong Glam', 'Little India', 'Mackenzie', 'Mount Emily', 'Rochor Canal', 'Selegie', 'Sungei Road', 'Victoria'], 'Singapore River': ['Boat Quay', 'Clarke Quay', 'Robertson Quay'], 'Southern Islands': ['Sentosa', 'Southern Group'], 'Straits View': ['Straits View'], 'Tanglin': ['Chatsworth', 'Nassim', 'Ridout', 'Tyersall'], 'Toa Payoh': ['Bidadari', 'Boon Teck', 'Braddell', 'Joo Seng', 'Kim Keat', 'Lorong 8 Toa Payoh', 'Pei Chun', 'Potong Pasir', 'Sennett', 'Toa Payoh Central', 'Toa Payoh West', 'Woodleigh']},
    'East Region': {'Bedok': ['Bayshore', 'Bedok North', 'Bedok Reservoir', 'Bedok South', 'Frankel', 'Kaki Bukit', 'Kembangan', 'Siglap'], 'Changi': ['Changi Airport', 'Changi Point', 'Changi West'], 'Changi Bay': ['Changi Bay'], 'Pasir Ris': ['Flora Drive', 'Loyang East', 'Loyang West', 'Pasir Ris Central', 'Pasir Ris Drive', 'Pasir Ris Park', 'Pasir Ris Wafer Fab Park', 'Pasir Ris West'], 'Paya Lebar': ['Airport Road', 'Paya Lebar East', 'Paya Lebar North', 'Paya Lebar West', 'PLAB'], 'Tampines': ['Simei', 'Tampines East', 'Tampines North', 'Tampines West', 'Xilin']},
    'North Region': {'Central Water Catchment': ['Central Water Catchment'], 'Lim Chu Kang': ['Lim Chu Kang'], 'Mandai': ['Mandai East', 'Mandai Estate', 'Mandai West'], 'Sembawang': ['Admiralty', 'Sembawang Central', 'Sembawang East', 'Sembawang North', 'Sembawang Springs', 'Sembawang Straits', 'Senoko North', 'Senoko South', 'The Wharves'], 'Simpang': ['Pulau Seletar', 'Simpang North', 'Simpang South', 'Tanjong Irau'], 'Sungei Kadut': ['Gali Batu', 'Kranji', 'Pang Sua', 'Reservoir View', 'Turf Club'], 'Woodlands': ['Greenwood Park', 'Midview', 'North Coast', 'Senoko West', 'Woodgrove', 'Woodlands East', 'Woodlands Regional Centre', 'Woodlands South', 'Woodlands West'], 'Yishun': ['Khatib', 'Lower Seletar', 'Nee Soon', 'Northland', 'Springleaf', 'Yishun Central', 'Yishun East', 'Yishun South', 'Yishun West']},
    'North-East Region': {'Ang Mo Kio': ['Ang Mo Kio Town Centre', 'Cheng San', 'Chong Boon', 'Kebun Bahru', 'Sembawang Hills', 'Shangri-La', 'Tagore', 'Townsville', 'Yio Chu Kang', 'Yio Chu Kang East', 'Yio Chu Kang North', 'Yio Chu Kang West'], 'Hougang': ['Defu Industrial Park', 'Hougang Central', 'Hougang East', 'Hougang West', 'Kangkar', 'Kovan', 'Lorong Ah Soo', 'Lorong Halus', 'Tai Seng', 'Trafalgar'], 'North-Eastern Islands': ['North-Eastern Islands'], 'Punggol': ['Coney Island', 'Matilda', 'Northshore', 'Punggol Canal', 'Punggol Field', 'Punggol Town Centre', 'Waterway East'], 'Seletar': ['Pulau Punggol Barat', 'Pulau Punggol Timor', 'Seletar', 'Seletar Aerospace Park'], 'Sengkang': ['Anchorvale', 'Compassvale', 'Fernvale', 'Lorong Halus North', 'Rivervale', 'Sengkang Town Centre', 'Sengkang West'], 'Serangoon': ['Lorong Chuan', 'Seletar Hills', 'Serangoon Central', 'Serangoon Garden', 'Serangoon North', 'Serangoon North Industrial Estate', 'Upper Paya Lebar']},
    'West Region': {'Boon Lay': ['Liu Fang', 'Samulun', 'Shipyard', 'Tukang'], 'Bukit Batok': ['Brickworks', 'Bukit Batok Central', 'Bukit Batok East', 'Bukit Batok West', 'Bukit Batok South', 'Gombak', 'Guilin', 'Hillview', 'Hong Kah North'], 'Bukit Panjang': ['Bangkit', 'Dairy Farm', 'Fajar', 'Jelebu', 'Nature Reserve', 'Saujana', 'Senja'], 'Choa Chu Kang': ['Choa Chu Kang Central', 'Choa Chu Kang North', 'Keat Hong', 'Peng Siang', 'Teck Whye', 'Yew Tee'], 'Clementi': ['Clementi Central', 'Clementi North', 'Clementi West', 'Clementi Woods', 'Faber', 'Pandan', 'Sunset Way', 'Toh Tuck', 'West Coast'], 'Jurong East': ['International Business Park', 'Jurong Gateway', 'Jurong Port', 'Jurong River', 'Lakeside (Business)', 'Lakeside (Leisure)', 'Penjuru Crescent', 'Teban Gardens', 'Toh Guan', 'Yuhua East', 'Yuhua West'], 'Jurong West': ['Boon Lay Place', 'Chin Bee', 'Hong Kah', 'Jurong West Central', 'Kian Teck', 'Safti', 'Taman Jurong', 'Wenya', 'Yunnan'], 'Pioneer': ['Benoi Sector', 'Gul Basin', 'Gul Circle', 'Joo Koon', 'Pioneer Sector'], 'Tengah': ['Brickland', 'Forest Hill', 'Garden', 'Park', 'Plantation', 'Tengah Industrial Estate'], 'Tuas': ['Tengeh', 'Tuas Bay', 'Tuas North', 'Tuas Promenade', 'Tuas View', 'Tuas View Extension'], 'Western Islands': ['Jurong Island and Bukom', 'Semakau', 'Sudong'], 'Western Water Catchment': ['Bahar', 'Cleantech', 'Murai']},
    }

def find_region(row, places_dict):
    for region, areas in places_dict.items():
        for area, sub_areas in areas.items():
            if row['Planning Area'] in area:
                return region
    return None

# add a new column "Region" to the dataframe from based on the "Planning Area" column
df['Region'] = df.apply(find_region, axis=1, args=(LIST_OF_PLACES,))


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

# Temporary test for time animation
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


# Update the CSV File
df.to_csv('main.csv', encoding='utf-8-sig', index=False)