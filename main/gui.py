
##################### imported modules #####################

import PySimpleGUI as sg
import os
import shutil
from functions import *
from util import readfile
import threading
from gpt import *
from data_visualizer import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import matplotlib.pyplot as plt
import constants
import webbrowser
import logging

# long-running function
def generate_map_thread(window, df_data, plot_function, planning_area, category, filter_json, time_feature=None):
    try:
        global temp_file_name
        if filter_json is not None and filter_json != "":
            filtered_df = filter_df_json(filter_json, df_data)
            filtered_df = filter_df(planning_area, category, filtered_df)
        else:
            filtered_df = filter_df(planning_area, category, df_data)

        if plot_function == "plotmap_with_animation":
            temp_file_name = plotmap_with_animation(filtered_df, time_feature)
        else: # else is plotmap
            temp_file_name = plotmap(filtered_df) 


        # elif plot_function == "plotmap_3d":
        #     temp_file_name = plotmap_3d(filtered_df)
        # elif plot_function =="plotmap_with_heat":
        #     temp_file_name= plotmap_with_heat(filtered_df)
            
        window.write_event_value('-MAP-GENERATED-', None)  # Signal the GUI thread that the task is done
    except Exception as e:
        logging.exception("Exception occurred in generate_map_thread")
        window.write_event_value('-MAP-FAILED-', None)

def generate_filter_thread(window, query):
    try:
        filter_json = generate_filter(query)
    except Exception as e:
        filter_json = ""
        logging.exception("Exception occurred in generate_filter_thread")
        window.write_event_value('-FILTER-FAILED-', None)
    # Update the GUI with the generated filter
    window.write_event_value('-FILTER-GENERATED-', filter_json)  # Signal the GUI thread that the task is done

def generate_plot_json_thread(window, query):
    plot_json = generate_plot_json(query)
    # Update the GUI with the generated filter
    window.write_event_value('-PLOT-JSON-GENERATED-', plot_json)  # Signal the GUI thread that the task is done

def validate_json_thread(window, json_str):
    global validating_json
    validating_json = True
    validation_result = validate_filter_json_recursive(json_str)
    window.write_event_value('-JSON-VALIDATED-', validation_result)
    validating_json = False

def validate_json_plot_thread(window, json_str):
    global validating_plot_json
    validating_plot_json = True
    validation_result = validate_plot_json(json_str)
    window.write_event_value('-PLOT-JSON-VALIDATED-', validation_result)
    validating_plot_json = False

def validate_json_train_thread(window, json_str):
    global validating_train_json
    validating_train_json = True
    validation_result = validate_train_json(json_str)
    window.write_event_value('-TRAIN-JSON-VALIDATED-', validation_result)
    validating_train_json = False

def plot_thread(window, unfiltered_df, plot_json, filter_json_status, apply_filter, filter_json):
    df = unfiltered_df.copy()
    if apply_filter and filter_json_status == "Valid JSON" and filter_json is not None and filter_json != "":
        df = filter_df_json(filter_json, unfiltered_df)
        filter_json = json.loads(filter_json)
    # Drop String values that are "nan" based on columns feature1 and feature2 if feature2 is present
    df[plot_json["feature1"]] = df[plot_json["feature1"]].apply(lambda x: np.nan if x == "nan" or x == "NAN" else x)
    df = df.dropna(subset=[plot_json["feature1"]])
    if "feature2" in plot_json:
        df[plot_json["feature2"]] = df[plot_json["feature2"]].apply(lambda x: np.nan if x == "nan" or x == "NAN" else x)
        df = df.dropna(subset=[plot_json["feature2"]])
    try:
        global canvas_figure
        if plot_json["plot"] == "pie chart":
            canvas_figure = plot_pie_chart(plot_json["feature1"], df)
        elif plot_json["plot"] == "bar chart":
            canvas_figure = plot_bar_chart(plot_json["feature1"], plot_json["feature2"] if "feature2" in plot_json else None, df, filter_json)
        elif plot_json["plot"] == "line chart":
            canvas_figure = plot_line_chart(plot_json["feature1"], plot_json["feature2"], df)
        elif plot_json["plot"] == "scatter":
            canvas_figure = plot_scatter(plot_json["feature1"], plot_json["feature2"], df)
        elif plot_json["plot"] == "hexbin":
            canvas_figure = plot_hexbin(plot_json["feature1"], plot_json["feature2"], df)
        elif plot_json["plot"] == "distribution":
            canvas_figure = plot_distribution(plot_json["feature1"], df)
        # set window event
        window.write_event_value('-PLOT-GENERATED-', "Plotting finished successfully!")
    except Exception as e:
        logging.exception("Exception occurred in plot_thread")
        window.write_event_value('-PLOT-FAILED-', "Error occurred while plotting")

def generate_ml_train_json_thread(window, query):
    train_json = generate_ml_train_json(query)
    # Signal the GUI thread that the JSON generation is done
    window.write_event_value('-TRAIN-JSON-GENERATED-', train_json)
    

def train_and_predict_thread(window, unfiltered_df, train_json, filter_json_status, apply_filter, filter_json):
    df = unfiltered_df.copy()
    if apply_filter and filter_json_status == "Valid JSON" and filter_json is not None and filter_json != "":
        df = filter_df_json(filter_json, unfiltered_df)
        filter_json = json.loads(filter_json)
    # for each feature in features, drop String values that are "nan" based on the feature
    # TODO:
    try:
        global canvas_figure
        if train_json["model"] == "linear regression":
            canvas_figure = plot_linear_regression(train_json["features"], train_json["target"], df)
        elif train_json["model"] == "random forest":
            canvas_figure = plot_random_forest(train_json["features"], train_json["target"], df)
        elif train_json["model"] == "isolation forest":
            canvas_figure = plot_isolation_forest(train_json["features"], df)
        
        # Signal the GUI thread that the training and prediction are done
        window.write_event_value('-TRAINING-SUCCESS-', None)
    except Exception as e:
        logging.exception("Exception occurred in train_and_predict_thread")
        window.write_event_value('-TRAINING-FAILED-', None)



# Function to draw matplotlib figure on PySimpleGUI Canvas
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# Below code is for the GUI

# Configure logging
logging.basicConfig(filename='gui_error.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')


plt.switch_backend('agg')
plt.figure(figsize=(40, 40))
df_data=readfile("main/main.csv")
filter_json = None
json_queue_full = False
validating_json = False

json_plot_queue_full = False
validating_plot_json = False

json_train_queue_full = False
validating_train_json = False

#find the catgory types in the csv to use the values to create a dropdown list in the GUI
unique_cat = df_data['Category'].unique()
unique_cat_list = sorted(list(map(str, unique_cat)))

# find all time ISO8601 features in the constants.FEATURES_DATATYPES
time_features_list = [feature for feature, datatype in constants.FEATURES_DATATYPES.items() if datatype == "ISO8601"]


# find the sub area types in the csv
unique_Area = df_data['Planning Area'].unique()
unique_Area_list = sorted(list(map(str, unique_Area)))

sg.theme('DarkAmber')  # Add a touch of color to the gui
#creating the gui / formatting the layout of the GUI
font = ("Arial",11)

default_filter_text = """"""
default_filter_query = "dine in and takeaway and region is central and top 10 on bayesian rating"



#layout of the first tab
layout = [
    
    [sg.Text()],
    [sg.Text('Filtering data by Natural Language Query: ', font=("Arial",16))],
    [
        # add text for the description of the input box
        sg.Text('NLQ: ', font=font),
        # add a text box for a user query input
        sg.Multiline(size=(50, 3), default_text=default_filter_query, key='-USER-QUERY-', font=font),
        # add a button to submit the query
        sg.Button('Generate', key='-SUBMIT-QUERY-', size=(10, 1), font=font,border_width=0),
    ],
    [sg.Text(size=(5,1))],
    [
        # add text for the description of the input box
        sg.Text('JSON Filter: ', font=font),
        # add a text box for a user query input
        sg.Multiline(size=(50, 5), default_text=default_filter_text, key='-FILTER-', enable_events=True),
        # add text displaying json validation
        sg.Text('', size=(15, 1), key='-JSON-STATUS-')
    ],
    [
        sg.Button('Import Workflow', key='-IMPORT-WORKFLOW-', size=(15, 2),font=font,border_width=0),
        sg.Button('Export Workflow', key='-EXPORT-WORKFLOW-', size=(15, 2),font=font,border_width=0),
    ],
    [sg.Text(size=(10,1))],
    [sg.Text('Additional Filters:', font=("Arial",16))],
    [ 
        sg.Text('Areas in Singapore : ', font=font),
        sg.Text(size=(10, 2)),
        sg.Text('Category of Foodplaces : ', font=font),
        sg.Text(size=(9, 2)),
        sg.Text('Time Features(animated map only) : ', font=font)
    ],
    
    [   
        sg.Listbox(unique_Area_list, size=(20,6), select_mode='multiple', key='-OPTION-'),
        sg.Text(size=(14, 2)),
        sg.Listbox(values=unique_cat_list, size=(22,6), select_mode='multiple', key='-OPTION2-'),
        sg.Text(size=(14, 2)),
        sg.Listbox(values=time_features_list, size=(22,6), select_mode='single', key='-PLOT-TIME-FEATURE-')
    ],
    [sg.Text(size=(5,1))],
    [
        sg.Button('Show on Map', size=(15, 2), font=font,border_width=0,button_color=('white', 'green')),
        sg.Button('Show on Animated Map', size=(20, 2), font=font,border_width=0,button_color=('white', 'green')),
        
       
    ],
    [sg.Text(size=(5,1))],
    [
        sg.Button('Export Map', key='-EXPORT-MAP-', size=(15, 2),font=font,border_width=0), 
        sg.Button('Export Filtered Dataset', key='-EXPORT-FILTERED-', size=(20, 2), font=font,border_width=0),
        sg.Button('Export Entire Dataset', key='-EXPORT-', pad=(10,10), size=(20,2), font=font),
    ],
    # add map status
    [sg.Text('', key='-STATUS-', font=font)],
    [sg.Text( font=font)],
]




#layout of the second tab 
layout2 = [
            [sg.Text('Display datagrams :', font=("Arial", 20))],
            [sg.Text(size=(5,2))],
            [
                # add text for the description of the input box
                sg.Text('NLQ: ', font=font),
                # add a text box for a user query input
                sg.Multiline(size=(50, 3), default_text='Plot the relationship between number of reviews and star rating!', key='-PLOT-QUERY-', font=font, enable_events=True),
                # add a button to submit the query
                sg.Button('Generate', key='-SUBMIT-PLOT-QUERY-', size=(10, 1), font=font,border_width=0),
            ],
            [sg.Text(size=(5,1))],
            [
                # add text for the description of the input box
                sg.Text('Plot JSON: ', font=font),
                # add a text box for a user query input
                sg.Multiline(size=(50, 5), default_text=constants.DEFAULT_PLOT_JSON, key='-PLOT-JSON-', enable_events=True),
                # add text displaying json validation
                sg.Text('', size=(15, 1), key='-PLOT-JSON-STATUS-'),
            ],
            [sg.Text(size=(5,1))],
            [
                sg.Button('Show Diagram', key='-SHOW-DIAGRAM-', size=(15, 2), font=font,border_width=0,button_color=('white', 'green')),
                # add a checkbox to apply the filter to the diagram
                sg.Checkbox('Apply filter', key='-APPLY-FILTER-', font=font),  
                # add a checkbox to clear the previous plt on the canvas
                sg.Checkbox('Clear previous plot', key='-CLEAR-PLOT-', font=font), 
                # create a checkbox to show the diagram on the canvas
                sg.Checkbox('Plot in new window', key='-PLOT-IN-NEW-WINDOW-', font=font),
            ],
            [sg.Text('', key='-PLOT-STATUS-', font=font)],
            [sg.Canvas(key='-CANVAS-')],
        ]

layout3 = [
            [sg.Text('Train ML models:', font=("Arial", 20))],
            [
                # add text for the description of the input box
                sg.Text('Natural Language query: ', font=font),
                # add a text box for a user query input
                sg.Multiline(size=(50, 3), default_text='make a model to visualize if there are any anomalies in avg star rating.', key='-TRAIN-QUERY-', font=font),
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
                # add a checkbox to apply the filter to the diagram
                sg.Checkbox('Apply filter', key='-TRAIN-APPLY-FILTER-', font=font),  
                # add a checkbox to clear the previous plt on the canvas
                sg.Checkbox('Clear previous plot', key='-TRAIN-CLEAR-PLOT-', font=font), 
                # create a checkbox to show the diagram on the canvas
                sg.Checkbox('Plot in new window', key='-TRAIN-PLOT-IN-NEW-WINDOW-', font=font),
            ],
            [sg.Text('', key='-TRAIN-STATUS-', font=font)],
            [sg.Canvas(key='-TRAIN-CANVAS-')],
        ]

# Define the layout for the Help tab
help_tab_layout = [
    [sg.Text('Instructions', font=("Arial", 16, "underline bold")), ],
    [sg.Text(size=(5,1))],
    [sg.Text('Please visit ', font=("Arial", 12)), 
     sg.Text('https://github.com/AlexanderLJX/SIT-Data-Visualization-and-Analysis', font=('Arial', 12, 'underline'), text_color='light blue', key='-HELP-LINK-', enable_events=True),
     sg.Text('for a detailed documentation on using each of the PySimpleGUI tab.', font=("Arial", 12))]
]

# Define the tab group with the tabs
tabgrp = [
    [sg.TabGroup([
        [sg.Tab('View Foodplaces', layout, element_justification='center',border_width=0)],
        [sg.Tab('Data Diagrams', layout2, element_justification='center', border_width=0 )],
        [sg.Tab('Train ML Models', layout3, element_justification='center', border_width=0)],
        [sg.Tab('Help', help_tab_layout, element_justification='center', border_width=0)]
    ], tab_location='centertop' , size=(1100,900))],
    [sg.Text( font=font)]
]


window = sg.Window('Foodplaces in Singapore', tabgrp, size=(1250,1000),element_justification='center', resizable=True,no_titlebar=False,grab_anywhere=True, finalize=True)


temp_file_name= None

# validate json
# get value of filter json
filter_json = window['-FILTER-'].get()
threading.Thread(target=validate_json_thread, args=(window, filter_json), daemon=True).start()

# get value of plot json
plot_json = window['-PLOT-JSON-'].get()
threading.Thread(target=validate_json_plot_thread, args=(window, plot_json), daemon=True).start()

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Close':
        if temp_file_name is not None:
            os.remove(temp_file_name)
        break
    
        
    elif event== '-SHOW-DIAGRAM-':
        # show plotting diagram on the plot status
        window['-PLOT-STATUS-'].update('Plotting...')
        # diagram = values["-OPTION3-"]
        # get the json from the plot json box
        plot_json = values['-PLOT-JSON-']
        # if plot status is valid, then plot the diagram
        if window['-PLOT-JSON-STATUS-'].get() == 'Valid JSON':
            # convert the json to a dictionary
            plot_json = json.loads(plot_json)
            # check if the clear plot checkbox is checked
            if values["-CLEAR-PLOT-"]:
                plt.clf()
                plt.figure(figsize=(40, 40))
            # check filter status
            filter_json_status = window['-JSON-STATUS-'].get()
            apply_filter = values['-APPLY-FILTER-']
            filter_json = values['-FILTER-']
            threading.Thread(target=plot_thread, args=(window, df_data, plot_json, filter_json_status, apply_filter, filter_json), daemon=True).start()
        else:
            # set status to error
            window['-PLOT-STATUS-'].update('Error: Invalid JSON filter')

    elif event == '-IMPORT-WORKFLOW-':
        workflow_path = sg.popup_get_file('Select JSON workflow file', file_types=(("JSON Files", "*.json"),))
        if workflow_path and os.path.exists(workflow_path):
            # read with utf-8 encoding
            with open(workflow_path, 'r', encoding='utf-8') as f:
                workflow_json = f.read()
            # load json prettily
            workflow_json = json.loads(workflow_json)
            filter_json = json.dumps(workflow_json["filter"], indent=4)
            if filter_json == '""':
                filter_json = ""
            plot_json = json.dumps(workflow_json["plot"], indent=4)
            if plot_json == '""':
                plot_json = ""
            train_json = json.dumps(workflow_json["train"], indent=4)
            if train_json == '""':
                train_json = ""
            window['-FILTER-'].update(filter_json)
            window['-PLOT-JSON-'].update(plot_json)
            window['-TRAIN-JSON-'].update(train_json)
            threading.Thread(target=validate_json_thread, args=(window, filter_json), daemon=True).start()
            threading.Thread(target=validate_json_plot_thread, args=(window, plot_json), daemon=True).start()
            threading.Thread(target=validate_json_train_thread, args=(window, train_json), daemon=True).start()
            window['-STATUS-'].update('Successfully imported workflow!')
        else:
            # set status to error
            window['-STATUS-'].update('Error: No file selected')

    elif event == '-EXPORT-WORKFLOW-':
        try:
            json_filter = json.loads(values['-FILTER-'])
        except:
            json_filter = ""
        try:
            json_plot = json.loads(values['-PLOT-JSON-'])
        except:
            json_plot = ""
        try:
            json_train = json.loads(values['-TRAIN-JSON-'])
        except:
            json_train = ""
        workflow_json = {
            "filter": json_filter,
            "plot": json_plot,
            "train": json_train
        }
        filename = sg.popup_get_file('Select a file to save the workflow', save_as=True, file_types=(("JSON Files", "*.json"),))
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(json.dumps(workflow_json, indent=4))
            window['-STATUS-'].update('Workflow exported successfully!')
        else:
            # set status to error
            window['-STATUS-'].update('Error: No file selected')

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
        # get plot in new window checkbox value
        plot_in_new_window = values["-PLOT-IN-NEW-WINDOW-"]
        if plot_in_new_window:
            nlayout = [[sg.Canvas(key='-CANVAS-')]]
            nwindow = sg.Window('Foodplaces in Singapore', nlayout, size=(800,600),element_justification='center', resizable=True,no_titlebar=False,grab_anywhere=True, finalize=True)
            ncanvas_elem = nwindow['-CANVAS-']
            ncanvas = ncanvas_elem.TKCanvas
            figure_canvas_agg = FigureCanvasTkAgg(plt.gcf(), ncanvas)
            figure_canvas_agg.draw()
            figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=3)
        else:
            # Remove previous drawings
            canvas_elem = window['-CANVAS-']
            canvas = canvas_elem.TKCanvas
            for child in canvas.winfo_children():
                child.destroy()
            # Draw the figure on the canvas
            draw_figure(canvas, canvas_figure)

    elif event == '-SUBMIT-TRAIN-QUERY-':
        # Update GUI to show "generating..." message
        window['-TRAIN-STATUS-'].update('Generating ML JSON...')
        query = values['-TRAIN-QUERY-']
        # Logic to process query and generate JSON arguments
        threading.Thread(target=generate_ml_train_json_thread, args=(window, query), daemon=True).start()

    elif event == '-TRAIN-JSON-GENERATED-':
        train_json = values[event]  # Assuming this is the event value from your generation function
        window['-TRAIN-JSON-'].update(train_json)
        window['-TRAIN-STATUS-'].update('ML JSON generated successfully!')
        # validate the json
        threading.Thread(target=validate_json_train_thread, args=(window, train_json), daemon=True).start()

    elif event == '-TRAIN-JSON-VALIDATED-':
        validation_result = values[event]
        window['-TRAIN-JSON-STATUS-'].update(validation_result)

    elif event == '-TRAIN-JSON-' or (json_train_queue_full and not validating_train_json):  # Event triggered when the train JSON text changes
        if validating_train_json:
            json_train_queue_full = True
        else:
            json_train_queue_full = False
            train_json = values['-TRAIN-JSON-']
            # Update GUI to show "validating..." message next to the JSON filter input box
            window['-TRAIN-JSON-STATUS-'].update('Validating...')
            # Start the JSON validation in a new thread to keep the GUI responsive
            threading.Thread(target=validate_json_train_thread, args=(window, train_json), daemon=True).start()

    elif event == '-TRAIN-AND-PREDICT-':
        window['-TRAIN-STATUS-'].update('Training...')
        train_json = values['-TRAIN-JSON-']
        if window['-TRAIN-JSON-STATUS-'].get() == 'Valid JSON':
            train_json = json.loads(train_json)
            if values["-TRAIN-CLEAR-PLOT-"]:
                plt.clf()
                plt.figure(figsize=(40, 40))
            filter_json_status = window['-JSON-STATUS-'].get()
            apply_filter = values['-TRAIN-APPLY-FILTER-']
            filter_json = values['-FILTER-']
            threading.Thread(target=train_and_predict_thread, args=(window, df_data, train_json, filter_json_status, apply_filter, filter_json)).start()
        else:
            window['-TRAIN-STATUS-'].update('Error: Invalid JSON')

    elif event == '-TRAINING-SUCCESS-':
        window['-TRAIN-STATUS-'].update('Training and prediction completed successfully!')
        # get plot in new window checkbox value
        plot_in_new_window = values["-TRAIN-PLOT-IN-NEW-WINDOW-"]
        if plot_in_new_window:
            nlayout = [[sg.Canvas(key='-TRAIN-CANVAS-')]]
            nwindow = sg.Window('Foodplaces in Singapore', nlayout, size=(800,600),element_justification='center', resizable=True,no_titlebar=False,grab_anywhere=True, finalize=True)
            ncanvas_elem = nwindow['-TRAIN-CANVAS-']
            ncanvas = ncanvas_elem.TKCanvas
            figure_canvas_agg = FigureCanvasTkAgg(plt.gcf(), ncanvas)
            figure_canvas_agg.draw()
            figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=3)
        else:
            # Remove previous drawings
            canvas_elem = window['-TRAIN-CANVAS-']
            canvas = canvas_elem.TKCanvas
            for child in canvas.winfo_children():
                child.destroy()
            # Draw the figure on the canvas
            draw_figure(canvas, canvas_figure)
    elif event == '-TRAINING-FAILED-':
        window['-TRAIN-STATUS-'].update('Error during training and prediction')


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

    elif event == 'Show on Animated Map' :
        if window['-JSON-STATUS-'].get() == 'Valid JSON':
            # Update GUI to show "generating..." message
            window['-STATUS-'].update('Generating...')
            # view the map with the Category of restaurant or the sub area that it is in
            planning_area = values['-OPTION-']
            category = values['-OPTION2-']
            if values['-PLOT-TIME-FEATURE-'] == []:
                window['-STATUS-'].update('Error: No time feature selected')
                continue
            time_feature = values['-PLOT-TIME-FEATURE-'][0]
            # get text in the filter box -FILTER-
            filter_json = values['-FILTER-']
            threading.Thread(target=generate_map_thread, args=(window, df_data, "plotmap_with_animation", planning_area, category, filter_json, time_feature), daemon=True).start()
        else:
            # set status to error
            window['-STATUS-'].update('Error: Invalid JSON filter')

   
    elif event == '-MAP-GENERATED-':
        window['-STATUS-'].update('Map generated successfully!')

    elif event == '-MAP-FAILED-':
        window['-STATUS-'].update('Error: Map generation failed')

    elif event == '-PLOT-FAILED-':
        window['-PLOT-STATUS-'].update(values[event])

    elif event == '-TRAIN-FAILED-':
        window['-TRAIN-STATUS-'].update(values[event])
    
    elif event == '-EXPORT-MAP-':
        # exporting of the map
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
        planning_area = values['-OPTION-']
        category = values['-OPTION2-']
        filter_json = values['-FILTER-']
        # If there are any selected areas or categories, filter the dataframe accordingly
        if planning_area or category or filter_json != "":
            if filter_json is not None and filter_json != "":
                filtered_df = filter_df_json(filter_json, df_data)
                filtered_df = filter_df(planning_area, category, filtered_df)
            else:
                filtered_df = filter_df(planning_area, category, df_data)

            # Save the filtered dataframe to a CSV file
            destination = sg.popup_get_file('Select a file to save the filtered dataset CSV', save_as=True, file_types=(('CSV Files', '*.csv'),))
            if destination:
                filtered_df.to_csv(destination, index=False,encoding='utf-8-sig')
                window['-STATUS-'].update('Filtered dataset exported successfully!')
        else:
            window['-STATUS-'].update('Error: No filters applied')

    elif event == '-EXPORT-':
        # exporting the full dataset
        filename = sg.popup_get_file('Select a file to save to', save_as=True, file_types=(("CSV Files", "*.csv"),))
        if filename:
            try:
                df_data.to_csv(filename, index=False, encoding='utf-8-sig')
            except Exception as e:
                print(f"An error occurred while saving the file: {e}")

    elif event == '-HELP-LINK-':
        webbrowser.open('https://github.com/AlexanderLJX/SIT-Data-Visualization-and-Analysis')
        


# Close the PySimpleGUI window
window.close()


