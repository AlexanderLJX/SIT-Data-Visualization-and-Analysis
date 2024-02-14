
##################### imported modules ######################

import PySimpleGUI as sg
import os
import shutil
from functions import plotmap , readfile



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
layout = [
    
    [sg.Text('What would you like to do today?', font=font)],
    [sg.Text()],
    [sg.Text('Choose one of the following options : ', font=font)],
    [],
    [sg.Button('View all food places', key='-VIEW-ALL-', size=(30, 2), pad=(10,10)), sg.Button('View Dataset diagrams', key='-VIEW-DIAGRAMS-', pad=(10,10), size=(30, 2)), sg.Button('Export Dataset', key='-EXPORT-', pad=(10,10), size=(30,2), font=font)],
    [sg.Text()],
    [sg.Text('Filter the data and see it on the map : ', font=font)],
    [],
    [sg.Text('Choose the area in Singapore : ', font=font),sg.Combo(values=unique_Area_list, key='-OPTION-', pad=(10,10), size=(30, 20), font=font),sg.Text('Choose the Category of Foodplace : ', font=font),sg.Combo(values=unique_cat_list, key='-OPTION2-', pad=(10,10), size=(30, 20), font=font)],
    [sg.Text( font=font)],
    [sg.Button('Export Map', key='-EXPORT-MAP-', size=(15, 2),font=font,border_width=0),sg.Button('Export Filtered Dataset', key='-EXPORT-FILTERED-', size=(20, 2), font=font,border_width=0),sg.Button('Show on Map', size=(15, 2), font=font,border_width=0,button_color=('white', 'green')),],
    [],
    [sg.Text( font=font)],
    [ sg.Button('Close', size=(6, 2), font=font,border_width=0,button_color=('white', 'maroon'))],
    [],
]

window = sg.Window('Foodplaces in Singapore', layout, size=(1000,400),element_justification='center', resizable=True, finalize=True)
temp_file_name= None

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Close':
        if temp_file_name is not None:
            os.remove(temp_file_name)
        break
        
    if event == '-VIEW-ALL-':
        #viewing the map without any filters
        temp_file_name=plotmap('','',df_data)
        
    elif event == '-VIEW-DIAGRAMS-':
        # adding the viewing of the dataset diagrams that others supposed to create 
        sg.popup('View Dataset Diagrams', 'This feature is currently under development.')


    elif event == '-EXPORT-':
        #exporting the full dataset
        filename = sg.popup_get_file('Select a file to save to', save_as=True, file_types=(("CSV Files", "*.csv"),))
        if filename:
            df_data.to_csv(filename, index=False)


    elif event == 'Show on Map' :
        #view the map with the Category of restaurant or the sub area that it is in
        value1 = values['-OPTION-']
        value2 = values['-OPTION2-']
        temp_file_name = plotmap(value1,value2,df_data)

    
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
        


# Close the PySimpleGUI window
window.close()


