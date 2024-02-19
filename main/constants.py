FEATURES_DATATYPES = {
    "href": "string",  # Link to the restaurant
    "Region": "string",  # Region of Singapore
    "Planning Area": "string",  # 1 of the 55 Planning Areas in Singapore
    "Subzone": "string",  # Subzone of planning area
    "Name": "string",  # Name of the restaurant
    "Search Engine Rating": "integer",  # Ranking in search results
    "Sponsored": "string",  # 'Yes' or 'No' for Google advertising
    "Opening Hours": "dictionary",  # Dictionary with days as keys and lists of open-close times as values
    "Popular Times": "dictionary",  # Nested dictionary with days as keys and times/crowd percentages as values
    "Average Star Rating": "float",  # Decimal number for average rating
    "Bayesian Rating": "float",  # Decimal number for Bayesian rating
    "Reviews": "integer",  # Total number of reviews
    "Category": "string",  # Type or category of the establishment
    "Price Rating": "string",  # Price range ('Moderate', 'Inexpensive', 'Very Expensive', or 'NAN')
    "Address": "string",  # Address of the restaurant
    "Metadata": "list",  # List of strings with additional information
    "longitude": "float",  # Decimal number for longitude
    "latitude": "float",  # Decimal number for latitude
    "Tags": "dictionary",  # Dictionary where keys are tags and values are integers
    "About": "list",  # List of features, services, or attributes
    "Service Rating": "float",  # Decimal number for service rating
    "Food Rating": "float",  # Decimal number for food rating
    "Atmosphere Rating": "float",  # Decimal number for atmosphere rating
    "Price Per Person": "float",  # Decimal number for price per person
    "Recommended Dishes": "list",  # String with recommended dishes
    "First Opening Time": "ISO8601",  # ISO8601 format for the first opening time
    "Last Opening Time": "ISO8601",  # ISO8601 format for the last opening time
    "Average Opening Time": "float",  # Decimal number for average opening time in hours
}

PLOT_FEATURES_DATATYPES = {
    "href": "string",  # Link to the restaurant
    "Region": "string",  # Region of Singapore
    "Planning Area": "string",  # 1 of the 55 Planning Areas in Singapore
    "Subzone": "string",  # Subzone of planning area
    "Name": "string",  # Name of the restaurant
    "Search Engine Rating": "integer",  # Ranking in search results
    "Sponsored": "string",  # 'Yes' or 'No' for Google advertising
    # "Opening Hours": "dictionary",  # Dictionary with days as keys and lists of open-close times as values
    # "Popular Times": "dictionary",  # Nested dictionary with days as keys and times/crowd percentages as values
    "Average Star Rating": "float",  # Decimal number for average rating
    "Bayesian Rating": "float",  # Decimal number for Bayesian rating
    "Reviews": "integer",  # Total number of reviews
    "Category": "string",  # Type or category of the establishment
    "Price Rating": "string",  # Price range ('Moderate', 'Inexpensive', 'Very Expensive', or 'NAN')
    "Address": "string",  # Address of the restaurant
    # "Metadata": "list",  # List of strings with additional information
    # "Tags": "dictionary",  # Dictionary where keys are tags and values are integers
    # "About": "list",  # List of features, services, or attributes
    "Service Rating": "float",  # Decimal number for service rating
    "Food Rating": "float",  # Decimal number for food rating
    "Atmosphere Rating": "float",  # Decimal number for atmosphere rating
    "Price Per Person": "float",  # Decimal number for price per person
    # "Recommended Dishes": "list",  # String with recommended dishes
    "First Opening Time": "ISO8601",  # ISO8601 format for the first opening time
    "Last Opening Time": "ISO8601",  # ISO8601 format for the last opening time
    "Average Opening Time": "float",  # Decimal number for average opening time in hours
}

LIST_OF_PLACES = {
    'Central Region': {'Bishan': ['Bishan East', 'Marymount', 'Upper Thomson'], 'Bukit Merah': ['Alexandra Hill', 'Alexandra North', 'Bukit Ho Swee', 'Bukit Merah', 'City Terminals', 'Depot Road', 'Everton Park', 'Henderson Hill', 'Kampong Tiong Bahru', 'Maritime Square', 'Redhill', 'Singapore General Hospital', 'Telok Blangah Drive', 'Telok Blangah Rise', 'Telok Blangah Way', 'Tiong Bahru', 'Tiong Bahru Station'], 'Bukit Timah': ['Anak Bukit', 'Coronation Road', 'Farrer Court', 'Hillcrest', 'Holland Road', 'Leedon Park', 'Swiss Club', 'Ulu Pandan'], 'Downtown Core': ['Anson', 'Bayfront Subzone', 'Bugis', 'Cecil', 'Central Subzone', 'City Hall', 'Clifford Pier', 'Marina Centre', 'Maxwell', 'Nicoll', 'Phillip', 'Raffles Place', 'Tanjong Pagar'], 'Geylang': ['Aljunied', 'Geylang East', 'Kallang Way', 'Kampong Ubi', 'MacPherson'], 'Kallang': ['Bendemeer', 'Boon Keng', 'Crawford', 'Geylang Bahru', 'Kallang Bahru', 'Kampong Bugis', 'Kampong Java', 'Lavender', 'Tanjong Rhu'], 'Marina East': ['Marina East'], 'Marina South': ['Marina South'], 'Marine Parade': ['East Coast', 'Katong', 'Marina East', 'Marine Parade', 'Mountbatten'], 'Museum': ['Bras Basah', 'Dhoby Ghaut', 'Fort Canning'], 'Newton': ['Cairnhill', 'Goodwood Park', 'Istana Negara', "Monk's Hill", 'Newton Circus', 'Orange Grove'], 'Novena': ['Balestier', 'Dunearn', 'Malcolm', 'Moulmein', 'Mount Pleasant'], 'Orchard': ['Boulevard', 'Somerset', 'Tanglin'], 'Outram': ['China Square', 'Chinatown', "Pearl's Hill", "People's Park"], 'Queenstown': ['Commonwealth', 'Dover', 'Ghim Moh', 'Holland Drive', 'Kent Ridge', 'Margaret Drive', 'Mei Chin', 'National University of Singapore', 'one-north', 'Pasir Panjang 1', 'Pasir Panjang 2', 'Port', 'Queensway', 'Singapore Polytechnic', 'Tanglin Halt'], 'River Valley': ['Institution Hill', 'Leonie Hill', 'One Tree Hill', 'Oxley', 'Paterson'], 'Rochor': ['Bencoolen', 'Farrer Park', 'Kampong Glam', 'Little India', 'Mackenzie', 'Mount Emily', 'Rochor Canal', 'Selegie', 'Sungei Road', 'Victoria'], 'Singapore River': ['Boat Quay', 'Clarke Quay', 'Robertson Quay'], 'Southern Islands': ['Sentosa', 'Southern Group'], 'Straits View': ['Straits View'], 'Tanglin': ['Chatsworth', 'Nassim', 'Ridout', 'Tyersall'], 'Toa Payoh': ['Bidadari', 'Boon Teck', 'Braddell', 'Joo Seng', 'Kim Keat', 'Lorong 8 Toa Payoh', 'Pei Chun', 'Potong Pasir', 'Sennett', 'Toa Payoh Central', 'Toa Payoh West', 'Woodleigh']},
    'East Region': {'Bedok': ['Bayshore', 'Bedok North', 'Bedok Reservoir', 'Bedok South', 'Frankel', 'Kaki Bukit', 'Kembangan', 'Siglap'], 'Changi': ['Changi Airport', 'Changi Point', 'Changi West'], 'Changi Bay': ['Changi Bay'], 'Pasir Ris': ['Flora Drive', 'Loyang East', 'Loyang West', 'Pasir Ris Central', 'Pasir Ris Drive', 'Pasir Ris Park', 'Pasir Ris Wafer Fab Park', 'Pasir Ris West'], 'Paya Lebar': ['Airport Road', 'Paya Lebar East', 'Paya Lebar North', 'Paya Lebar West', 'PLAB'], 'Tampines': ['Simei', 'Tampines East', 'Tampines North', 'Tampines West', 'Xilin']},
    'North Region': {'Central Water Catchment': ['Central Water Catchment'], 'Lim Chu Kang': ['Lim Chu Kang'], 'Mandai': ['Mandai East', 'Mandai Estate', 'Mandai West'], 'Sembawang': ['Admiralty', 'Sembawang Central', 'Sembawang East', 'Sembawang North', 'Sembawang Springs', 'Sembawang Straits', 'Senoko North', 'Senoko South', 'The Wharves'], 'Simpang': ['Pulau Seletar', 'Simpang North', 'Simpang South', 'Tanjong Irau'], 'Sungei Kadut': ['Gali Batu', 'Kranji', 'Pang Sua', 'Reservoir View', 'Turf Club'], 'Woodlands': ['Greenwood Park', 'Midview', 'North Coast', 'Senoko West', 'Woodgrove', 'Woodlands East', 'Woodlands Regional Centre', 'Woodlands South', 'Woodlands West'], 'Yishun': ['Khatib', 'Lower Seletar', 'Nee Soon', 'Northland', 'Springleaf', 'Yishun Central', 'Yishun East', 'Yishun South', 'Yishun West']},
    'North-East Region': {'Ang Mo Kio': ['Ang Mo Kio Town Centre', 'Cheng San', 'Chong Boon', 'Kebun Bahru', 'Sembawang Hills', 'Shangri-La', 'Tagore', 'Townsville', 'Yio Chu Kang', 'Yio Chu Kang East', 'Yio Chu Kang North', 'Yio Chu Kang West'], 'Hougang': ['Defu Industrial Park', 'Hougang Central', 'Hougang East', 'Hougang West', 'Kangkar', 'Kovan', 'Lorong Ah Soo', 'Lorong Halus', 'Tai Seng', 'Trafalgar'], 'North-Eastern Islands': ['North-Eastern Islands'], 'Punggol': ['Coney Island', 'Matilda', 'Northshore', 'Punggol Canal', 'Punggol Field', 'Punggol Town Centre', 'Waterway East'], 'Seletar': ['Pulau Punggol Barat', 'Pulau Punggol Timor', 'Seletar', 'Seletar Aerospace Park'], 'Sengkang': ['Anchorvale', 'Compassvale', 'Fernvale', 'Lorong Halus North', 'Rivervale', 'Sengkang Town Centre', 'Sengkang West'], 'Serangoon': ['Lorong Chuan', 'Seletar Hills', 'Serangoon Central', 'Serangoon Garden', 'Serangoon North', 'Serangoon North Industrial Estate', 'Upper Paya Lebar']},
    'West Region': {'Boon Lay': ['Liu Fang', 'Samulun', 'Shipyard', 'Tukang'], 'Bukit Batok': ['Brickworks', 'Bukit Batok Central', 'Bukit Batok East', 'Bukit Batok West', 'Bukit Batok South', 'Gombak', 'Guilin', 'Hillview', 'Hong Kah North'], 'Bukit Panjang': ['Bangkit', 'Dairy Farm', 'Fajar', 'Jelebu', 'Nature Reserve', 'Saujana', 'Senja'], 'Choa Chu Kang': ['Choa Chu Kang Central', 'Choa Chu Kang North', 'Keat Hong', 'Peng Siang', 'Teck Whye', 'Yew Tee'], 'Clementi': ['Clementi Central', 'Clementi North', 'Clementi West', 'Clementi Woods', 'Faber', 'Pandan', 'Sunset Way', 'Toh Tuck', 'West Coast'], 'Jurong East': ['International Business Park', 'Jurong Gateway', 'Jurong Port', 'Jurong River', 'Lakeside (Business)', 'Lakeside (Leisure)', 'Penjuru Crescent', 'Teban Gardens', 'Toh Guan', 'Yuhua East', 'Yuhua West'], 'Jurong West': ['Boon Lay Place', 'Chin Bee', 'Hong Kah', 'Jurong West Central', 'Kian Teck', 'Safti', 'Taman Jurong', 'Wenya', 'Yunnan'], 'Pioneer': ['Benoi Sector', 'Gul Basin', 'Gul Circle', 'Joo Koon', 'Pioneer Sector'], 'Tengah': ['Brickland', 'Forest Hill', 'Garden', 'Park', 'Plantation', 'Tengah Industrial Estate'], 'Tuas': ['Tengeh', 'Tuas Bay', 'Tuas North', 'Tuas Promenade', 'Tuas View', 'Tuas View Extension'], 'Western Islands': ['Jurong Island and Bukom', 'Semakau', 'Sudong'], 'Western Water Catchment': ['Bahar', 'Cleantech', 'Murai']},
    }

PLOT_TYPES = ['pie chart', 'bar chart', 'distribution', 'hexbin', 'linear regression', 'scatter', 'line chart']

OPERATORS = ['==', '>', '<', '>=', '<=', '!=', 'smallest', 'largest', 'in', 'not in']


DEFAULT_PLOT_JSON = """{
  "feature1": "First Opening Time",
  "feature2": "Average Star Rating",
  "plot": "line chart"
}"""

FOOD_CSV_URL = "https://huggingface.co/datasets/AlexanderLJX/Dining-Insights/resolve/main/scraped_data_food_full.csv?download=true"
REVIEW_CSV_URL = "https://huggingface.co/datasets/AlexanderLJX/Dining-Insights/resolve/main/scraped_data_reviews_food_full.csv?download=true"

INCLUDED_CATEGORIES_KEYWORDS = ['restaurant', 'cafe', 'bar', 'takeaway', 'food court', 'bakery', 'pub', 'beer', 'patisserie', 'creperie', 'diner', 'bistro', 'live music venue', 'hawker', 'grill', 'kiosk', 'stand', 'BBQ', 'brewery', 'delicatessen', 'deli', 'chinese tea house', 'crab house', 'french steakhouse restaurant', 'japanese steakhouse', 'steak house', 'tea house', 'açaí shop', 'bagel shop', 'cake shop', 'coffee shop', 'dessert shop', 'ice cream shop', 'juice shop', 'kebab shop', 'noodle shop', 'pasta shop', 'pastry shop', 'salad shop', 'sandwich shop', 'soba noodle shop', 'soft drinks shop', 'soup shop', 'steamed bun shop', 'tea and coffee shop', 'bubble tea store', 'coffee store', 'grill store', 'health food store', 'tea store', 'wine store']

EXCLUDED_CATEGORIES = ['Academic department', 'Add a photo', 'Add hours', "Add place's phone number", 'Apartment building', 'Apartment complex', 'Athletic field', 'BBQ area', 'Beverage distributor', 'Boat tour agency', 'Box lunch supplier', 'Bridge', 'Building firm', 'Bus stop', 'Business center', 'Butcher shop', 'Caterer', 'Catering food and drink supplier', 'Chicken shop', 'Circus', 'Club', 'Commercial agent', 'Commercial real estate agency', 'Community center', 'Computer repair service', 'Condominium complex', 'Convenience store', 'Corporate campus', 'Corporate office', 'Country club', 'Dog park', 'Environment office', 'Event venue', 'Family service center', 'Festival', 'Food', 'Food and beverage consultant', 'Food and drink', 'Food manufacturer', 'Food manufacturing supply', 'Food processing company', 'Food producer', 'Food products supplier', 'Fresh food market', 'Frozen food manufacturer', 'Fruit and vegetable store', 'Furniture store', 'Garden', 'Gourmet grocery store', 'Grocery store', 'HDB Flats', 'Hiking area', 'Hotel', 'Housing complex', 'Housing development', 'Housing society', 'Hypermarket', 'Importer', 'Industrial Real Estate Agency', 'International school', 'Island', 'Italian grocery store', 'Japanese grocery store', 'MRT/LRT Station', 'Manufacturer', 'Market', 'Meat products store', 'Media company', 'Nature preserve', 'Oil refinery', 'Park', 'Parking lot', 'Permanently closed', 'Personal chef service', 'Petrol Station', 'Prawn Fishing', 'Primary school', 'Promenade', 'Railway services', 'Rainwater tank supplier', 'Real estate agency', 'Real estate developer', 'Rice shop', 'Seafood market', 'Seafood wholesaler', 'Shared-use commercial kitchen', 'Shop', 'Shopping mall', 'Skateboard park', 'Soup kitchen', 'Sports club', 'Supermarket', 'Tiffin center', 'Tour operator', 'Tourist attraction', 'Townhouse complex', 'Transportation service', 'Vegetable wholesale market', 'Vending machine supplier', 'Visitor center', 'Warehouse', 'Waste management service', 'Wholesaler']