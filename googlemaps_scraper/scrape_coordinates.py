import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue

# CSV file path
CSV_FILE_PATH = 'scraped_data_food_processed.csv'

NEW_CSV_FILE_PATH = 'scraped_data_food_processed_coordinates.csv'

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

# Function to scrape data for a single row
def scrape_data(row, queue):
    global counter
    coordinates = []
    driver = webdriver.Chrome(options=chrome_options)
    url = row['href']
    while not queue.empty():
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
                    print(f"Processed {counter} out of {len(df)} addresses. Latitude: {lat}, Longitude: {lng}")
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
    queue.put(row['href'])

# Use ThreadPoolExecutor to execute tasks concurrently
with ThreadPoolExecutor(max_workers=10) as executor:
    for index, row in df.iterrows():
        # wait 2 second before starting a new thread
        import time
        time.sleep(2)
        futures.append(executor.submit(scrape_data, row, queue))

# Wait for all futures to complete
for future in as_completed(futures):
    future.result()

# close the writer
csv_writer.close()
