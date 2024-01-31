import PySimpleGUI as sg
import webbrowser
import pandas as pd
import folium
from branca.element import Figure



df_data=pd.read_csv('main/modified_data.csv')

fig=Figure(width=550,height=350)
m=folium.Map(location=[1.287953, 103.851784],zoom_start=12)
fig.add_child(m)
coordinates=[]
for i,n in enumerate(df_data['Name']):
    a= [df_data['Name'][i],df_data['latitude'][i], df_data['longitude'][i]]
    coordinates.append(a)



for c in coordinates:
    rest=c[0]
    lon=c[1]
    lat=c[2]
    folium.Marker(location=[lon, lat],popup=str(rest),tooltip='Click here to see restaurant').add_to(m)

m.save("main/map.html")






sg.theme('DarkAmber')  # Add a touch of color

# Read data from the file
df = pd.read_csv('main/scraped_data_food.csv')

layout = [
    [sg.Text('What would you like to do today?')],
    [sg.Text('Choose one of the following options : ')],
    [],
    [sg.Button('View all food places', key='-VIEW-ALL-', size=(30, 2), pad=(10,10)), sg.Button('View Dataset diagrams', key='-VIEW-DIAGRAMS-', pad=(10,10), size=(30, 2)), sg.Button('Export the Dataset', key='-EXPORT-', pad=(10,10), size=(30, 2))],
    [],
    [sg.Text('Choose the area in Singapore : '),sg.Combo(['Bukit Batok','Bukit Timah','Sengkang','Hougang'], key='-OPTION-', pad=(10,10), size=(30, 2))],
    [],
    [sg.Button('Ok', size=(5, 2)), sg.Button('Cancel', size=(5, 2))],
    [],
]

window = sg.Window('Foodplaces in Singapore', layout, size=(1000, 300),element_justification='center', resizable=True, finalize=True)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
        
    if event == '-VIEW-ALL-':
        webbrowser.open(r"main\map.html")
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

