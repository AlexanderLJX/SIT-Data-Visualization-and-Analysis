# Dining Insights: Singapore

## Overview

Welcome to the Dining Insights project by Group 3! This Python project focuses on analyzing and visualizing data from dine-in food places, including restaurants and coffee shops, in Singapore. Our objective aligns with the requirements of the ICT1002 Programming Fundamentals course, aiming to apply and deepen our Python programming skills, practice team collaboration using Python tools and libraries, and gain hands-on experience in solving real-world problems.

## Project Scope

In adherence to the project specifications, we will explore various aspects of dining establishments in Singapore, such as:

- **Location Ratings:** Identifying areas with higher ratings based on customer reviews.
- **Price Analysis:** Analyzing the distribution of food prices, highlighting places with more expensive and more affordable options.
- **Cuisine Diversity:** Exploring the types of cuisine available in specific areas.
- **Review Quality:** Identifying locations with better and higher reviews.

## Tools and Technologies

To achieve our objectives, we will leverage the following technologies:

- **Python:** The primary programming language for data processing, analysis, and visualization.
- **Google Maps:** To scrape relevant data about dine-in establishments in Singapore.
- **Data Visualization Libraries:** Utilizing libraries like Matplotlib and Seaborn for creating pie charts, bar graphs, and other visualizations.

## Project Structure

The project will be organized into the following sections:

1. **Data Collection:** Scraping relevant data from Google Maps using Selenium.
2. **Data Processing:** Cleaning and organizing the collected data for analysis.
3. **Data Analysis:** Extracting insights from the dataset to answer specific questions about dining establishments.
4. **Data Visualization:** Creating visually appealing and informative charts and graphs to represent our findings.
5. **Documentation:** Providing comprehensive documentation to guide users and developers through the project.

## Getting Started

To launch the GUI simply double click `launch_gui.py`

Alternatively, you can follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/AlexanderLJX/SIT-Data-Visualization-and-Analysis.git
   cd SIT-Data-Visualization-and-Analysis
2. **Create a virtual environment**
   ```bash
   python -m venv venv
3. **Activate the virtual environment**
   ```bash
   venv\Scripts\activate.bat
4. **Install the dependencies**
   ```bash
   pip install -r requirements.txt
5. **Launch the project**
   ```bash
   python main.py
   ```


## Web Scraper

1. Lauching the web srcaper
   ```bash
   python googlemaps_scraper/scraper.py

## Data Cleansing and Data Visualization Notebooks

You can either use the jupyter notebook extension in Visual Studio Code or use the Jupyter Notebook application.
1. Install Jupyter Notebook
   ```bash
   pip install notebook

2. Launch Jupyter Notebook and open the notebook files
   ```bash
   jupyter notebook

## Data 

**Restaurants csv:**
 - **href:** Link to the restaurant. Format is a string.
 - **Planning Area** 1 of the 55 Planning Areas in Singapore. Format is a string
 - **Subzone:** Subzone of planning area. Format is a string.
 - **Name:** Name of the restaurant. Format is a string.
 - **Search Engine Rating:** 1 means it it the first restaurant that appears in the list when searching that specific area, 2 means it's the second, and so on. Format is an integer.
 - **Sponsored:** Whether the restaurant paid for google advertising. This will probably mean it will be the first to appear in the list, search engine rating 1. Format is a string, either 'Yes' or 'No'.
 - **Opening Hours** Opening hours of the restaurant. Provided as a dictionary, the key is the day of the week and the value is a list of opening hours, each element in that list is a dictionary with a 'open' and 'close' value with the key being the time e.g. '9 am'. If 'open' and 'close' value is 'Closed' means the restaurant is closed on that day. If 'open' is '12 am' and 'close' is '12 am' means the restaurant is opened the whole day. The values are lists because some restaurants have more than 1 opening and closing time for example, open from 11am to 3pm then close then open from 5 pm to 10pm.
 - **Popular Times:** Provided as a dictionary where each key represents a day of the week (e.g., 'Monday', 'Tuesday') and the value is another dictionary. This inner dictionary's keys are times of the day (e.g., '6 am', '7 am') with corresponding values indicating the percentage of the establishment's usual crowd at that time (e.g., '24%', '41%'). This data is based on aggregated and anonymized Location History data from Google Maps users.
 - **Average Star Rating:** The average star rating given to the establishment by reviewers. Format is a decimal number (float) (e.g., 4.2).
 - **Reviews:** The total number of reviews left for the establishment. Format is an integer.
 - **Category:** The type or category of the establishment (e.g., 'Shopping mall', 'Restaurant'). Format is a string.
 - **Price Rating:** An indicator of the price range of the establishment, based on the official Google price rating system, the number of dollar signs (e.g., '$', '$$'). It is provided as a String, either 'Moderate', 'Inexpensive', 'Very Expensive' or listed as 'NAN' if not available.
 - **Address:** Address of the restaurant. Provided as a String.
 - **Metadata:** Additional information about the establishment, potentially including a website URL, phone number, unique location code, and other relevant details. Provided as a list of strings.
 - **Tags:** Keywords or phrases frequently mentioned in reviews or associated with the establishment. Provided as a dictionary where keys are tags related to the food or service provided by the restaurant (e.g., 'wine', 'mussels', 'dinner', 'ingredients') and values are integers representing the number of times the tag has been mentioned or associated with the restaurant.
 - **About:** A list of features, services, or attributes of the restaurant, such as 'Dine-in', 'Delivery', 'Wheelchair-accessible entrance', etc., provided in a list format.


**Reviews csv:**
 - **href of Place:** The URL linking to the Google Maps page of the place. It serves as a unique identifier that can be used as a primary key to relate to entries in the Restaurants CSV. Format is a string.
 - **Review ID:** A unique identifier for the review. Format is a string.
 - **Relavancy Ranking:** Indicates the order of relevance of the review, with 1 being the most relevant and appearing as the first review. Format is an integer.
 - **Reviewer href:** The URL to the reviewer's Google Maps profile. It can serve as a unique identifier or primary key for reviewers. Format is a string.
 - **Reviewer Name:** The name of the person who left the review. Format is a string.
 - **Local Guide:** Indicates whether the reviewer is part of the Google Local Guide program. Format is a boolean, represented as 'True' or 'False'.
 - **Total Reviews:** The total number of reviews the reviewer has posted on Google Maps. Format is an integer.
 - **Total Photos:** The total number of photos the reviewer has uploaded to Google Maps. Format is an integer.
 - **Star Rating:** The star rating given by the reviewer, typically on a scale from 1 to 5. Format is an integer.
 - **Date:** The date and time when the review was posted. This is calculated based on the relative time from the current date. Format is a datetime string.
 - **Review:** The text content of the review. Format is a string.
 - **Metadata:** Additional information related to the review, such as ratings for specific aspects like food or service, meal type, price per person, recommended dishes, and atmosphere. This is provided as a list of strings or key-value pairs enclosed in brackets.
 - **Likes:** The number of likes the review has received. Format is an integer.
 - **Review Images href:** The URLs to the images attached to the review. Format is a list of strings.

 

## TODO

- detected browser out of memory error

- Detect temporarily closed restaurants