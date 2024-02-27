import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('final_data.csv')


unique_coords = df[['gps latitude', 'gps longitude']].drop_duplicates()

plt.figure(figsize=(10, 6))
plt.scatter(unique_coords['gps latitude'], unique_coords['gps longitude'], s=30, color = "red",marker='^')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Unique Latitude and Longitude Points')
plt.grid(True)
plt.xticks([])
plt.yticks([])
plt.show()