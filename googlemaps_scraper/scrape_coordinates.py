import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue

# CSV file path
CSV_FILE_PATH = 'scraped_data_food.csv'

NEW_CSV_FILE_PATH = 'scraped_data_food_coordinates.csv'

NUM_OF_THREADS = 10

from csv import writer

counter = 0

# make a csv writer object
csv_writer = writer(open(NEW_CSV_FILE_PATH, 'w', encoding="utf-8", newline=''))

# write header
csv_writer.writerow(['href', 'latitude', 'longitude'])

# import threading lock
from threading import Lock

# create lock
lock = Lock()

# Disable JavaScript in Chrome options
chrome_options = Options()
prefs = {'profile.default_content_setting_values': {'images':2}}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_experimental_option("detach", True)
# headless mode
# chrome_options.add_argument("--headless=new")

# Function to scrape data for a single row
def scrape_data(queue):
    global counter
    driver = webdriver.Chrome(options=chrome_options)
    start_time = time.time()
    while not queue.empty():
        if time.time() - start_time > 60:
            break # can't find another way to clear the memeory in the browser
        url = queue.get()
        driver.get(url)
        # Implement the scraping logic here, e.g., extract coordinates
        while True:
            try:
                current_url = driver.current_url
                lat, lng = current_url.split('/@')[1].split(',')[0], current_url.split('/@')[1].split(',')[1]
                # print(lat, lng)
                
                lat = float(lat)
                lng = float(lng)
                # if lat or lng is more than 10 digits, it is not a valid coordinate
                if len(str(lat)) > 15 or len(str(lng)) > 15:
                    raise Exception('Invalid coordinates')
                # df.loc[index, 'coordinates'] = f"{lat}, {lng}"
                with lock:
                    csv_writer.writerow([url, lat, lng])
                    counter += 1
                    print(f"Processed {counter} of {len(df)} addresses. Latitude: {lat}, Longitude: {lng}")
                break
            except Exception as exception:
                if str(exception) != 'list index out of range':
                    print(exception)
                pass
        # Remember to close the driver after each task is completed
    driver.quit()

# Read the CSV file
df = pd.read_csv(CSV_FILE_PATH)

# List to hold futures
futures = []

queue = Queue()
for index, row in df.iterrows():
    # if row doesn't have values in latitude and longitude
    if pd.isna(row['latitude']) or pd.isna(row['longitude']):
        queue.put(row['href'])

# Use ThreadPoolExecutor to execute tasks concurrently
with ThreadPoolExecutor(max_workers=NUM_OF_THREADS) as executor:
    while not queue.empty():
        # wait 1 second before starting a new thread
        time.sleep(1)
        futures.append(executor.submit(scrape_data, queue))

# Wait for all futures to complete
for future in as_completed(futures):
    future.result()



# combine the two csv files
# Load the first CSV file
df1 = pd.read_csv('scraped_data_food.csv', encoding='utf-8-sig')

# Load the second CSV file
df2 = pd.read_csv('scraped_data_food_coordinates.csv', encoding='utf-8-sig')

# for each href row in df1 check if the latitute and longitude is empty, if it is add the latitute and longitude from df2 based on the same href
for index, row in df1.iterrows():
    if pd.isna(row['latitude']) or pd.isna(row['longitude']):
        df2_row = df2.loc[df2['href'] == row['href']]
        if len(df2_row) > 0:
            df1.loc[index, 'latitude'] = df2_row.iloc[0]['latitude']
            df1.loc[index, 'longitude'] = df2_row.iloc[0]['longitude']

# Save the merged dataframe to a new CSV file
df1.to_csv('merged_data.csv', index=False, encoding='utf-8-sig')