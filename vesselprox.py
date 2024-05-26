import pandas as pd
import numpy as np
from math import sin, cos, sqrt
from scipy.spatial import cKDTree
import time 

# Load data
df = pd.read_csv('sample_data.csv')


df['timestamp'] = pd.to_datetime(df['timestamp'])

# Define the Haversine function 
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers

    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    distance = 2 * R * np.arcsin(sqrt((sin(dlat/2))**2 + cos(lat1)*cos(lat2)*(sin(dlon/2))**2))
    return distance

# Define the proximity threshold in kilometers
threshold_distance = 1.0

# Convert lat and lon to radians 
coords = np.radians(df[['lat', 'lon']].to_numpy())

before_tree = time.time()
# Build the binary KDTree
tree = cKDTree(coords)

after_tree = time.time()

print("time to make tree ", after_tree - before_tree)

# Query the KDTree for all points within the threshold distance
pairs = tree.query_pairs(np.radians(threshold_distance / 6371.0))  # Convert km to radians

after_pairs = time.time()
print("time for queries ", after_pairs - after_tree)
# Collect proximity events
proximity_events = []

for i, j in pairs:
    if df.iloc[i]['mmsi'] != df.iloc[j]['mmsi'] and df.iloc[i]['timestamp'] == df.iloc[j]['timestamp']:
        dist = haversine(df.iloc[i]['lat'], df.iloc[i]['lon'], df.iloc[j]['lat'], df.iloc[j]['lon'])
        if dist < threshold_distance:
            proximity_events.append({
                'mmsi': df.iloc[i]['mmsi'],
                'vessel_proximity': df.iloc[j]['mmsi'],
                'timestamp': df.iloc[i]['timestamp']
            })

after_loop = time.time()

print("time for loop ", after_loop - after_pairs)
# Convert to DataFrame
proximity_df = pd.DataFrame(proximity_events)

proximity_df.to_csv('proximity_data.csv')
# print(proximity_df)
