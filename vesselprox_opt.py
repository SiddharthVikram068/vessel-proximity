import pandas as pd
import numpy as np
from scipy.spatial import cKDTree
from math import radians, cos, sin, sqrt, atan2
import time
# Load data
df = pd.read_csv('sample_data.csv')

threshold_distance = 1.0

before_time = time.time()
# Parse timestamps
df['timestamp'] = pd.to_datetime(df['timestamp'])


# Define the Haversine formula using vectorization
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers

    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    distance = 2 * R * np.arcsin(sqrt((sin(dlat/2))**2 + cos(lat1)*cos(lat2)*(sin(dlon/2))**2))
    return distance



# Prepare a list to collect proximity events
proximity_events = []
grouped = df.groupby('timestamp')


# Iterate through each group
for timestamp, group in grouped:

    if len(group) < 2:
        continue  # Skip groups with less than 2 ships

    # Convert lat and lon to radians for quadtree
    coords = np.radians(group[['lat', 'lon']].values)

    # Build the quadtree
    tree = cKDTree(coords)

    # Define the proximity threshold in kilometers


    # Query the quadtree for all points within the threshold distance
    pairs = tree.query_pairs(np.radians(threshold_distance / 6371.0))  # Convert km to radians

    # Collect proximity events with a filter for different MMSI
    for i, j in pairs:
        if group.iloc[i]['mmsi'] != group.iloc[j]['mmsi']:
            dist = haversine(group.iloc[i]['lat'], group.iloc[i]['lon'],
                             group.iloc[j]['lat'], group.iloc[j]['lon'])
            if dist < threshold_distance:
                proximity_events.append({
                    'mmsi': group.iloc[i]['mmsi'],
                    'vessel_proximity': group.iloc[j]['mmsi'],
                    'timestamp': group.iloc[i]['timestamp']
                })

# Convert to DataFrame
proximity_df = pd.DataFrame(proximity_events)
proximity_df.to_csv('proximity_data.csv')
# print(proximity_df)
after_time = time.time()
print("time taken ", after_time - before_time)
