
##################### imported modules #####################

import PySimpleGUI as sg
import os
import shutil
from functions import readfile, piechart, bargraph, filter_df, filter_df_json, plotmap, plotmap_3d, plotmap_with_animation
import threading
from gpt import generate_filter
from data_visualizer import plot_distribution, plot_hexbin, plot_linear_regression

# long-running function
def generate_map_thread(window, df_data, plot_function, planning_area, category, filter_json):
    global temp_file_name
    if filter_json is not None and filter_json != "":
        filtered_df = filter_df_json(filter_json, df_data)
    else:
        filtered_df = filter_df(planning_area, category, df_data)
    
    if plot_function == "plotmap_3d":
        temp_file_name = plotmap_3d(filtered_df)
    elif plot_function == "plotmap_with_animation":
        temp_file_name = plotmap_with_animation(filtered_df)
    else: # else is plotmap
        temp_file_name = plotmap(filtered_df)  

    window.write_event_value('-MAP-GENERATED-', None)  # Signal the GUI thread that the task is done

def generate_filter_thread(window, query):
    filter_json = generate_filter(query)
    # Update the GUI with the generated filter
    window.write_event_value('-FILTER-GENERATED-', filter_json)  # Signal the GUI thread that the task is done


df_data=readfile()
filter_json = None

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
    [
        # add text for the description of the input box
        sg.Text('Natural Language query: ', font=font),
        # add a text box for a user query input
        sg.InputText(default_text='Filter out restaurants that are not LGBTQ!', key='-USER-QUERY-', font=font),
        # add a button to submit the query
        sg.Button('Generate', key='-SUBMIT-QUERY-', size=(10, 1), font=font,border_width=0),
    ],
    [sg.Text()],
    [
        # add text for the description of the input box
        sg.Text('JSON Filter: ', font=font),
        # add a text box for a user query input
        sg.InputText(default_text='', key='-FILTER-')
    ],
    [sg.Text()],
    [
        sg.Text('Area in Singapore : ', font=font),
        sg.Text(size=(16, 2)),
        sg.Text('Category of Foodplace : ', font=font)
    ],
    [
        sg.Listbox(unique_Area_list, size=(20,10), select_mode='multiple', key='-OPTION-'),
        sg.Text(size=(14, 2)),
        sg.Listbox(values=unique_cat_list, size=(20,10), select_mode='multiple', key='-OPTION2-')
    ],
    [sg.Text( font=font)],
    [
        sg.Button('Export Map', key='-EXPORT-MAP-', size=(15, 2),font=font,border_width=0), 
        sg.Button('Export Filtered Dataset', key='-EXPORT-FILTERED-', size=(20, 2), font=font,border_width=0),
        sg.Button('Export Entire Dataset', key='-EXPORT-', pad=(10,10), size=(20,2), font=font),
    ],
    [
        sg.Button('Show on Map', size=(15, 2), font=font,border_width=0,button_color=('white', 'green')),
        sg.Button('Show on 3D Map', size=(15, 2), font=font,border_width=0,button_color=('white', 'green')),
        sg.Button('Show on Animated Map', size=(20, 2), font=font,border_width=0,button_color=('white', 'green')),
    ],
    # add map status
    [sg.Text('', key='-STATUS-', font=font)],
    [sg.Text( font=font)],
]

#layout of the second tab 
layout2 = [
            [sg.Text('Display datagrams :', font=("Arial", 20))],
            [sg.Text( )],
            [
                sg.Text('Choose the diagram type: ', font=font),
                sg.Combo(values=["Pie Chart","Bar Graph"], key='-OPTION3-', pad=(10,10), size=(30, 20), font=font),
                sg.Text('Choose the data you would like to view : ', font=font),
                sg.Combo(values= ["Average Star Rating","Takeaway"] ,key='-OPTION4-', pad=(10,10), size=(30, 20), font=font)
            ],
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


window = sg.Window('Foodplaces in Singapore', tabgrp, size=(1200,650),element_justification='center', resizable=True,no_titlebar=False,grab_anywhere=True, finalize=True)


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
        
    elif event== '-SHOW-DIAGRAM-' and values["-OPTION3-"]=="Pie Chart":
        piechart()
    elif event== '-SHOW-DIAGRAM-' and values["-OPTION3-"]=="Bar Graph":
        plot_distribution(values["-OPTION4-"],df_data)

    elif event == '-EXPORT-':
        # exporting the full dataset
        filename = sg.popup_get_file('Select a file to save to', save_as=True, file_types=(("CSV Files", "*.csv"),))
        if filename:
            df_data.to_csv(filename, index=False)

    elif event == '-SUBMIT-QUERY-':
        # Update GUI to show "generating..." message
        window['-STATUS-'].update('Generating filter...')
        # view the map with the Category of restaurant or the sub area that it is in
        query = values['-USER-QUERY-']
        threading.Thread(target=generate_filter_thread, args=(window, query), daemon=True).start()

    elif event == '-FILTER-GENERATED-':
        # Update the -FILTER- text box with the generated filter
        filter_json = values[event]  # This accesses the event value for '-FILTER-GENERATED-'
        if filter_json is not None:
            window['-FILTER-'].update(filter_json)
        # Update GUI after the filter is generated, e.g., display a message or update the map view
        window['-STATUS-'].update('Filter generated successfully!')


    elif event == 'Show on Map' :
        # Update GUI to show "generating..." message
        window['-STATUS-'].update('Generating...')
        # view the map with the Category of restaurant or the sub area that it is in
        planning_area = values['-OPTION-']
        category = values['-OPTION2-']
        # get text in the filter box -FILTER-
        filter_json = values['-FILTER-']
        threading.Thread(target=generate_map_thread, args=(window, df_data, "plotmap", planning_area, category, filter_json), daemon=True).start()

    elif event == 'Show on 3D Map' :
        # Update GUI to show "generating..." message
        window['-STATUS-'].update('Generating...')
        # view the map with the Category of restaurant or the sub area that it is in
        planning_area = values['-OPTION-']
        category = values['-OPTION2-']
        # get text in the filter box -FILTER-
        filter_json = values['-FILTER-']
        threading.Thread(target=generate_map_thread, args=(window, df_data, "plotmap_3d", planning_area, category, filter_json), daemon=True).start()
    
    elif event == 'Show on Animated Map' :
        # Update GUI to show "generating..." message
        window['-STATUS-'].update('Generating...')
        # view the map with the Category of restaurant or the sub area that it is in
        planning_area = values['-OPTION-']
        category = values['-OPTION2-']
        # get text in the filter box -FILTER-
        filter_json = values['-FILTER-']
        threading.Thread(target=generate_map_thread, args=(window, df_data, "plotmap_with_animation", planning_area, category, filter_json), daemon=True).start()

    elif event == '-MAP-GENERATED-':
        # Update GUI after the map is generated, e.g., display a message or update the map view
        window['-STATUS-'].update('Map generated successfully!')
    
    elif event == '-EXPORT-MAP-':
        #exporting of the map
        if temp_file_name is not None:
            destination = sg.popup_get_file('Select a file to save the map HTML', save_as=True, file_types=(("HTML Files", "*.html"),))
            if destination:
                shutil.copy(temp_file_name, destination)
                # set status
                window['-STATUS-'].update('Map exported successfully!')
            else:
                # set status to error
                window['-STATUS-'].update('Error: No file selected')
        else:
            # set status to error
            window['-STATUS-'].update('Error: Map not generated yet!')

    elif event == '-EXPORT-FILTERED-':
        value1 = values['-OPTION-']
        value2 = values['-OPTION2-']
    
    # If there are any selected areas or categories, filter the dataframe accordingly
        if value1 or value2:
            # Use the 'isin' method to filter based on multiple values
            if value1:
                filtered_df = df_data.loc[df_data['Planning Area'].isin(value1)]
            else:
                filtered_df = df_data

            if value2:
                # If value2 is not empty, filter by category
                filtered_df = filtered_df.loc[filtered_df['Category'].isin(value2)]

            # Save the filtered dataframe to a CSV file
            destination = sg.popup_get_file('Select a file to save the filtered dataset CSV', save_as=True, file_types=(('CSV Files', '*.csv'),))
            if destination:
                filtered_df.to_csv(destination, index=False)
        else:
            window['-STATUS-'].update('Error: No filters applied')
        


# Close the PySimpleGUI window
window.close()


