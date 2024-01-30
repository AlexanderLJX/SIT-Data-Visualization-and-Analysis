import PySimpleGUI as sg
import webbrowser


sg.theme('DarkAmber')  # Add a touch of color



layout = [
    [sg.Text('What would you like to do today?')],
    [sg.Text('Choose one of the following options : ')],
    [sg.Button('View all food places', key='-VIEW-ALL-'), sg.Button('View Dataset diagrams', key='-VIEW-DIAGRAMS-')],
    [sg.Button('View in areas of Singapore', key='-VIEW-AREAS-')],
    [sg.Button('Ok'), sg.Button('Cancel')],
]

window = sg.Window('Foodplaces in Singapore', layout, finalize=True)

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

