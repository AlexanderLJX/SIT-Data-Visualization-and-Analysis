
##################### imported modules #####################

import PySimpleGUI as sg
import os
import shutil
from functions import plotmap , readfile ,piechart,bargraph
import threading

def generate_map_thread(window, value1, value2, df_data):
    global temp_file_name
    temp_file_name = plotmap(value1, value2, df_data)  # Call your long-running function
    window.write_event_value('-MAP-GENERATED-', None)  # Signal the GUI thread that the task is done


df_data=readfile()

#find the catgory types in the csv to use the values to create a dropdown list in the GUI
unique_cat = df_data['Category'].unique()
unique_cat_list = list(map(str, unique_cat))

# find the sub area types in the csv
unique_Area = df_data['Planning Area'].unique()
unique_Area_list = list(map(str, unique_Area))

sg.theme('DarkAmber')  # Add a touch of color to the gui
#creating the gui / formatting the layout of the GUI
font = ("Arial",11)

#layout of the first tab
layout = [
    
    [sg.Text('Filter the data and see it on the map : ', font=("Arial",20))],
    [sg.Text()],
    [sg.Text('Area in Singapore : ', font=font),sg.Text(size=(16, 2)),sg.Text('Category of Foodplace : ', font=font)],
    [sg.Listbox(unique_Area_list, size=(20,10), select_mode='multiple', key='-OPTION-'),sg.Text(size=(14, 2)),sg.Listbox(values=unique_cat_list, size=(20,10), select_mode='multiple', key='-OPTION2-')],
    [sg.Text( font=font)],
    [sg.Button('Export Map', key='-EXPORT-MAP-', size=(15, 2),font=font,border_width=0),sg.Button('Export Filtered Dataset', key='-EXPORT-FILTERED-', size=(20, 2), font=font,border_width=0),sg.Button('Export Entire Dataset', key='-EXPORT-', pad=(10,10), size=(20,2), font=font),sg.Button('Show on Map', size=(15, 2), font=font,border_width=0,button_color=('white', 'green'))],
    # add map status
    [sg.Text('Map Status: ', font=font), sg.Text('', key='-MAP-STATUS-', font=font)],
    [sg.Text( font=font)],
  
]

#layout of the second tab 
layout2 = [
            [sg.Text('Display datagrams :', font=("Arial", 20))],
            [sg.Text( )],
            [sg.Text('Choose the diagram type: ', font=font),sg.Combo(values=["Pie Chart","Bar Graph"], key='-OPTION3-', pad=(10,10), size=(30, 20), font=font),sg.Text('Choose the data you would like to view : ', font=font),sg.Combo(values= ["Average Star Rating","Takeaway"] ,key='-OPTION4-', pad=(10,10), size=(30, 20), font=font)],
            [sg.Text( font=font)],
            [sg.Button('Show Diagram', key='-SHOW-DIAGRAM-', size=(15, 2), font=font,border_width=0,button_color=('white', 'green'))],
            [sg.Text( font=font)],
            
        ]

# Define the tab group with the tabs
tabgrp = [
    [sg.TabGroup([
        [sg.Tab('View Foodplaces', layout, element_justification='center',border_width=0)],
        [sg.Tab('Data Diagrams', layout2, element_justification='center', border_width=0 )],
    ], tab_location='centertop')],
    [sg.Text( font=font)],
    [sg.Button('Close', size=(5,1))]
]


window = sg.Window('Foodplaces in Singapore', tabgrp, size=(1200,550),element_justification='center', resizable=True,no_titlebar=False,grab_anywhere=True, finalize=True)


temp_file_name= None
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Close':
        if temp_file_name is not None:
            os.remove(temp_file_name)
        break
    
    elif event == '-VIEW-ALL-':
        #viewing the map without any filters
        temp_file_name=plotmap('','',df_data)

    elif event == '-EXPORT-':
        #exporting the full dataset
        filename = sg.popup_get_file('Select a file to save to', save_as=True, file_types=(("CSV Files", "*.csv")))
        if filename:
            df_data.to_csv(filename, index=False)

    elif event == 'Show on Map' :
        # Update GUI to show "generating..." message
        window['-MAP-STATUS-'].update('Generating...')
        #view the map with the Category of restaurant or the sub area that it is in
        value1 = values['-OPTION-']
        value2 = values['-OPTION2-']
        threading.Thread(target=generate_map_thread, args=(window, value1, value2, df_data), daemon=True).start()

    elif event == '-MAP-GENERATED-':
        # Update GUI after the map is generated, e.g., display a message or update the map view
        window['-MAP-STATUS-'].update('Map generated successfully!')
    
    elif event == '-EXPORT-MAP-':
        #exporting of the map 
        if temp_file_name is not None:
            destination = sg.popup_get_file('Select a file to save the map HTML', save_as=True, file_types=(("HTML Files", "*.html"),))
            if destination:
                shutil.copy(temp_file_name, destination)

    elif event == '-EXPORT-FILTERED-':
        #exporting of the filtered dataset
        value1 = values['-OPTION-']
        value2 = values['-OPTION2-']
        if value1!='':
            filtered_df = df_data.loc[df_data['Planning Area'] == value1]
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




    elif event== '-SHOW-DIAGRAM-' and values["-OPTION3-"]=="Pie Chart":
        piechart()
    elif event== '-SHOW-DIAGRAM-' and values["-OPTION3-"]=="Bar Graph":
        bargraph()   


# Close the PySimpleGUI window
window.close()


