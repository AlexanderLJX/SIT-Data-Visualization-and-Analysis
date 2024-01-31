import PySimpleGUI as sg
import os
import webbrowser
import pandas as pd
from branca.element import Figure
import folium
from folium.plugins import MarkerCluster
import tempfile
import threading

sg.theme('DarkAmber')  # Add a touch of color

# Read data from the file
try:
    df = pd.read_csv('main/scraped_data_food.csv')
    df_data=pd.read_csv('main/modified_data.csv')
except FileNotFoundError:
    print("One or both CSV files could not be found.")
    exit(1)
except Exception as e:
    print(f"An error occurred while reading the CSV files: {e}")
    exit(1)

m=folium.Map(location=[1.287953, 103.851784],zoom_start=12,prefer_canvas=True)

marker_cluster = MarkerCluster().add_to(m)


def add_markers(df_data, marker_cluster):
    coordinates = df_data.apply(lambda row: [row['Name'], row['latitude'], row['longitude']], axis=1)
    for coord in coordinates:
        folium.Marker(location=[coord[1], coord[2]], popup=str(coord[0]), tooltip='Click here to see restaurant').add_to(marker_cluster)
# Start a new thread for the for loop
thread = threading.Thread(target=add_markers, args=(df_data, marker_cluster))
thread.start()
# Save the HTML content to a temporary file
with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
    tmp.write(m._repr_html_().encode('utf-8'))
    tmp.close()
font = ("Arial", 11)
layout = [
    
    [sg.Text('What would you like to do today?', font=font)],
    [sg.Text('Choose one of the following options : ', font=font)],
    [],
    [sg.Button('View all food places', key='-VIEW-ALL-', size=(30, 2), pad=(10,10)), sg.Button('View Dataset diagrams', key='-VIEW-DIAGRAMS-', pad=(10,10), size=(30, 2)), sg.Button('Export the Dataset', key='-EXPORT-', pad=(10,10), size=(30, 2) , font=font)],
    [],
    [sg.Text('Choose the area in Singapore : ', font=font),sg.Combo(['Bukit Batok','Bukit Timah','Sengkang','Hougang'], key='-OPTION-', pad=(10,10), size=(30, 2), font=font)],
    [sg.Text( font=font)],
    [sg.Button('Ok', size=(3, 2), font=font), sg.Button('Cancel', size=(6, 2), font=font)],
    [],
]

window = sg.Window('Foodplaces in Singapore', layout, size=(1000, 300),element_justification='center', resizable=True, finalize=True)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
        
    if event == '-VIEW-ALL-':
            # Open the temporary file in a web browser
            webbrowser.open("file://" + os.path.realpath(tmp.name))
        
    elif event == '-VIEW-DIAGRAMS-':
        print('View Dataset diagrams')


    elif event == '-EXPORT-':
        filename = sg.popup_get_file('Select a file to save to', save_as=True, file_types=(("CSV Files", "*.csv"),))
        if filename:
            df.to_csv(filename, index=False)


    elif event == '-VIEW-AREAS-':
        print('View in areas of Singapore')

# Close the PySimpleGUI window
window.close()
os.remove(tmp.name)
