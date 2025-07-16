import pandas as pd
import folium
import osmnx as ox

# Load deceleration data
df = pd.read_csv('202504-deceleration.csv', encoding='shift_jis')
df.columns = [
    "session_id", "longitude", "latitude", "zone_id", "deceleration_g",
    "timestamp", "speed_kmh", "mode", "unused_1", "unused_2"
]

# Download road network
print("Downloading roads...")
G = ox.graph_from_place("Sakai, Osaka, Japan", network_type="drive")
edges = ox.graph_to_gdfs(G, nodes=False, edges=True)

# Download railway stations
print("Downloading stations...")
stations = ox.features_from_place(
    "Sakai, Osaka, Japan",
    tags={'railway': 'station'}
)

# Filter for high deceleration points
high_dec = df[df['deceleration_g'] > 0.5]  # adjustable threshold

# Create base map
m = folium.Map(location=[34.5078, 135.4834], zoom_start=13)

folium.TileLayer(
    tiles='https://stamen-tiles.a.ssl.fastly.net/terrain/{z}/{x}/{y}.jpg',
    attr='Map tiles by Stamen Design, CC BY 3.0 — Map data © OpenStreetMap contributors',
    name='Stamen Terrain',
    overlay=False,
    control=True
).add_to(m)

folium.LayerControl().add_to(m)

# Add roads
for _, row in edges.iterrows():
    if row['geometry'].geom_type == 'LineString':
        folium.PolyLine(
            locations=[(lat, lon) for lon, lat in row['geometry'].coords],
            color='gray', weight=1, opacity=0.5
        ).add_to(m)

# Add stations
for _, row in stations.iterrows():
    if row.geometry.geom_type == 'Point':
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=row.get('name', 'Station'),
            icon=folium.Icon(color='blue', icon='train', prefix='fa')
        ).add_to(m)

# Add high deceleration points
for _, row in high_dec.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        color='red',
        fill=True,
        fill_opacity=0.7,
        popup=f"Deceleration: {row['deceleration_g']}g"
    ).add_to(m)

# Save map
m.save('sakai_high_deceleration_points.html')
print("Map saved. Open 'sakai_high_deceleration_points.html' in your browser.")
