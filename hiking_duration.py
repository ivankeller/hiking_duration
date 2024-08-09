#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Python Script For Computing Hiking Time 
"""


import argparse
import unittest
from helpers import (
    get_user_input,
    analyze_gpx_trace,
    compute_duration,
    decimal_time_to_hours_minutes,
    get_user_hiking_data
)

from constants import (
    DEFAULT_POS_VERT_SPEED,
    DEFAULT_NEG_VERT_SPEED,
    DEFAULT_HORIZ_SPEED,
    DEFAULT_MARGIN
)      


def main(gpx_file_path=None):
    if gpx_file_path:
        with open(gpx_file_path, 'r') as gpx_file:
            gpx_data = analyze_gpx_trace(gpx_file)
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
        f"Horizontal speed (km/h), default = {DEFAULT_HORIZ_SPEED}: ",
        float,
        default=DEFAULT_HORIZ_SPEED
    )
    margin = get_user_input(
        f"Margin (%)= {DEFAULT_MARGIN}%:",
        int,
        default=DEFAULT_MARGIN
    )
    
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
    print()
    pt = pos_vert_len/pos_vert_speed
    nt = neg_vert_len/neg_vert_speed
    ht = horiz_len/horiz_speed
    print("Detail of the calculation:")
    print(f"Positive elevation time (pt): {pt:.1f} h")
    print(f"Negative elevation time (nt): {nt:.1f} h")
    print(f"horizontal time (ht): {ht:.1f} h")
    print(f"Walking duration = Max(pt + nt, ht) + 0.5 * Min(pt + nt, ht)")
    print(f"Walking duration = Max({pt:.1f} + {nt:.1f}, {ht:.1f}) + 0.5 * Min({pt:.1f} + {nt:.1f}, {ht:.1f})")
    print(f"Total duration (with margin) = {1 + margin / 100:.2f} * Walking duration = {duration_format}")


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

