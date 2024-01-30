import PySimpleGUI as sg
import webbrowser


sg.theme('DarkAmber')  # Add a touch of color



layout = [
    [sg.Text('What would you like to do today?')],
    [sg.Text('Choose one of the following options : ')],
    [],
    [sg.Button('View all food places', key='-VIEW-ALL-', size=(30, 2), pad=(10,10)), sg.Button('View Dataset diagrams', key='-VIEW-DIAGRAMS-', pad=(10,10), size=(30, 2))],
    [],
    [sg.Text('Choose the area in Singapore : '),sg.Combo(['Bukit Batok','Bukit Timah','Sengkang','Hougang'], key='-OPTION-', pad=(10,10), size=(30, 2))],
    [],
    [sg.Button('Ok', size=(5, 2)), sg.Button('Cancel', size=(5, 2))],
    [],
]

window = sg.Window('Foodplaces in Singapore', layout, size=(1000, 500),element_justification='center', resizable=True, finalize=True)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    if event == '-VIEW-ALL-':
        webbrowser.open("main/map.html")
    elif event == '-VIEW-DIAGRAMS-':
        print('View Dataset diagrams')
    elif event == '-VIEW-AREAS-':
        print('View in areas of Singapore')

# Close the PySimpleGUI window
window.close()

