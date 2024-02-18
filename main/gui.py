
##################### imported modules #####################

import PySimpleGUI as sg
import os
import shutil
from functions import readfile, validate_filter_json, validate_plot_json, filter_df, filter_df_json, plotmap, plotmap_3d, plotmap_with_animation,plotmap_with_heat
import threading
from gpt import generate_filter, generate_plot_json
from data_visualizer import plot_distribution, plot_hexbin, plot_scatter, plot_line_chart, plot_bar_chart, plot_pie_chart
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import matplotlib.pyplot as plt
import constants
import webbrowser
import logging

# long-running function
def generate_map_thread(window, df_data, plot_function, planning_area, category, filter_json):
    try:
        global temp_file_name
        if filter_json is not None and filter_json != "":
            filtered_df = filter_df_json(filter_json, df_data)
        else:
            filtered_df = filter_df(planning_area, category, df_data)
        
        if plot_function == "plotmap_3d":
            temp_file_name = plotmap_3d(filtered_df)
        elif plot_function == "plotmap_with_animation":
            temp_file_name = plotmap_with_animation(filtered_df)
        elif plot_function =="plotmap_with_heat":
            temp_file_name= plotmap_with_heat(filtered_df)
        else: # else is plotmap
            temp_file_name = plotmap(filtered_df)  

        window.write_event_value('-MAP-GENERATED-', None)  # Signal the GUI thread that the task is done
    except Exception as e:
        logging.exception("Exception occurred in generate_map_thread")
        window.write_event_value('-MAP-FAILED-', None)

def generate_filter_thread(window, query):
    filter_json = generate_filter(query)
    # Update the GUI with the generated filter
    window.write_event_value('-FILTER-GENERATED-', filter_json)  # Signal the GUI thread that the task is done

def generate_plot_json_thread(window, query):
    plot_json = generate_plot_json(query)
    # Update the GUI with the generated filter
    window.write_event_value('-PLOT-JSON-GENERATED-', plot_json)  # Signal the GUI thread that the task is done

def validate_json_thread(window, json_str):
    global validating_json
    validating_json = True
    validation_result = validate_filter_json(json_str)
    window.write_event_value('-JSON-VALIDATED-', validation_result)
    validating_json = False

def validate_json_plot_thread(window, json_str):
    global validating_plot_json
    validating_plot_json = True
    validation_result = validate_plot_json(json_str)
    window.write_event_value('-PLOT-JSON-VALIDATED-', validation_result)
    validating_plot_json = False

def plot_thread(window, plot_dict, df, plot_on_canvas, filter_json=None):
    try:
        global canvas_figure
        if plot_dict["plot"] == "pie chart":
            canvas_figure = plot_pie_chart(plot_dict["feature1"], df)
        elif plot_dict["plot"] == "bar chart":
            canvas_figure = plot_bar_chart(plot_dict["feature1"], plot_dict["feature2"] if "feature2" in plot_dict else None, df, filter_json)
        elif plot_dict["plot"] == "line chart":
            canvas_figure = plot_line_chart(plot_dict["feature1"], plot_dict["feature2"], df)
        elif plot_dict["plot"] == "scatter":
            canvas_figure = plot_scatter(plot_dict["feature1"], plot_dict["feature2"], df)
        elif plot_dict["plot"] == "hexbin":
            canvas_figure = plot_hexbin(plot_dict["feature1"], plot_dict["feature2"], df)
        elif plot_dict["plot"] == "distribution":
            canvas_figure = plot_distribution(plot_dict["feature1"], df)
        # set window event
        window.write_event_value('-PLOT-GENERATED-', "Plotting finished successfully!")
    except Exception as e:
        logging.exception("Exception occurred in plot_thread")
        window.write_event_value('-PLOT-FAILED-', "Error occurred while plotting")

# Function to draw matplotlib figure on PySimpleGUI Canvas
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# Below code is for the GUI

# Configure logging
logging.basicConfig(filename='gui_error.txt', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')


plt.switch_backend('agg')
df_data=readfile()
filter_json = None
json_queue_full = False
validating_json = False

json_plot_queue_full = False
validating_plot_json = False

json_train_queue_full = False
validating_train_json = False

#find the catgory types in the csv to use the values to create a dropdown list in the GUI
unique_cat = df_data['Category'].unique()
unique_cat_list = list(map(str, unique_cat))

# find the sub area types in the csv
unique_Area = df_data['Planning Area'].unique()
unique_Area_list = list(map(str, unique_Area))

sg.theme('DarkAmber')  # Add a touch of color to the gui
#creating the gui / formatting the layout of the GUI
font = ("Arial",11)

default_filter_text = """"""
default_filter_query = "dinein and takeaway and region is central and top 10 on bayesian rating"

#layout of the first tab
layout = [
    
    [sg.Text('Filter the data and see it on the map : ', font=("Arial",20))],
    [sg.Text()],
    [
        # add text for the description of the input box
        sg.Text('Natural Language query: ', font=font),
        # add a text box for a user query input
        sg.Multiline(size=(50, 3), default_text=default_filter_query, key='-USER-QUERY-', font=font),
        # add a button to submit the query
        sg.Button('Generate', key='-SUBMIT-QUERY-', size=(10, 1), font=font,border_width=0),
    ],
    [
        # add text for the description of the input box
        sg.Text('JSON Filter: ', font=font),
        # add a text box for a user query input
        sg.Multiline(size=(50, 5), default_text=default_filter_text, key='-FILTER-', enable_events=True),
        # add text displaying json validation
        sg.Text('', size=(15, 1), key='-JSON-STATUS-')
    ],
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
    [
        sg.Button('Export Map', key='-EXPORT-MAP-', size=(15, 2),font=font,border_width=0), 
        sg.Button('Export Filtered Dataset', key='-EXPORT-FILTERED-', size=(20, 2), font=font,border_width=0),
        sg.Button('Export Entire Dataset', key='-EXPORT-', pad=(10,10), size=(20,2), font=font),
    ],
    [
        sg.Button('Show on Map', size=(15, 2), font=font,border_width=0,button_color=('white', 'green')),
        sg.Button('Show on 3D Map', size=(15, 2), font=font,border_width=0,button_color=('white', 'green')),
        sg.Button('Show on Animated Map', size=(20, 2), font=font,border_width=0,button_color=('white', 'green')),
        sg.Button('Show on Heat Map', size=(15, 2), font=font,border_width=0,button_color=('white', 'green')),
    ],
    # add map status
    [sg.Text('', key='-STATUS-', font=font)],
    [sg.Text( font=font)],
]




#layout of the second tab 
layout2 = [
            [sg.Text('Display datagrams :', font=("Arial", 20))],
            [
                # add text for the description of the input box
                sg.Text('Natural Language query: ', font=font),
                # add a text box for a user query input
                sg.Multiline(size=(50, 3), default_text='Plot the relationship between number of reviews and star rating!', key='-PLOT-QUERY-', font=font),
                # add a button to submit the query
                sg.Button('Generate', key='-SUBMIT-PLOT-QUERY-', size=(10, 1), font=font,border_width=0),
            ],
            [
                # add text for the description of the input box
                sg.Text('Plot JSON: ', font=font),
                # add a text box for a user query input
                sg.Multiline(size=(50, 5), default_text=constants.DEFAULT_PLOT_JSON, key='-PLOT-JSON-', enable_events=True),
                # add text displaying json validation
                sg.Text('', size=(15, 1), key='-PLOT-JSON-STATUS-'),
            ],
            # [
            #     sg.Text('Choose the diagram type: ', font=font),
            #     sg.Combo(values=["Pie Chart","Bar Graph"], key='-OPTION3-', pad=(10,10), size=(30, 20), font=font),
            #     sg.Text('Choose the data you would like to view : ', font=font),
            #     sg.Combo(values= ["Average Star Rating","Takeaway"] ,key='-OPTION4-', pad=(10,10), size=(30, 20), font=font)
            # ],
            [
                sg.Button('Show Diagram', key='-SHOW-DIAGRAM-', size=(15, 2), font=font,border_width=0,button_color=('white', 'green')),
                # add a checkbox to apply the filter to the diagram
                sg.Checkbox('Apply filter to diagram', key='-APPLY-FILTER-', font=font),  
                # add a checkbox to clear the previous plt on the canvas
                sg.Checkbox('Clear previous plot', key='-CLEAR-PLOT-', font=font), 
                # create a checkbox to show the diagram on the canvas
                # sg.Checkbox('Show plot in GUI', key='-SHOW-ON-CANVAS-', font=font),
            ],
            [sg.Text('', key='-PLOT-STATUS-', font=font)],
            [sg.Canvas(key='-CANVAS-')],
        ]

layout3 = [
            [sg.Text('Train ML models:', font=("Arial", 20))],
            [sg.Text( )],
            [
                # add text for the description of the input box
                sg.Text('Natural Language query: ', font=font),
                # add a text box for a user query input
                sg.Multiline(size=(50, 3), default_text='make a model to visualize if there are any anomalies in the for categories.', key='-TRAIN-QUERY-', font=font),
                # add a button to submit the query
                sg.Button('Generate', key='-SUBMIT-TRAIN-QUERY-', size=(10, 1), font=font,border_width=0),
            ],
            [
                # add text for the description of the input box
                sg.Text('JSON Arguments: ', font=font),
                # add a text box for a user query input
                sg.Multiline(size=(50, 5), default_text='', key='-TRAIN-JSON-', enable_events=True),
                # add text displaying json validation
                sg.Text('', size=(15, 1), key='-TRAIN-JSON-STATUS-')
            ],
            [
                sg.Button('Train & Predict', key='-TRAIN-AND-PREDICT-', size=(15, 2), font=font,border_width=0,button_color=('white', 'green')),
            ],
            [sg.Text('', key='-PRED-STATUS-', font=font)],
            [sg.Text( font=font)],
        ]

# Define the layout for the Help tab
help_tab_layout = [
    [sg.Text('How to Use This Application', font=("Arial", 20))],
    [sg.Text('1. Start by selecting a category or area you are interested in.', font=font)],
    [sg.Text('2. Use the "Generate" button to apply filters based on your query.', font=font)],
    [sg.Text('3. Explore the different visualization tabs to see the data in various forms.', font=font)],
    [sg.Text('For detailed documentation, visit ', font=font), sg.Text('https://github.com/AlexanderLJX/SIT-Data-Visualization-and-Analysis', font=('Arial', 10, 'underline'), text_color='blue', key='-HELP-LINK-', enable_events=True)]
]

# Define the tab group with the tabs
tabgrp = [
    [sg.TabGroup([
        [sg.Tab('View Foodplaces', layout, element_justification='center',border_width=0)],
        [sg.Tab('Data Diagrams', layout2, element_justification='center', border_width=0 )],
        [sg.Tab('Train ML Models', layout3, element_justification='center', border_width=0 )],
        [sg.Tab('Help', help_tab_layout, element_justification='center', border_width=0)]
    ], tab_location='centertop')],
    [sg.Text( font=font)],
    [sg.Button('Close', size=(5,1))]
]


window = sg.Window('Foodplaces in Singapore', tabgrp, size=(1200,750),element_justification='center', resizable=True,no_titlebar=False,grab_anywhere=True, finalize=True)


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
        
    elif event== '-SHOW-DIAGRAM-':
        # show plotting diagram on the plot status
        window['-PLOT-STATUS-'].update('Plotting...')
        # diagram = values["-OPTION3-"]
        # get the json from the plot json box
        plot_json = values['-PLOT-JSON-']
        # if plot status is valid, then plot the diagram
        if window['-PLOT-JSON-STATUS-'].get() == 'Valid JSON':
            # convert the json to a dictionary
            plot_dict = json.loads(plot_json)
            # plot_on_canvas = values["-SHOW-ON-CANVAS-"] # True if checked, False if unchecked
            plot_on_canvas = True
            # check if the clear plot checkbox is checked
            if values["-CLEAR-PLOT-"]:
                plt.clf()
            # check filter status
            filter_json_status = window['-JSON-STATUS-'].get()
            if values['-APPLY-FILTER-'] and filter_json_status == "Valid JSON":
                filter_json = values['-FILTER-']
                filtered_df = filter_df_json(filter_json, df_data)
                # json load
                filter_json = json.loads(filter_json)
                threading.Thread(target=plot_thread, args=(window, plot_dict, filtered_df, plot_on_canvas, filter_json), daemon=True).start()
            else:
                threading.Thread(target=plot_thread, args=(window, plot_dict, df_data, plot_on_canvas), daemon=True).start()
        else:
            # set status to error
            window['-PLOT-STATUS-'].update('Error: Invalid JSON filter')

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
        # validate the json
        threading.Thread(target=validate_json_thread, args=(window, filter_json), daemon=True).start()
        
    elif event == '-FILTER-' or (json_queue_full and not validating_json):  # Event triggered when the JSON filter text changes
        if validating_json:
            json_queue_full = True
        else:
            json_queue_full = False
            filter_json = values['-FILTER-']
            # Update GUI to show "validating..." message next to the JSON filter input box
            window['-JSON-STATUS-'].update('Validating...')
            # Start the JSON validation in a new thread to keep the GUI responsive
            threading.Thread(target=validate_json_thread, args=(window, filter_json), daemon=True).start()

    elif event == '-JSON-VALIDATED-':
        validation_result = values[event]  # This accesses the event value for '-JSON-VALIDATED-'
        window['-JSON-STATUS-'].update(validation_result)

    elif event == '-SUBMIT-PLOT-QUERY-':
        # Update GUI to show "generating..." message
        window['-PLOT-STATUS-'].update('Generating plot JSON...')
        # view the map with the Category of restaurant or the sub area that it is in
        query = values['-PLOT-QUERY-']
        threading.Thread(target=generate_plot_json_thread, args=(window, query), daemon=True).start()

    elif event == '-PLOT-JSON-GENERATED-':
        # Update the -FILTER- text box with the generated filter
        plot_json = values[event]  # This accesses the event value for '-PLOT-JSON-GENERATED-'
        if plot_json is not None:
            window['-PLOT-JSON-'].update(plot_json)
        # Update GUI after the filter is generated, e.g., display a message or update the map view
        window['-PLOT-STATUS-'].update('Plot JSON generated successfully!')
        # validate the json
        threading.Thread(target=validate_json_plot_thread, args=(window, plot_json), daemon=True).start()

    elif event == '-PLOT-JSON-' or (json_plot_queue_full and not validating_plot_json):  # Event triggered when the plot JSON text changes
        if validating_plot_json:
            json_plot_queue_full = True
        else:
            json_plot_queue_full = False
            filter_json = values['-PLOT-JSON-']
            # Update GUI to show "validating..." message next to the JSON filter input box
            window['-PLOT-JSON-STATUS-'].update('Validating...')
            # Start the JSON validation in a new thread to keep the GUI responsive
            threading.Thread(target=validate_json_plot_thread, args=(window, filter_json), daemon=True).start()

    elif event == '-PLOT-JSON-VALIDATED-':
        validation_result = values[event]
        window['-PLOT-JSON-STATUS-'].update(validation_result)

    elif event == "-PLOT-GENERATED-":
        # update plot status
        window['-PLOT-STATUS-'].update(values[event])
        # Remove previous drawings
        canvas_elem = window['-CANVAS-']
        canvas = canvas_elem.TKCanvas
        for child in canvas.winfo_children():
            child.destroy()
        if plot_on_canvas:
            # Draw the figure on the canvas
            # Draw new figure
            draw_figure(canvas, canvas_figure)


    elif event == 'Show on Map' :
        # check that the text of  json status is valid
        if window['-JSON-STATUS-'].get() == 'Valid JSON':
            # Update GUI to show "generating..." message
            window['-STATUS-'].update('Generating...')
            # view the map with the Category of restaurant or the sub area that it is in
            planning_area = values['-OPTION-']
            category = values['-OPTION2-']
            # get text in the filter box -FILTER-
            filter_json = values['-FILTER-']
            threading.Thread(target=generate_map_thread, args=(window, df_data, "plotmap", planning_area, category, filter_json), daemon=True).start()
        else:
            # set status to error
            window['-STATUS-'].update('Error: Invalid JSON filter')

    elif event == 'Show on 3D Map' :
        if window['-JSON-STATUS-'].get() == 'Valid JSON':
            # Update GUI to show "generating..." message
            window['-STATUS-'].update('Generating...')
            # view the map with the Category of restaurant or the sub area that it is in
            planning_area = values['-OPTION-']
            category = values['-OPTION2-']
            # get text in the filter box -FILTER-
            filter_json = values['-FILTER-']
            threading.Thread(target=generate_map_thread, args=(window, df_data, "plotmap_3d", planning_area, category, filter_json), daemon=True).start()
        else:
            # set status to error
            window['-STATUS-'].update('Error: Invalid JSON filter')
        
    elif event == 'Show on Animated Map' :
        if window['-JSON-STATUS-'].get() == 'Valid JSON':
            # Update GUI to show "generating..." message
            window['-STATUS-'].update('Generating...')
            # view the map with the Category of restaurant or the sub area that it is in
            planning_area = values['-OPTION-']
            category = values['-OPTION2-']
            # get text in the filter box -FILTER-
            filter_json = values['-FILTER-']
            threading.Thread(target=generate_map_thread, args=(window, df_data, "plotmap_with_animation", planning_area, category, filter_json), daemon=True).start()
        else:
            # set status to error
            window['-STATUS-'].update('Error: Invalid JSON filter')
    
    elif event == "Show on Heat Map":
        # Update GUI to show "generating..." message
        window['-STATUS-'].update('Generating...')
        planning_area = values['-OPTION-']
        category = values['-OPTION2-']
        filter_json = values['-FILTER-']
        threading.Thread(target=generate_map_thread, args=(window, df_data, "plotmap_with_heat", planning_area, category, filter_json), daemon=True).start()

    elif event == '-MAP-GENERATED-':
        window['-STATUS-'].update('Map generated successfully!')

    elif event == '-MAP-FAILED-':
        window['-STATUS-'].update('Error: Map generation failed')

    elif event == '-PLOT-FAILED-':
        window['-PLOT-STATUS-'].update(values[event])
    
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

    elif event == '-HELP-LINK-':
        webbrowser.open('https://github.com/AlexanderLJX/SIT-Data-Visualization-and-Analysis')
        


# Close the PySimpleGUI window
window.close()


