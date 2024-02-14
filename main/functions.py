import pandas as pd
import webbrowser
import folium
from folium.plugins import MarkerCluster
import tempfile
import os

# defining datas
def readfile():
    try:
        df_data=pd.read_csv('main/main.csv')
        return df_data
    #exception if the file cant be found 
    except FileNotFoundError:
        print(" CSV file could not be found.")
        exit(1)
    #exception if there are issues reading the csv file
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        exit(1)
    




#defining a function to plot the locations on the map
def plotmap(value1, value2, df_data):
    #if value 1 is not empty if filters out the data else it will take the whole dataset
    if value1!='':
       df_data_filtered = df_data.loc[df_data['Planning Area'] == value1]
    else: 
        df_data_filtered=df_data
   #if value 2 is not empty it filters out the data either from value or it does not 
    if value2 != '':
        df_data_filtered = df_data_filtered.loc[df_data_filtered['Category'] == value2]
    else :
        df_data_filtered=df_data_filtered
    #setting the map and the geo location that we want the users to focus on (e.g. Singapore) by using SG coordininates
    m=folium.Map(location=[1.287953, 103.851784],zoom_start=12,prefer_canvas=True)
    #getting the coordinates from the data set then adding the markers
    coordinates = df_data_filtered.apply(lambda row: [row['Name'], row['latitude'], row['longitude']], axis=1)
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