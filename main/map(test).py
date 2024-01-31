import folium
import pandas as pd 

import folium
from branca.element import Figure



df_data=pd.read_csv('main/modified_data.csv')

fig=Figure(width=550,height=350)
m=folium.Map(location=[1.287953, 103.851784],zoom_start=12,prefer_canvas=True)
fig.add_child(m)
coordinates=[]
for i,n in enumerate(df_data['Name']):
    a= [df_data['Name'][i],df_data['latitude'][i], df_data['longitude'][i]]
    coordinates.append(a)


from folium.plugins import MarkerCluster

# Create a marker cluster
marker_cluster = MarkerCluster().add_to(m)

# Add points to the cluster instead of the map
for c in coordinates:
    folium.Marker(location=[c[1], c[2]], popup=str(c[0]), tooltip='Click here to see restaurant').add_to(marker_cluster)


m.save("main/map.html")