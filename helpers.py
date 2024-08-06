
import gpxpy
import gpxpy.gpx
from geopy.distance import geodesic
from typing import (
    Optional,
    Any
)


def get_user_input(prompt: str, expected_type: Any, default : Optional[int] = None) -> int:
    """Prompts the user for input and ensures it is an integer.
    
    Args:
        prompt (str): The message to display to the user.
        expected_type: The expected type of the user input
        default: value used if user does not provide any value
        
    Returns:
        The input provided by the user;

    """
    while True:
        user_response = input(prompt)
        if default is not None and user_response == "":
            print(f"Using default value = {default}.")
            return default
        else:
            try:
                return expected_type(user_response)
            except (ValueError, TypeError) as e:
                print(f"Error casting value '{user_response}' to type '{expected_type}': {e}. Retry.")


def analyze_gpx_trace(gpx_file):
    """
    Analyzes a GPX file to calculate total positive elevation, negative elevation, and total distance.
    
    Args:
        gpx_file : A GPX file.
        
    Returns:
        dict: A dictionary containing 'positive_elevation', 'negative_elevation', and 'total_distance'.
    
    """
    gpx = gpxpy.parse(gpx_file)
    
    total_positive_elevation = 0.0
    total_negative_elevation = 0.0
    total_distance = 0.0

    for track in gpx.tracks:
        for segment in track.segments:
            previous_point = None
            for point in segment.points:
                if point.elevation is None:
                    return None
                if previous_point:
                    # Calculate elevation gain/loss
                    elevation_change = point.elevation - previous_point.elevation
                    if elevation_change > 0:
                        total_positive_elevation += elevation_change
                    else:
                        total_negative_elevation += elevation_change
                    
                    # Calculate distance
                    total_distance += geodesic(
                        (previous_point.latitude, previous_point.longitude),
                        (point.latitude, point.longitude)).meters
                
                previous_point = point
    
    return {
        'positive_elevation': total_positive_elevation,
        'negative_elevation': - total_negative_elevation,
        'total_distance': total_distance / 1000  # convert to km
    }

def compute_duration(
    pos_vert_len, 
    neg_vert_len, 
    pos_vert_speed,
    neg_vert_speed,
    horiz_len,
    horiz_speed,
    margin
) -> float:
    """Compute the total duration of the hike."""
    pos_vert_duration = pos_vert_len / pos_vert_speed
    neg_vert_duration = neg_vert_len / neg_vert_speed
    horiz_duration = horiz_len / horiz_speed
    total_duration = max(
        pos_vert_duration + neg_vert_duration,
        horiz_duration
        ) + 0.5 * min(
        pos_vert_duration + neg_vert_duration,
        horiz_duration
    )
    total_duration_with_margin = (1 + margin) * total_duration
    return total_duration_with_margin

def decimal_time_to_hours_minutes(time: float) -> str:
    """Return a duration in hours and minutes from a decimal duration.
    
    Round to the nearest 5 minutes.
    
    Args:
        time (float): The decimal time to be converted.
        
    Returns:
        str: The time in hours and minutes, rounded to the nearest 5 minutes.

    Example:
    >>> decimal_time_to_hours_minutes(2.33)
    '2 h 20 min'
    """
    # Calculate hours and minutes
    hours = int(time)
    minutes = (time - hours) * 60
    
    # Round minutes to the nearest 5
    minutes = round(minutes / 5) * 5
    
    if minutes == 60:
        hours += 1
        minutes = 0
    
    return f"{hours} h {minutes} min"

def get_user_hiking_data():
        pos_vert_len = get_user_input("Positive elevation (m): ", int)
        neg_vert_len = get_user_input("Negative elevation (m): ", int)
        horiz_len = get_user_input("total distance (km): ", float)
        return pos_vert_len, neg_vert_len, horiz_len
