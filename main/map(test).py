import folium
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