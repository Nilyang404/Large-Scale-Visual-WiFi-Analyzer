import pandas as pd
import matplotlib.pyplot as plt

# load dataset
df = pd.read_csv('merged_released.csv')

import folium
from folium.plugins import HeatMap
import pandas as pd

data = df[df['network delay (ms)'].notnull()]
new_rows = []
for i in range(len(data) - 1):
    new_row = {
        'gps latitude': (data.iloc[i]['gps latitude'] + data.iloc[i+1]['gps latitude']) / 2,
        'gps longitude': (data.iloc[i]['gps longitude'] + data.iloc[i+1]['gps longitude']) / 2,
        'rssi': -76
    }
    new_rows.append(new_row)

# insert data
for idx, new_row in enumerate(new_rows):
    insert_idx = 2 * idx + 1
    data = pd.concat([data.iloc[:insert_idx], pd.DataFrame([new_row]), data.iloc[insert_idx:]]).reset_index(drop=True)


m = folium.Map(location=[data['gps latitude'].mean(), data['gps longitude'].mean()], zoom_start=6, radius=18)


heat_data = [[row['gps latitude'], row['gps longitude'], row['rssi']] for index, row in data.iterrows()]
HeatMap(heat_data).add_to(m)

# show map
m.save('map.html')  # save as html
