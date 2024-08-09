from flask import Flask, render_template, request, flash
import gpxpy
import os

from helpers import (
    analyze_gpx_trace,
    compute_duration,
    decimal_time_to_hours_minutes,
)

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'defaultsecretkey')  # Use environment variable or default; needed for flashing messages

from constants import (
    DEFAULT_POS_VERT_SPEED,
    DEFAULT_NEG_VERT_SPEED,
    DEFAULT_HORIZ_SPEED,
    DEFAULT_MARGIN
)   
    
@app.route('/', methods=['GET', 'POST'])
def index():
    pos_vert_len = ''
    neg_vert_len = ''
    horiz_len = ''
    pos_vert_speed = DEFAULT_POS_VERT_SPEED
    neg_vert_speed = DEFAULT_NEG_VERT_SPEED
    horiz_speed = DEFAULT_HORIZ_SPEED
    margin = DEFAULT_MARGIN

    if request.method == 'POST':
        pos_vert_len = int(request.form.get('pos_vert_len', 0))
        neg_vert_len = int(request.form.get('neg_vert_len', 0))
        pos_vert_speed = int(request.form.get('pos_vert_speed', DEFAULT_POS_VERT_SPEED))
        neg_vert_speed = int(request.form.get('neg_vert_speed', DEFAULT_NEG_VERT_SPEED))
        horiz_len = int(request.form.get('horiz_len', 0))
        horiz_speed = int(request.form.get('horiz_speed', DEFAULT_HORIZ_SPEED))
        margin = int(request.form.get('margin', DEFAULT_MARGIN))

        gpx_file = request.files.get('gpx_file')
        if gpx_file:
            gpx_data = analyze_gpx_trace(gpx_file)
            if gpx_data is not None:
                pos_vert_len = gpx_data["positive_elevation"]
                neg_vert_len = gpx_data["negative_elevation"]
                horiz_len = gpx_data["total_distance"]
                flash(f'GPX Analysis: Positive Elevation: {pos_vert_len} m, Negative Elevation: {neg_vert_len} m, Horizontal Length: {horiz_len} km')
            else:   
                # there is no elevation data i nthe GPX
                flash('The GPX file does not contain elevation data. Provide the data manually.')

        duration = compute_duration(
            pos_vert_len, 
            neg_vert_len, 
            pos_vert_speed,
            neg_vert_speed,
            horiz_len,
            horiz_speed,
            margin
        )
        duration_formatted = decimal_time_to_hours_minutes(duration)
        return render_template('index.html', duration=duration_formatted, 
                               pos_vert_len=pos_vert_len, neg_vert_len=neg_vert_len,
                               pos_vert_speed=pos_vert_speed, neg_vert_speed=neg_vert_speed,
                               horiz_len=horiz_len, horiz_speed=horiz_speed, margin=margin)

    return render_template('index.html', duration=None, 
                           pos_vert_len=pos_vert_len, neg_vert_len=neg_vert_len,
                           pos_vert_speed=pos_vert_speed, neg_vert_speed=neg_vert_speed,
                           horiz_len=horiz_len, horiz_speed=horiz_speed, margin=margin)

if __name__ == '__main__':
    app.run(debug=True)