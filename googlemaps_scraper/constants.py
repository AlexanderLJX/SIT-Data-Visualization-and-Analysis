# list of planning areas in Singapore from https://en.wikipedia.org/wiki/Planning_Areas_of_Singapore
LIST_OF_PLANNING_AREAS = [
    "Ang Mo Kio",
    "Bedok",
    "Bishan",
    "Bukit Batok",
    "Bukit Merah",
    # "Bukit Panjang",
    # "Bukit Timah",
    # "Central Water Catchment",
    # "Changi",
    # "Choa Chu Kang",
    # "Clementi",
    # "Downtown Core",
    # "Geylang",
    # "Hougang",
    # "Jurong East",
    # "Jurong West",
    # "Kallang",
    # "Lim Chu Kang",
    # "Mandai",
    # "Marina East",
    # "Marina South",
    # "Marine Parade",
    # "Museum",
    # "Newton",
    # "Novena",
    # "Outram",
    # "Pasir Ris",
    # "Paya Lebar",
    # "Pioneer",
    # "Punggol",
    # "Queenstown",
    # "River Valley",
    # "Rochor",
    # "Seletar",
    # "Sembawang",
    # "Sengkang",
    # "Serangoon",
    # "Simpang",
    # "Singapore River",
    # "Southern Islands",
    # "Sungei Kadut",
    # "Tampines",
    # "Tanglin",
    # "Tengah",
    # "Toa Payoh",
    # "Tuas",
    # "Western Islands",
    # "Western Water Catchment",
    # "Woodlands",
    # "Yishun"
]

# google's main URL
# URL = "https://www.google.com/maps/search/japanese+restaurants/@1.3143869,103.78828,17z"

URL = "https://www.google.com/maps/search/"

TARGET = "food"

MAX_REVIEWS_PER_PLACE = 5

RUN_MULTITHREADED = True

RUN_HEADLESS = True

NUM_THREADS = 6

NOT_FOOD_FLAGS = ["island", "temple", "park", "nature preserve"]



SUB_AREAS = ["Marymount", "Upper Thomson",
 "Alexandra Hill", "Alexandra North", "Bukit Ho Swee", "Bukit Merah", "Depot Road", "Everton Park",
 "HarbourFront/Maritime Square", "Henderson Hill", "Kampong Tiong Bahru", "Redhill", "Singapore General Hospital",
 "Telok Blangah Drive", "Telok Blangah Rise", "Telok Blangah Way", "Tiong Bahru",
 "Anak Bukit", "Coronation Road", "Farrer Court", "Hillcrest", "Holland Road", "Leedon Park", "Swiss Club", "Ulu Pandan",
 "Anson", "Bayfront Subzone", "Bugis", "Cecil", "Central Subzone", "City Hall", "Clifford Pier", "Marina Centre", 
 "Maxwell", "Millenia Singapore", "Nicoll", "Phillip", "Raffles Place", "Tanjong Pagar",
 "Aljunied", "Geylang East", "Kallang Way", "Kampong Ubi", "MacPherson", "Kallang Bendemeer", "Boon Keng", 
 "Crawford", "Geylang Bahru", "Kallang Bahru", "Kampong Bugis", "Kampong Java", "Lavender", "Tanjong Rhu",
 "Marina East", "Marina South",
 "East Coast", "Katong", "Marina East", "Marine Parade",
 "Mountbatten", "Museum Bras Basah", "Dhoby Ghaut", "Fort Canning", "Newton", "Cairnhill", "Goodwood Park", 
 "Istana Negara", "Monk's Hill", "Newton Circus", "Orange Grove", "Novena", "Balestier", "Dunearn", "Malcolm", 
 "Moulmein", "Mount Pleasant", "Orchard Boulevard", "Somerset", "Tanglin",
 "China Square", "Chinatown", "Pearl's Hill", "People's Park",
 "Commonwealth", "Dover", "Ghim Moh", "Kent Ridge", "Margaret Drive", "Mei Chin", "National University of Singapore", 
 "one-north", "Pasir Panjang 1", "Pasir Panjang 2", "Tanglin Halt", 
 "Queensway", "River Valley", "Institution Hill", "Leonie Hill", "One Tree Hill", "Oxley", "Paterson",
 "Bencoolen", "Farrer Park", "Kampong Glam", "Little India", "Mackenzie", "Mount Emily", "Rochor Canal", 
 "Selegie", "Sungei Road", "Victoria",
 "Boat Quay", "Clarke Quay", "Robertson Quay",
 "Kusu Island", "Lazarus Island", "Sentosa", "Sisters' Islands", "Saint John's Island", "Straits View",
 "Chatsworth", "Nassim", "Ridout", "Tyersall",
 "Bidadari", "Boon Teck", "Braddell", "Joo Seng", "Kim Keat", "Lorong 8 Toa Payoh", "Pei Chun", "Potong Pasir", 
 "Sennett", "Toa Payoh Central", "Toa Payoh West", "Woodleigh",
 "Bayshore", "Bedok North", "Reservoir", "Bedok South", "Frankel", "Kaki Bukit", "Kembangan", "Siglap", 
 "Changi Airport", "Changi Point", "Changi West", "Changi Bay",
 "Flora Drive", "Loyang East", "Loyang West", "Pasir Ris Central", "Pasir Ris Drive", "Pasir Ris Park", 
 "Pasir Ris Wafer Fab Park", "Pasir Ris West", "Paya Lebar Airport Road, Singapore", "Paya Lebar East",
 "Paya Lebar North", "Paya Lebar West", "Plab", "Simei", "Tampines East", "Tampines North", "Tampines West", "Xilin",
 "Lim Chu Kang", "Mandai East", "Mandai Estate", "Mandai West",
 "Admiralty", "Sembawang Central", "Sembawang East", "Sembawang North", "Sembawang Spring", "Sembawang Straits",
 "Senoko North", "Senoko South", "The Wharves", "Simpang Pulau", "Seletar", "Pulau Punggol Barat", "Pulau Punggol Timor",
 "Aerospace Park", "Sengkang Anchorvale", "Compassvale", "Fernvale", "Jalan Kayu", "Lorong Halus North", 
 "Rivervale", "Sengkang Town Centre", "Sengkang West", "Lorong Chuan", "Seletar Hills", "Serangoon Central", 
 "Serangoon Garden", "Serangoon North", "Serangoon North Industrial Estate", "Upper Paya Lebar",
 "Liu Fang", "Samulun", "Shipyard", "Tukang",
 "Bukit Batok Central", "Bukit Batok East", "Bukit Batok South", "Bukit Batok West", "Brickworks", "Bukit Gombak",
 "Guilin", "Hillview", "Hong Kah North",
 "Bangkit", "Dairy Farm", "Fajar", "Jelebu", "Nature Reserve", "Saujana", "Senja",
 "Choa Chu Kang Central", "Choa Chu Kang North", "Keat Hong", "Peng Siang", "Teck Whye", "Yew Tee",
 "Clementi Central", "Clementi North", "Clementi West", "Clementi Woods", "Faber", "Pandan", "Sunset Way", "Toh Tuck",
 "West Coast",
 "International Business Park", "Jurong Gateway", "Jurong Port", "Lakeside", "Jurong River", "Penjuru Crescent",
 "Teban Gardens", "Toh Guan", "Yuhua", "Boon Lay Place", "Chin Bee", "Hong Kah", "Kian Teck", "Safti",
 "Taman Jurong", "Wenya", "Yunnan", "Benoi Sector", "Gul Basin", "Gul Circle", "Joo Koon", "Pioneer Sector", 
 "Tengah", "Tuas Tengeh", "Tuas Bay", "Tuas North", "Tuas Promenade", "Tuas View", "Tuas View Extension",
 "Jurong Island", "Bukum", "Semakau", "Sudong",
 "Ang Mo Kio Town Centre", "Cheng San", "Chong Boon", "Kebun Baru", "Sembawang Hills", "Shangri-la", "Tagore",
 "Townsville, Singapore", "Yio Chu Kang", "Yio Chu Kang East", "Yio Chu Kang North", "Yio Chu Kang West",
 "Defu Industrial Park", "Hougang Central", "Hougang East", "Hougang West", "Kangkar", "Kovan", "Lorong Ah Soo",
 "Lorong Halus", "Tai Seng", "Trafalgar", "North-Eastern Islands", "Punggol Coney Island", "Matilda", "Northshore",
 "Punggol Canal", "Punggol Field", "Punggol Town Centre", "Waterway East", "Pulau Punggol Barat", "Pulau Punggol Timor",
 "Seletar", "Anchorvale", "Compassvale", "Fernvale", "Jalan Kayu", "Lorong Halus North", "Rivervale", 
 "Sengkang Town Centre", "Sengkang West", "Serangoon"]
