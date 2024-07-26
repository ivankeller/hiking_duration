import unittest
from io import StringIO
from unittest.mock import patch
from hiking_duration import (
    get_user_input,
    analyze_gpx_trace,
    compute_duration,
    decimal_time_to_hours_minutes,
    get_user_hiking_data,
    main,
)

class TestHikingDuration(unittest.TestCase):
    def test_get_user_input(self):
        with patch('builtins.input', return_value='10'):
            result = get_user_input("Enter a number: ", int)
            self.assertEqual(result, 10)

    def test_analyze_gpx_trace(self):
        gpx_file_path = "test.gpx"
        expected_result = {
            'positive_elevation': 1000.0,
            'negative_elevation': 500.0,
            'total_distance': 0.0
        }
        with patch('builtins.open', return_value=StringIO(
            """<gpx>
                <trk>
                    <trkseg>
                        <trkpt lat="0" lon="0">
                            <ele>0</ele>
                        </trkpt>
                        <trkpt lat="0" lon="0">
                            <ele>1000</ele>
                        </trkpt>
                        <trkpt lat="0" lon="0">
                            <ele>500</ele>
                        </trkpt>
                    </trkseg>
                </trk>
            </gpx>"""
        )):
            result = analyze_gpx_trace(gpx_file_path)
            self.assertDictEqual(result, expected_result)

    def test_compute_duration(self):
        pos_vert_len = 900
        neg_vert_len = 500
        pos_vert_speed = 300
        neg_vert_speed = 500
        horiz_len = 10
        horiz_speed = 5
        margin = 0.2
        expected_result = 6.0
        result = compute_duration(
            pos_vert_len, 
            neg_vert_len, 
            pos_vert_speed,
            neg_vert_speed,
            horiz_len,
            horiz_speed,
            margin
        )
        self.assertEqual(result, expected_result)

    def test_decimal_time_to_hours_minutes(self):
        time = 2.33
        expected_result = "2 h 20 min"
        result = decimal_time_to_hours_minutes(time)
        self.assertEqual(result, expected_result)

    def test_get_user_hiking_data(self):
        with patch('builtins.input', side_effect=['1000', '500', '10']):
            result = get_user_hiking_data()
            self.assertEqual(result, (1000, 500, 10))

    def test_main(self):
        with patch('builtins.input', side_effect=['900', '500', '10', '300', '500', '5', '20']):
            with patch('builtins.print') as mock_print:
                main()
                mock_print.assert_called_with("Total duration = 6 h 0 min.")

if __name__ == '__main__':
    unittest.main(verbosity=2)