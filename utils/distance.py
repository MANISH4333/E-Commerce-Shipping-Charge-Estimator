"""
Distance calculation utility using the Haversine formula.

The Haversine formula determines the great-circle distance between
two points on a sphere given their latitudes and longitudes.
"""

import math

# Earth's mean radius in kilometres
EARTH_RADIUS_KM = 6371.0


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points on Earth.

    Args:
        lat1: Latitude of point 1 (in degrees).
        lon1: Longitude of point 1 (in degrees).
        lat2: Latitude of point 2 (in degrees).
        lon2: Longitude of point 2 (in degrees).

    Returns:
        Distance in kilometres (rounded to 2 decimal places).
    """
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    # Haversine formula
    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = EARTH_RADIUS_KM * c
    return round(distance, 2)
