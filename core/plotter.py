import os
import re
import folium
import requests
import pandas as pd
from io import BytesIO
from geopy.distance import geodesic
import numpy as np

def check_dataframe(df, required_columns):
    """
    Check if the DataFrame contains the required columns.
    """
    for col in required_columns:
        if col not in df.columns:
            return False
    return True

def get_coordinates(city):
    """
    Use OpenStreetMap's Nominatim API to get latitude and longitude for a given city.
    """
    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": city, "format": "json"},
            headers={"User-Agent": "Mozilla/5.0"}
        )
        response.raise_for_status()
        results = response.json()
        if results:
            return float(results[0]["lat"]), float(results[0]["lon"])
    except Exception as e:
        print(f"Error getting coordinates for {city}: {e}")
    return None, None

def get_geodesic_curve(origin, destination, n_points=100):
    """
    Calcule une série de points suivant une courbure géodésique entre deux coordonnées.
    
    :param origin: Tuple (lat1, lon1) en degrés.
    :param destination: Tuple (lat2, lon2) en degrés.
    :param n_points: Nombre de points sur la courbure.
    :return: Liste de points (latitude, longitude) représentant la courbure.
    """
    # Convertir les coordonnées en radians
    lat1, lon1 = np.radians(origin)
    lat2, lon2 = np.radians(destination)
    
    # Calculer le vecteur de direction entre les deux points
    delta_lon = lon2 - lon1
    delta_lat = lat2 - lat1

    # Distance angulaire entre les points (grande cercle)
    delta_sigma = np.arccos(
        np.sin(lat1) * np.sin(lat2) +
        np.cos(lat1) * np.cos(lat2) * np.cos(delta_lon)
    )
    
    # Liste pour stocker les points interpolés
    points = []
    
    for i in range(n_points + 1):
        t = i / n_points
        
        # Interpolation sphérique
        A = np.sin((1 - t) * delta_sigma) / np.sin(delta_sigma)
        B = np.sin(t * delta_sigma) / np.sin(delta_sigma)
        
        x = A * np.cos(lat1) * np.cos(lon1) + B * np.cos(lat2) * np.cos(lon2)
        y = A * np.cos(lat1) * np.sin(lon1) + B * np.cos(lat2) * np.sin(lon2)
        z = A * np.sin(lat1) + B * np.sin(lat2)
        
        # Convertir en latitude et longitude
        lat = np.arctan2(z, np.sqrt(x**2 + y**2))
        lon = np.arctan2(y, x)
        
        # Ajouter le point à la liste, converti en degrés
        points.append([np.degrees(lat), np.degrees(lon)])
    
    return points

def plotMap(dataframe, tile='OpenStreetMap'):
    """
    Plot a map with the given dataframe and tile
    :param dataframe: DataFrame with columns 'Departure city', 'Departure lat', 'Departure lon', 'Arrival city', 'Arrival lat', 'Arrival lon', 'Line color'
    :param tile: Tile type for the map (e.g., 'OpenStreetMap', 'Cartodb Positron', etc.)
    :return: Folium map object
    """
    if dataframe.empty:
        print("Empty dataframe")
        return None

    # Initial map center
    center_lat = dataframe['Departure lat'].mean()
    center_lon = dataframe['Departure lon'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=4, tiles=tile)

    for _, row in dataframe.iterrows():
        origin = (row['Departure lat'], row['Departure lon'])
        dest = (row['Arrival lat'], row['Arrival lon'])
        line_color = row['Line color']

        # Add markers
        folium.CircleMarker(origin, radius=5, color='black', fill=True, fill_color='blue', 
                    tooltip=f"Departure: {row['Departure city']}").add_to(m)
        folium.CircleMarker(dest, radius=5, color='black', fill=True, fill_color='red', 
                    tooltip=f"Arrival: {row['Arrival city']}").add_to(m)

        folium.Circle(origin)

        # Add geodesic curve
        curve_points = get_geodesic_curve(origin, dest)
        folium.PolyLine(locations=curve_points, color=line_color, weight=2.5).add_to(m)

    return m