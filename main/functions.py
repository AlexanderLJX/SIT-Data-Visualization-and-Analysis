import pandas as pd
import webbrowser
import folium
from folium.plugins import MarkerCluster
import tempfile
import os
import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk
from folium.plugins import HeatMapWithTime
from folium.plugins import TimestampedGeoJson
import json
import ast
import constants

# defining datas
def readfile():
    try:
        df_data=pd.read_csv('main/main.csv')
        return process_csv(df_data)
    #exception if the file cant be found 
    except FileNotFoundError:
        print(" CSV file could not be found.")
        exit(1)
    #exception if there are issues reading the csv file
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        exit(1)

def process_csv(df_data):
    # convert based on the features_datatypes
    for feature, datatype in constants.FEATURES_DATATYPES.items():
        if datatype == "string":
            df_data[feature] = df_data[feature].astype(str)
        elif datatype == "integer":
            df_data[feature] = pd.to_numeric(df_data[feature], errors='coerce')
        elif datatype == "float":
            df_data[feature] = pd.to_numeric(df_data[feature], errors='coerce')
        elif datatype == "dictionary":
            df_data[feature] = df_data[feature].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else x)
        elif datatype == "list":
            df_data[feature] = df_data[feature].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else x)
        elif datatype == "ISO8601":
            df_data[feature] = pd.to_datetime(df_data[feature], errors='coerce')
    # print dtypes
    print(df_data.dtypes)
    return df_data

def validate_filter_json(filter_json):
    try:
        # convert the json string to a list of dictionaries
        filter_list = json.loads(filter_json)
        # iterate through the list of dictionaries
        for filter_dict in filter_list:
            # get the column name from the dictionary
            column = filter_dict['column']
            # verify that the column is a key in the feature list
            if column not in constants.FEATURES_DATATYPES.keys():
                return f"{column} not a valid column"
            # get the value from the dictionary
            value = filter_dict['value']
            # verify that the value is the correct data type
            # TODO: verify that the value is the correct data type
            # get the operator from the dictionary
            operator = filter_dict['operator']
            # if the operator is not one of the valid operators
            if operator not in constants.OPERATORS:
                return f"{operator} not a valid operator"
    except:
        return "Not valid JSON"

    return "Valid JSON"

def validate_plot_json(plot_json):
    try:
        # convert the json string to a list of dictionaries
        plot_dict = json.loads(plot_json)
    # except and print the error
    except Exception as e:
        return "Not valid JSON"
    
    if 'feature1' not in plot_dict:
        return "feature1 not in the JSON"
    if 'plot' not in plot_dict:
        return "plot not in the JSON"
    
    # if json is a list of dictionaries
    if isinstance(plot_dict, list):
        return "Only one plot is allowed"
    
    # check if the plot type is valid
    if plot_dict['plot'] not in constants.PLOT_TYPES:
        return f"{plot_dict['plot']} not a valid plot type"
    # verify that the column is in feature list
    if plot_dict['feature1'] not in constants.FEATURES_DATATYPES.keys():
        return f"{plot_dict['feature1']} not a valid column"
    
    # if there is a feature2 check it too
    if 'feature2' in plot_dict:
        # verify that the column is in feature list
        if plot_dict['feature2'] not in constants.FEATURES_DATATYPES.keys():
            return f"{plot_dict['feature2']} not a valid column"
    
    # if plot is distribution make sure feature1 is in the JSON is a int or float
    if plot_dict['plot'] == "distribution":
        if constants.FEATURES_DATATYPES[plot_dict['feature1']] not in ["integer", "float"]:
            return f"{plot_dict['feature1']} not a valid column for distribution plot"
    
        
    
    
    return "Valid JSON"
    
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
    # convert the json string to a list of dictionaries
    filter_list = json.loads(filter_json)
    # make a copy of the dataframe so that the original dataframe is not modified
    df_data_filtered = df_data.copy()
    for filter_dict in filter_list:
        # get the column name from the dictionary
        column = filter_dict['column']
        # drop rows with NaN values or empty strings or lists or dictionaries
        df_data_filtered = df_data_filtered.dropna(subset=[column])
        # get the value from the dictionary
        value = filter_dict['value']
        # try converting the value to a float
        try:
            value = float(value)
            # try converting hte df column to a float as well
            df_data_filtered[column] = df_data_filtered[column].astype(float)
        except:
            pass
        # get the operator from the dictionary
        operator = filter_dict['operator']

        # if column = "About"
        if column == "About":
            # filter the dataframe based on the column, value and operator
            if operator == "==":
                df_data_filtered = df_data_filtered[df_data_filtered[column].apply(lambda x: value in x)]
            elif operator == "!=":
                df_data_filtered = df_data_filtered[~df_data_filtered[column].apply(lambda x: value in x)]
            else:
                df_data_filtered = df_data_filtered
            continue
        if column == "Tags":
            # Tags is a dictionary the value should be a key in the dictionary
            # convert value to lowercase
            value = value.lower()
            # convert keys to lowercase
            df_data_filtered[column] = df_data_filtered[column].apply(lambda x: {k.lower(): v for k, v in x.items()})
            # filter the dataframe based on the column, value and operator, some values are not in the dictionary
            if operator == "==":
                df_data_filtered = df_data_filtered[df_data_filtered[column].apply(lambda x: value == x.keys())]
            elif operator == "!=":
                df_data_filtered = df_data_filtered[~df_data_filtered[column].apply(lambda x: value == x.keys())]
            elif operator == "in":
                df_data_filtered = df_data_filtered[df_data_filtered[column].apply(lambda x: value in x.keys())]
            elif operator == "not in":
                df_data_filtered = df_data_filtered[~df_data_filtered[column].apply(lambda x: value in x.keys())]
            else:
                df_data_filtered = df_data_filtered
            continue
        if "Time" in column:
            # convert the column to a string
            df_data_filtered[column] = df_data_filtered[column].apply(lambda x: str(x))
            # filter the dataframe based on the column, value and operator
            if operator == "==":
                df_data_filtered = df_data_filtered[df_data_filtered[column] == value]
            elif operator == "!=":
                df_data_filtered = df_data_filtered[df_data_filtered[column] != value]
            elif operator == "largest":
                # sort by the column and get the top x latest times
                df_data_filtered = df_data_filtered.sort_values(by=column, ascending=False).head(int(value))
            elif operator == "smallest":
                # sort by the column and get the top x earliest times
                df_data_filtered = df_data_filtered.sort_values(by=column, ascending=True).head(int(value))
            else:
                df_data_filtered = df_data_filtered
            continue
        # convert the column to lowercase if it's a string
        df_data_filtered[column] = df_data_filtered[column].apply(lambda x: x.lower() if isinstance(x, str) else x)
        # convert value to lowercase if it's a string
        value = value.lower() if isinstance(value, str) else value
        # if column is a int or float, convert the value to a float
        if df_data_filtered[column].dtype == 'float64':
            value = float(value)
        if df_data_filtered[column].dtype == 'int64':
            value = int(value)
        # filter the dataframe based on the column, value and operator
        if operator == "==":
            df_data_filtered = df_data_filtered[df_data_filtered[column] == value]
        elif operator == ">":
            df_data_filtered = df_data_filtered[df_data_filtered[column] > value]
        elif operator == "<":
            df_data_filtered = df_data_filtered[df_data_filtered[column] < value]
        elif operator == ">=":
            df_data_filtered = df_data_filtered[df_data_filtered[column] >= value]
        elif operator == "<=":
            df_data_filtered = df_data_filtered[df_data_filtered[column] <= value]
        elif operator == "!=":
            df_data_filtered = df_data_filtered[df_data_filtered[column] != value]
        elif operator == "largest":
            # filter using list slicing, sort df in descending order by column and get the first x rows
            df_data_filtered = df_data_filtered.sort_values(by=column, ascending=False).head(int(value))
        elif operator == "smallest":
            # filter using list slicing, sort df in ascending order by column and get the first x rows
            df_data_filtered = df_data_filtered.sort_values(by=column, ascending=True).head(int(value))
        elif operator == "in":
            df_data_filtered = df_data_filtered[df_data_filtered[column].apply(lambda x: value in x)]
        elif operator == "not in":
            df_data_filtered = df_data_filtered[~df_data_filtered[column].apply(lambda x: value in x)]
        else:
            df_data_filtered = df_data_filtered
    
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

def plotmap_with_heat(df):  
    # Convert 'First Opening Time' to datetime and then to string
    df['First Opening Time'] = pd.to_datetime(df['First Opening Time']).dt.strftime('%Y-%m-%dT%H:%M:%S')
    
    # Drop rows with NaN values
    df = df.dropna(subset=['latitude', 'longitude', 'First Opening Time'])
    
    
    # Sort by 'First Opening Time'
    df['First Opening Time'] = pd.to_datetime(df['First Opening Time']).sort_values(ascending=True)
    
    # Group by 'First Opening Time' and create data for HeatMapWithTime
    data = []
    for _, d in df.groupby('First Opening Time'):
        data.append([[row['latitude'], row['longitude'], 1] for _, row in d.iterrows()])
    
    # Create map
    m = folium.Map(location=[1.287953,  103.851784], zoom_start=12)
    
    # Add HeatMapWithTime plugin
    hm = HeatMapWithTime(data, auto_play=True, max_opacity=0.8)
    hm.add_to(m)
    
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
