import pandas as pd
import webbrowser
import folium
from folium.plugins import MarkerCluster
import tempfile
import os
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk
from folium.plugins import HeatMap
from folium.plugins import TimestampedGeoJson
import json
import ast

# defining datas
def readfile():
    try:
        df_data=pd.read_csv('main/scraped_data_food_full_processed.csv')
        return df_data
    #exception if the file cant be found 
    except FileNotFoundError:
        print(" CSV file could not be found.")
        exit(1)
    #exception if there are issues reading the csv file
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        exit(1)
    
def filter_df(planning_area, category, df_data):
    if planning_area != '' and planning_area != []:
        df_data_filtered = df_data[df_data['Planning Area'] == planning_area[0]]
    else:
        df_data_filtered = df_data

    if category != '' and category != []:
        df_data_filtered = df_data_filtered[df_data_filtered['Category'] == category[0]]

    return df_data_filtered

def filter_df_json(filter_json, df_data):
    # {"column": "About", "value": "LGBTQ friendly restaurants", "operator": "=="
    # convert the json string to a dictionary
    filter_dict = json.loads(filter_json)
    # get the column name from the dictionary
    column = filter_dict['column']
    # drop rows with NaN values or empty strings or lists or dictionaries
    df_data = df_data.dropna(subset=[column])
    # get the value from the dictionary
    value = filter_dict['value']
    # try converting the value to a float
    try:
        value = float(value)
        # try converting hte df column to a float as well
        df_data[column] = df_data[column].astype(float)
    except:
        pass
    # get the operator from the dictionary
    operator = filter_dict['operator']

    # if column = "About"
    if column == "About":
        # convert the value of the column which is string of a list to an actual list with ast.literal_eval
        df_data[column] = df_data[column].apply(lambda x: ast.literal_eval(x))
        # filter the dataframe based on the column, value and operator
        if operator == "==":
            df_data_filtered = df_data[df_data[column].apply(lambda x: value in x)]
        elif operator == "!=":
            df_data_filtered = df_data[~df_data[column].apply(lambda x: value in x)]
        else:
            df_data_filtered = df_data
        
        return df_data_filtered
    # filter the dataframe based on the column, value and operator
    if operator == "==":
        df_data_filtered = df_data[df_data[column] == value]
    elif operator == ">":
        df_data_filtered = df_data[df_data[column] > value]
    elif operator == "<":
        df_data_filtered = df_data[df_data[column] < value]
    elif operator == ">=":
        df_data_filtered = df_data[df_data[column] >= value]
    elif operator == "<=":
        df_data_filtered = df_data[df_data[column] <= value]
    elif operator == "!=":
        df_data_filtered = df_data[df_data[column] != value]
    else:
        df_data_filtered = df_data
    
    return df_data_filtered

def plotmap_3d(df):

    # Define the layer for the 3D scatter plot
    # layer = pdk.Layer(
    #     'ScatterplotLayer',     # Use a scatter plot layer
    #     df,
    #     get_position=['longitude', 'latitude'],
    #     get_color=[255, 0, 0, 160],    # Red color for the points
    #     get_radius=100,                # Radius of the points
    #     get_elevation='Average Star Rating',     # Use some 'elevation' value if your data has it, otherwise set a constant value
    #     elevation_scale=50,             # Scale for elevation to adjust the 3D effect
    # )
    layer = pdk.Layer(
    'HexagonLayer',  # `type` positional argument is here
    df,
    get_position=['longitude', 'latitude'],
    auto_highlight=True,
    elevation_scale=10,
    pickable=True,
    elevation_range=[0, 2000],
    extruded=True,
    coverage=1,
    radius=500)

    # Set the view for the 3D map
    view_state = pdk.ViewState(latitude=df['latitude'].mean(), longitude=df['longitude'].mean(), zoom=12, pitch=50)

    # Create the deck.gl map with CARTO as the map provider (no API key required)
    r = pdk.Deck(layers=[layer], 
                 initial_view_state=view_state, 
                 map_style='light',  # Using a CARTO basemap style
                 map_provider='carto')  # Specifying CARTO as the map provider

    # Save the map to an HTML file and open it in the browser
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
        r.to_html(tmp.name)
        webbrowser.open("file://" + os.path.realpath(tmp.name))
        
    return tmp.name


    # lat_long = [[row['latitude'], row['longitude']] for index, row in df_data_filtered.iterrows()]

    # # Adjust the gradient parameter to change the color thresholds
    # gradient = {
    #     0.3: 'blue',
    #     0.6: 'lime',
    #     0.8: 'yellow',
    #     0.9: 'orange',
    #     1.1: 'red'
    # }
    
    # # Create and add a HeatMap layer
    # HeatMap(lat_long, radius=15).add_to(m)

def plotmap_with_animation(df):
    # Convert 'Time' to string in ISO format if it's not already
    df['First Opening Time'] = pd.to_datetime(df['First Opening Time']).dt.strftime('%Y-%m-%dT%H:%M:%S')

    # drop rows with NaN values
    df = df.dropna(subset=['latitude', 'longitude', 'First Opening Time'])
    
    # Create GeoJSON features
    features = []
    for _, row in df.iterrows():
        feature = {
            'type': 'Feature',
            'properties': {
                'time': row['First Opening Time'],
                'name': row['Name']
                # Add other properties here if necessary
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [row['longitude'], row['latitude']]
            }
        }
        features.append(feature)
    
    # Construct GeoJSON FeatureCollection
    geojson = {
        'type': 'FeatureCollection',
        'features': features
    }
    
    # Create map
    m = folium.Map(location=[1.287953, 103.851784], zoom_start=12)
    
    # https://python-visualization.github.io/folium/latest/reference.html#module-folium.plugins
    # Add TimestampedGeoJson plugin
    TimestampedGeoJson(
        geojson,
        period='PT1H', # 1 hour intervals
        duration='PT1H', # appears for 1 hours then disappears in the animation
        transition_time=300, # 0.3 seconds per interval
        add_last_point=True,
        auto_play=True,
        loop=False,
        max_speed=1,
        loop_button=True,
        date_options='HH:mm:ss',
        time_slider_drag_update=True
    ).add_to(m)
    
    # Save and open the map
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
        m.save(tmp.name)
        webbrowser.open("file://" + os.path.realpath(tmp.name))
    
    return tmp.name

#defining a function to plot the locations on the map
def plotmap(df):
    #setting the map and the geo location that we want the users to focus on (e.g. Singapore) by using SG coordininates
    m=folium.Map(location=[1.287953, 103.851784],zoom_start=12,prefer_canvas=True)
    #getting the coordinates from the data set then adding the markers
    coordinates = df.apply(lambda row: [row['Name'], row['latitude'], row['longitude']], axis=1)
    marker_cluster = MarkerCluster().add_to(m)
    for coord in coordinates:
        folium.Marker(location=[coord[1], coord[2]], popup=str(coord[0]), tooltip='Click here to see restaurant').add_to(marker_cluster)

    # Save the HTML content to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
        tmp.write(m._repr_html_().encode('utf-8'))
        tmp.close()
    # Open the temporary file in a web browser (better for rendering)
    webbrowser.open("file://" + os.path.realpath(tmp.name))
    # Return the name of the temporary file so that we can delete the temp file after the user closes the window
    return tmp.name

def piechart():
    y = np.array([35, 25, 25, 15])
    plt.pie(y)
    plt.show()

def bargraph():
    x = np.array(["A", "B", "C", "D"])
    y = np.array([3, 8, 1, 10])

    plt.bar(x,y)
    plt.show()
