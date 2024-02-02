import PySimpleGUI as sg
import os
import webbrowser
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import tempfile
import shutil

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

def plotmap(value1, value2):
    if value1!='':
       df_data_filtered = df_data.loc[df_data['Sub Area'] == value1]
    else: 
        df_data_filtered=df_data

    if value2 != '':
        df_data_filtered = df_data_filtered.loc[df_data_filtered['Category'] == value2]
    else :
        df_data_filtered=df_data_filtered
    m=folium.Map(location=[1.287953, 103.851784],zoom_start=12,prefer_canvas=True)
    coordinates = df_data_filtered.apply(lambda row: [row['Name'], row['latitude'], row['longitude']], axis=1)
    marker_cluster = MarkerCluster().add_to(m)
    
    for coord in coordinates:
        folium.Marker(location=[coord[1], coord[2]], popup=str(coord[0]), tooltip='Click here to see restaurant').add_to(marker_cluster)

# Save the HTML content to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
        tmp.write(m._repr_html_().encode('utf-8'))
        tmp.close()
    # Open the temporary file in a web browser
    webbrowser.open("file://" + os.path.realpath(tmp.name))
    # Return the name of the temporary file
    return tmp.name



#find the catgory types in the csv

unique_cat = df_data['Category'].unique()
unique_cat_list = list(map(str, unique_cat))


# find the sub area types in the csv
unique_Area = df_data['Sub Area'].unique()
unique_Area_list = list(map(str, unique_Area))

#creatig the gui
font = ("Arial",11)
layout = [
    
    [sg.Text('What would you like to do today?', font=font)],
    [sg.Text('Choose one of the following options : ', font=font)],
    [],
    [sg.Button('View all food places', key='-VIEW-ALL-', size=(30, 2), pad=(10,10)), sg.Button('View Dataset diagrams', key='-VIEW-DIAGRAMS-', pad=(10,10), size=(30, 2)), sg.Button('Export Dataset', key='-EXPORT-', pad=(10,10), size=(30,2), font=font)],
    [],
    [sg.Text('Choose the area in Singapore : ', font=font),sg.Combo(values=unique_Area_list, key='-OPTION-', pad=(10,10), size=(30, 20), font=font),sg.Text('Choose the Category of Foodplace : ', font=font),sg.Combo(values=unique_cat_list, key='-OPTION2-', pad=(10,10), size=(30, 20), font=font)],
    [sg.Text( font=font)],
    [sg.Button('Export Map', key='-EXPORT-MAP-', size=(15, 2),button_color=('white', 'orange'),font=font,border_width=0),sg.Button('Export Filtered Dataset', key='-EXPORT-FILTERED-', size=(20, 2), font=font,button_color=('white', 'orange'),border_width=0)],
    [],
    [sg.Text( font=font)],
    [sg.Button('Ok', size=(3, 2), font=font,border_width=0), sg.Button('Cancel', size=(6, 2), font=font,border_width=0)],
    [],
]

window = sg.Window('Foodplaces in Singapore', layout, size=(1000,350),element_justification='center', resizable=True, finalize=True)
temp_file_name= None
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Cancel':
        if temp_file_name is not None:
            os.remove(temp_file_name)
        break
        
    if event == '-VIEW-ALL-':
        temp_file_name=plotmap('','')
        
    elif event == '-VIEW-DIAGRAMS-':
        print('View Dataset diagrams')


    elif event == '-EXPORT-':
        filename = sg.popup_get_file('Select a file to save to', save_as=True, file_types=(("CSV Files", "*.csv"),))
        if filename:
            df.to_csv(filename, index=False)


    elif event == 'Ok' :
        value1 = values['-OPTION-']
        value2 = values['-OPTION2-']
        temp_file_name = plotmap(value1, value2)
    
    elif event == '-EXPORT-MAP-':
        if temp_file_name is not None:
            destination = sg.popup_get_file('Select a file to save the map HTML', save_as=True, file_types=(("HTML Files", "*.html"),))
            if destination:
                shutil.copy(temp_file_name, destination)

    elif event == '-EXPORT-FILTERED-':
        value1 = values['-OPTION-']
        value2 = values['-OPTION2-']
        if value1!='':
            filtered_df = df_data.loc[df_data['Sub Area'] == value1]
        else: 
            filtered_df=df_data
        if value2!= '':
            filtered_df = filtered_df.loc[filtered_df['Category'] == value2]
        else :
            filtered_df=filtered_df
        if value1!='' or value2!='': 
            destination = sg.popup_get_file('Select a file to save the filtered dataset CSV', save_as=True, file_types=(("CSV Files", "*.csv"),))
            if destination:
                filtered_df.to_csv(destination, index=False)
        


# Close the PySimpleGUI window
window.close()


