import pandas as pd
import folium
from folium.plugins import HeatMap

df = pd.read_csv('202504-deceleration.csv', encoding='shift_jis')

df.columns = [
    "session_id", "longitude", "latitude", "zone_id", "deceleration_g",
    "timestamp", "speed_kmh", "mode", "unused_1", "unused_2"
]
# base map centered on Sakai City
m = folium.Map(location=[34.5078, 135.4834], zoom_start=13)
heat_data = df[['latitude', 'longitude', 'deceleration_g']].values.tolist()
HeatMap(
    heat_data,
    radius=10,     # size of each point
    blur=15,       # how much to blur
    max_zoom=1,    
).add_to(m)

m.save('sakai_deceleration_heatmap.html')

print("✅ Heatmap created! Open 'sakai_deceleration_heatmap.html' in your browser.")
