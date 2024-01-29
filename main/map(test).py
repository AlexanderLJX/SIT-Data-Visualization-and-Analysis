import folium
import pandas as pd 

import folium
from branca.element import Figure



df_coordinates=pd.read_csv('main/modified_data.csv')
df_coordinates.head()













fig=Figure(width=550,height=350)


m=folium.Map(location=[1.287953, 103.851784],zoom_start=12)


fig.add_child(m)

folium.Marker(location=[1.33503545, 103.85177265],popup='Default popup Marker1',tooltip='Click here to see Popup').add_to(m)

m.save("main/map.html")