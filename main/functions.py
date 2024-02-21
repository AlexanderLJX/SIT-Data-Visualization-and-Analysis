import pandas as pd
import webbrowser
import folium
from folium.plugins import MarkerCluster
import tempfile
import os
from folium.plugins import TimestampedGeoJson
import json
import constants
from util import process_df

def validate_filter_condition(condition):
    # Validate a single filter condition (leaf node)
    if 'column' in condition:
        column, operator = condition.get('column'), condition.get('operator')
        
        # Validate column
        if column not in constants.FEATURES_DATATYPES:
            return f"{column} not a valid column"
        
        # Validate operator
        if operator not in constants.OPERATORS:
            return f"{operator} not a valid operator"
        
        # Validate value based on column's data type (example simplified for brevity)
        # Additional checks for data type correctness would be similar to your initial approach
        
        return "Valid JSON"  # Return valid if all checks pass for a condition
    
    else:
        return None  # Indicate that this is not a leaf node

def validate_filter_json_recursive(filter_json):
    if filter_json == "":
        return "Valid JSON"
    try:
        filter_obj = json.loads(filter_json) if isinstance(filter_json, str) else filter_json
        
        def recursive_validate(node):
            # Base case for leaf nodes
            validation_result = validate_filter_condition(node)
            if validation_result:
                return validation_result
            
            # Recursive case for logical gates
            if 'gate' in node and 'input1' in node and 'input2' in node:
                gate = node['gate']
                if gate.lower() not in ['and', 'or']:
                    return f"{gate} is not a valid logical gate"
                
                # Recursively validate input1 and input2
                input1_result = recursive_validate(node['input1'])
                input2_result = recursive_validate(node['input2'])
                
                if input1_result != "Valid JSON":
                    return input1_result
                if input2_result != "Valid JSON":
                    return input2_result
                
                return "Valid JSON"  # Both inputs are valid
            
            return "Invalid JSON structure"  # Missing required keys or structure is incorrect
        
        # Start the recursive validation
        return recursive_validate(filter_obj)
    
    except ValueError as e:  # Catch JSON parsing errors
        return f"JSON parsing error: {str(e)}"
    except Exception as e:  # Catch all other exceptions
        return f"Unexpected error: {str(e)}"

def validate_filter_json(filter_json):
    if filter_json == "":
        return "Valid JSON"
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
            values = filter_dict['values']
            # verify that the value is the correct data type, can be converted to the data type of the column
            for value in values:
                if constants.FEATURES_DATATYPES[column] == "string":
                    try:
                        str(value)
                    except:
                        return f"{value} should be a string"
                elif constants.FEATURES_DATATYPES[column] == "integer":
                    try:
                        int(value)
                    except:
                        return f"{value} should be an integer"
                elif constants.FEATURES_DATATYPES[column] == "float":
                    try:
                        float(value)
                    except:
                        return f"{value} should be a float"
                elif constants.FEATURES_DATATYPES[column] == "ISO8601":
                    try:
                        pd.to_datetime(value, format='%H:%M')
                    except:
                        return f"{value} should be in ISO8601 format"
            # get the operator from the dictionary
            operator = filter_dict['operator']
            # if the operator is not one of the valid operators
            if operator not in constants.OPERATORS:
                return f"{operator} not a valid operator"
    except Exception as e:
        return "Not valid JSON"

    return "Valid JSON"

def validate_plot_json(plot_json):
    try:
        plot_dict = json.loads(plot_json)
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

def validate_train_json(train_json):
    try:
        train_dict = json.loads(train_json)
    except Exception as e:
        return "Not valid JSON"
    
    if 'model' not in train_dict:
        return "model not in the JSON"
    if 'features' not in train_dict:
        return "features not in the JSON"
    # if 'target' not in train_dict: # target is the column to predict
    #     return "target not in the JSON"
    
    # if json is a list of dictionaries
    if isinstance(train_dict, list):
        return "Only one model is allowed"
    
    # check if the model type is valid
    if train_dict['model'] not in constants.ML_MODELS:
        return f"{train_dict['model']} not a valid model type"
    # verify that each feature is in feature list
    for feature in train_dict['features']:
        if feature not in constants.PLOT_FEATURES_DATATYPES.keys():
            return f"{feature} not a valid column"
        
    # if model is isolation forest, make sure columns are float or integer
    if train_dict['model'] == "isolation forest":
        for feature in train_dict['features']:
            if constants.PLOT_FEATURES_DATATYPES[feature] not in ["integer", "float"]:
                return f"{feature} not a valid column for isolation forest model"
            
    # if model is linear regression, make sure columns are float or integer
    if train_dict['model'] == "linear regression":
        for feature in train_dict['features']:
            if constants.PLOT_FEATURES_DATATYPES[feature] not in ["integer", "float"]:
                return f"{feature} not a valid column for linear regression model"
        # make sure target is a float or integer
        if constants.PLOT_FEATURES_DATATYPES[train_dict['target']] not in ["integer", "float"]:
            return f"{train_dict['target']} not a valid column for linear regression model"
    
    # if model is random forest, make sure columns are float or integer

    # # verify that the column is in feature list
    # if train_dict['target'] not in constants.PLOT_FEATURES_DATATYPES.keys():
    #     return f"{train_dict['target']} not a valid column"

    return "Valid JSON"
    
def filter_df(planning_area, category, df_data):
    if planning_area:  # If value1 is not empty, it contains a list of selected areas
        df_data_filtered = df_data.loc[df_data['Planning Area'].isin(planning_area)]
    else:
        df_data_filtered = df_data

    if category:  # If value2 is not empty, it contains a list of selected categories
        df_data_filtered = df_data_filtered.loc[df_data_filtered['Category'].isin(category)]

    return df_data_filtered

def filter_or(filter_dict, df_data_filtered):
    # get the column name from the dictionary
    column = filter_dict['column']
    # drop rows with NaN values or empty strings or lists or dictionaries
    df_data_filtered = df_data_filtered.dropna(subset=[column])
    # get the value from the dictionary
    values = filter_dict['values']
    operator = filter_dict['operator']
    # convert values to the data type of the column
    if constants.FEATURES_DATATYPES[column] == "string":
        # convert values and column to lowercase
        values = [str(value).lower() for value in values]
        df_data_filtered[column] = df_data_filtered[column].apply(lambda x: str(x).lower())
        if operator == "==":
            df_data_filtered = df_data_filtered[df_data_filtered[column].apply(lambda x: x in values)]
        elif operator == "!=":
            df_data_filtered = df_data_filtered[~df_data_filtered[column].apply(lambda x: x in values)]
        elif operator == "largest":
            # filter by counting number of unique string values
            df_data_filtered = df_data_filtered.groupby(column).size().sort_values(ascending=False).head(int(values[0]))
        elif operator == "smallest":
            # filter by counting number of unique string values
            df_data_filtered = df_data_filtered.groupby(column).size().sort_values(ascending=True).head(int(values[0]))
        elif operator == "in":
            df_data_filtered = df_data_filtered[df_data_filtered[column].apply(lambda x: value in x for value in values)]
        elif operator == "not in":
            df_data_filtered = df_data_filtered[~df_data_filtered[column].apply(lambda x: value in x for value in values)]
    elif constants.FEATURES_DATATYPES[column] == "integer" or constants.FEATURES_DATATYPES[column] == "float":
        values = [float(value) for value in values]
        # filter the dataframe based on the column, value and operator
        if operator == "==":
            df_data_filtered = df_data_filtered[df_data_filtered[column].apply(lambda x: x in values)]
        elif operator == ">":
            df_data_filtered = df_data_filtered[df_data_filtered[column].apply(lambda x: x > values[0])]
        elif operator == "<":
            df_data_filtered = df_data_filtered[df_data_filtered[column].apply(lambda x: x < values[0])]
        elif operator == ">=":
            df_data_filtered = df_data_filtered[df_data_filtered[column] >= values[0]]
        elif operator == "<=":
            df_data_filtered = df_data_filtered[df_data_filtered[column] <= values[0]]
        elif operator == "!=":
            df_data_filtered = df_data_filtered[~df_data_filtered[column].apply(lambda x: x in values)]
        elif operator == "largest":
            # filter using list slicing, sort df in descending order by column and get the first x rows
            df_data_filtered = df_data_filtered.sort_values(by=column, ascending=False).head(int(values[0]))
        elif operator == "smallest":
            # filter using list slicing, sort df in ascending order by column and get the first x rows
            df_data_filtered = df_data_filtered.sort_values(by=column, ascending=True).head(int(values[0]))
    elif constants.FEATURES_DATATYPES[column] == "ISO8601":
        values = [pd.to_datetime(value, format='%H:%M') for value in values]
        # # convert the column to a string
        # df_data_filtered[column] = df_data_filtered[column].apply(lambda x: str(x))
        # filter the dataframe based on the column, value and operator
        if operator == "==":
            df_data_filtered = df_data_filtered[df_data_filtered[column].apply(lambda x: x in values)]
        elif operator == "!=":
            df_data_filtered = df_data_filtered[~df_data_filtered[column].apply(lambda x: x in values)]
        elif operator == "largest":
            # sort by the column and get the top x latest times
            value = values[0]
            df_data_filtered = df_data_filtered.sort_values(by=column, ascending=False).head(int(value))
        elif operator == "smallest":
            # sort by the column and get the top x earliest times
            value = values[0]
            df_data_filtered = df_data_filtered.sort_values(by=column, ascending=True).head(int(value))
        else:
            df_data_filtered = df_data_filtered
    elif constants.FEATURES_DATATYPES[column] == "list":
        # filter the dataframe based on the column, value and operator
        if operator == "==":
            df_data_filtered = df_data_filtered[df_data_filtered[column].apply(lambda x: any(y in x for y in values))]
        elif operator == "!=":
            df_data_filtered = df_data_filtered[~df_data_filtered[column].apply(lambda x: any(y in x for y in values))]
        else:
            df_data_filtered = df_data_filtered
    elif column == "Tags":
        # Tags is a dictionary the value should be a key in the dictionary
        # convert value to lowercase
        value = value.lower()
        # convert keys to lowercase
        df_data_filtered[column] = df_data_filtered[column].apply(lambda x: {k.lower(): v for k, v in x.items()})
        # filter the dataframe based on the column, value and operator, some values are not in the dictionary
        if operator == "==":
            df_data_filtered = df_data_filtered[df_data_filtered[column].apply(lambda x: set(x.keys()) <= set(values))]
        elif operator == "!=":
            df_data_filtered = df_data_filtered[~df_data_filtered[column].apply(lambda x: set(x.keys()) <= set(values))]
        elif operator == "in":
            df_data_filtered = df_data_filtered[df_data_filtered[column].apply(lambda x: any(key in values for key in x.keys()))]
        elif operator == "not in":
            df_data_filtered = df_data_filtered[~df_data_filtered[column].apply(lambda x: any(key in values for key in x.keys()))]
        else:
            df_data_filtered = df_data_filtered

def filter_one(column, operator, value, df_data_filtered):
    # drop rows with NaN values or empty strings or lists or dictionaries
    df_data_filtered = df_data_filtered.dropna(subset=[column])
    if constants.FEATURES_DATATYPES[column] == "string":
        # convert values and column to lowercase
        value = str(value).lower()
        df_data_filtered[column] = df_data_filtered[column].apply(lambda x: str(x).lower())
        if operator == "==":
            df_data_filtered = df_data_filtered[df_data_filtered[column] == value]
        elif operator == "!=":
            df_data_filtered = df_data_filtered[df_data_filtered[column] != value]
        elif operator == "in":
            df_data_filtered = df_data_filtered[df_data_filtered[column].apply(lambda x: value in x)]
        elif operator == "not in":
            df_data_filtered = df_data_filtered[~df_data_filtered[column].apply(lambda x: value in x)]
        elif operator == "largest":
            df_data_filtered = df_data_filtered.sort_values(by=column, ascending=False).head(int(value))
        elif operator == "smallest":
            df_data_filtered = df_data_filtered.sort_values(by=column, ascending=True).head(int(value))
    elif constants.FEATURES_DATATYPES[column] == "integer" or constants.FEATURES_DATATYPES[column] == "float":
        value = float(value)
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
            df_data_filtered = df_data_filtered.sort_values(by=column, ascending=False).head(int(value))
        elif operator == "smallest":
            df_data_filtered = df_data_filtered.sort_values(by=column, ascending=True).head(int(value))
    elif constants.FEATURES_DATATYPES[column] == "ISO8601":
        value = pd.to_datetime(value, format='%H:%M')
        if operator == "==":
            df_data_filtered = df_data_filtered[df_data_filtered[column] == value]
        elif operator == "!=":
            df_data_filtered = df_data_filtered[df_data_filtered[column] != value]
        elif operator == "largest":
            df_data_filtered = df_data_filtered.sort_values(by=column, ascending=False).head(int(value))
        elif operator == "smallest":
            df_data_filtered = df_data_filtered.sort_values(by=column, ascending=True).head(int(value))
    elif constants.FEATURES_DATATYPES[column] == "list":
        if operator == "==":
            df_data_filtered = df_data_filtered[df_data_filtered[column].apply(lambda x: value in x)]
        elif operator == "!=":
            df_data_filtered = df_data_filtered[~df_data_filtered[column].apply(lambda x: value in x)]
    elif column == "Tags":
        # Tags is a dictionary the value should be a key in the dictionary
        # convert value to lowercase
        value = value.lower()
        # convert keys to lowercase
        df_data_filtered[column] = df_data_filtered[column].apply(lambda x: {k.lower(): v for k, v in x.items()})
        if operator == "==":
            df_data_filtered = df_data_filtered[df_data_filtered[column].apply(lambda x: value in x.keys())]
        elif operator == "!=":
            df_data_filtered = df_data_filtered[~df_data_filtered[column].apply(lambda x: value in x.keys())]
        elif operator == "in":
            df_data_filtered = df_data_filtered[df_data_filtered[column].apply(lambda x: value in x.keys())]
        elif operator == "not in":
            df_data_filtered = df_data_filtered[~df_data_filtered[column].apply(lambda x: value in x.keys())]

    return df_data_filtered

def parse_logic(expression, df_data_filtered):
    # Base case: if the expression is a condition (leaf node)
    if "column" in expression:
        # Construct the condition string
        column = expression["column"]
        operator = expression["operator"]
        value = expression.get("value", "")

        return filter_one(column, operator, value, df_data_filtered)
    
    # Recursive case: if the expression is a logical gate (non-leaf node)
    else:
        gate = expression["gate"].upper()  # AND, OR, etc.
        df_input1 = parse_logic(expression["input1"], df_data_filtered.copy())
        df_input2 = parse_logic(expression["input2"], df_data_filtered.copy())

        if gate == "AND":
            # combine dataframes, keeping only rows that are present in both dataframes, do not include the index in merge
            ndf_data_filtered = pd.merge(df_input1, df_input2, on='href', suffixes=('', '__2'), how='inner')
            # Drop the duplicate columns
            ndf_data_filtered.drop(columns=[col for col in ndf_data_filtered.columns if '__2' in col], inplace=True)
            return ndf_data_filtered
        elif gate == "OR":
            # combine dataframes, keeping all rows from both dataframes
            ndf_data_filtered = pd.concat([df_input1, df_input2])
            return ndf_data_filtered
        

def filter_df_json(filter_json, df_data):
    # convert the json string to a list of dictionaries
    filter_json = json.loads(filter_json)
    # make a copy of the dataframe so that the original dataframe is not modified
    df_data_filtered = df_data.copy()
    df_data_filtered = parse_logic(filter_json, df_data_filtered)
    
    return df_data_filtered

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

def plotmap_with_animation(df, time_feature):
    # Convert 'Time' to string in ISO format if it's not already, eg 11:00:00, there is no date, only time, so make it today's date
    # get today's date in the format 2024-02-19
    today = pd.to_datetime('today').strftime('%Y-%m-%d')
    df[time_feature] = pd.to_datetime(df[time_feature]).dt.strftime(today + 'T%H:%M:%S')

    # drop rows with NaN values
    df = df.dropna(subset=['latitude', 'longitude', time_feature])

    features = []
    for _, row in df.iterrows():
        feature = {
            'type': 'Feature',
            'properties': {
                'time': row[time_feature],
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

















