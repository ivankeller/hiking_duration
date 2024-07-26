#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Python Script For Computing Hiking Time 
"""


import argparse
import gpxpy
import gpxpy.gpx
import unittest
from geopy.distance import geodesic
from typing import (
    Any,
    Optional,
)

DEFAULT_POS_VERT_SPEED = 300  # m/h
DEFAULT_NEG_VERT_SPEED = 500  # m/h
DEFAULT_HORIZ_SPEED = 4       # km/h
DEFAULT_MARGIN = 0.2      


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


def analyze_gpx_trace(gpx_file_path):
    """
    Analyzes a GPX file to calculate total positive elevation, negative elevation, and total distance.
    
    Args:
        gpx_file_path (str): Path to the GPX file.
        
    Returns:
        dict: A dictionary containing 'positive_elevation', 'negative_elevation', and 'total_distance'.
    """
    with open(gpx_file_path, 'r') as file:
        gpx = gpxpy.parse(file)
    
    total_positive_elevation = 0.0
    total_negative_elevation = 0.0
    total_distance = 0.0

    for track in gpx.tracks:
        for segment in track.segments:
            previous_point = None
            for point in segment.points:
                if point.elevation is None:
                    return
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
        'total_distance': total_distance / 1000.0  # convert meters to kilometers
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

    
    
def main(gpx_file_path=None):
    if gpx_file_path:
        gpx_data = analyze_gpx_trace(gpx_file_path)
        if gpx_data is not None:
            pos_vert_len = gpx_data['positive_elevation']
            neg_vert_len = gpx_data['negative_elevation']
            horiz_len = gpx_data['total_distance']
            print("GPX trzace analyzed:")
            print(f"Positive elevation = {int(pos_vert_len)} m")
            print(f"Negative elevation = {int(neg_vert_len)} m")
            print(f"Total distance = {int(horiz_len)} km")
        else:
            print("There is no elevation data in this GPX file. Enter the data manually:")
            pos_vert_len, neg_vert_len, horiz_len = get_user_hiking_data()
    else:
        pos_vert_len, neg_vert_len, horiz_len = get_user_hiking_data()
    pos_vert_speed = get_user_input(
        f"Positive elevation speed (m/h), default = {DEFAULT_POS_VERT_SPEED}: ", 
        int,
        default=DEFAULT_POS_VERT_SPEED
    )
    neg_vert_speed = get_user_input(
        f"Negative elevation speed (m/h), default = {DEFAULT_NEG_VERT_SPEED}: ",
        int, 
        default=DEFAULT_NEG_VERT_SPEED
    )
    horiz_speed = get_user_input(
        f"Horizontal speed (km/h), default = {DEFAULT_HORIZ_SPEED}:",
        float,
        default=DEFAULT_HORIZ_SPEED
    )
    margin = get_user_input(
        f"Margin (%)= {DEFAULT_MARGIN:.0%}:",
        int,
        default=DEFAULT_MARGIN
    ) / 100
    
    duration = compute_duration(
        pos_vert_len, 
        neg_vert_len, 
        pos_vert_speed,
        neg_vert_speed,
        horiz_len,
        horiz_speed,
        margin
    )
    duration_format = decimal_time_to_hours_minutes(duration)
    print(f"Total duration = {duration_format}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hiking duration calculator")
    parser.add_argument("gpx_file_path", nargs="?", help="Path to the GPX file")
    parser.add_argument("--test", action="store_true", help="Run doctests")

    args = parser.parse_args()
    if args.test:
        # Run the unit tests
        loader = unittest.TestLoader()
        tests = loader.discover('.', pattern='test_hiking_duration.py')
        testRunner = unittest.TextTestRunner()
        testRunner.run(tests)
    else:
        main(args.gpx_file_path)

