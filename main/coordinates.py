
 ############# imported modules ###############

from geopy.geocoders import Nominatim      
import pandas as pd
import json

############### reading data  from csv file##################### 
data = pd.read_csv(r'scraped_data_food.csv') #!!!!!!!!!!! remember to change the file location if you are runnign this code if needed!!!!!!!!!!!!!!!!!!!!!!!!!!

string = data['Metadata'].to_string()
metadata_list=json.loads(string)
address_list=[]









geolocator = Nominatim(user_agent = 'coordinates')
location = geolocator.geocode()
print((location.latitude, location.longitude))

