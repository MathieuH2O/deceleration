import pandas as pd
import folium
from folium.plugins import HeatMap
import osmnx as ox

df = pd.read_csv('202504-deceleration.csv', encoding='shift_jis')
df.columns = [
    "session_id", "longitude", "latitude", "zone_id", "deceleration_g",
    "timestamp", "speed_kmh", "mode", "unused_1", "unused_2"
]

print("Downloading roads...")
G = ox.graph_from_place("Sakai, Osaka, Japan", network_type="drive")
edges = ox.graph_to_gdfs(G, nodes=False, edges=True)

print("Downloading stations...")
stations = ox.features_from_place(
    "Sakai, Osaka, Japan",
    tags={'railway': 'station'}
)

m = folium.Map(location=[34.5078, 135.4834], zoom_start=13)

for _, row in edges.iterrows():
    if row['geometry'].geom_type == 'LineString':
        folium.PolyLine(
            locations=[(lat, lon) for lon, lat in row['geometry'].coords],
            color='gray', weight=1, opacity=0.5
        ).add_to(m)

for _, row in stations.iterrows():
    if row.geometry.geom_type == 'Point':
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=row.get('name', 'Station'),
            icon=folium.Icon(color='blue', icon='train', prefix='fa')
        ).add_to(m)

heat_data = df[['latitude', 'longitude', 'deceleration_g']].values.tolist()
HeatMap(heat_data, radius=10, blur=15, max_zoom=1).add_to(m)

m.save('sakai_deceleration_osm_heatmap.html')

print("Map saved. Open 'sakai_deceleration_osm_heatmap.html' in your browser.")
