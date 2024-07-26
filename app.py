from flask import Flask, render_template, request
from hiking_duration import compute_duration, decimal_time_to_hours_minutes

app = Flask(__name__)

DEFAULT_POS_VERT_SPEED = 300  # Default positive vertical speed in m/h
DEFAULT_NEG_VERT_SPEED = 500  # Default negative vertical speed in m/h
DEFAULT_HORIZ_SPEED = 4       # Default horizontal speed in km/h
DEFAULT_MARGIN = 20           # Default margin in percentage

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pos_vert_len = float(request.form['pos_vert_len'])
        neg_vert_len = float(request.form['neg_vert_len'])
        pos_vert_speed = float(request.form.get('pos_vert_speed', DEFAULT_POS_VERT_SPEED))
        neg_vert_speed = float(request.form.get('neg_vert_speed', DEFAULT_NEG_VERT_SPEED))
        horiz_len = float(request.form['horiz_len'])
        horiz_speed = float(request.form.get('horiz_speed', DEFAULT_HORIZ_SPEED))
        margin = float(request.form.get('margin', DEFAULT_MARGIN)) / 100

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
        return render_template('index.html', duration=duration_format, 
                               pos_vert_len=pos_vert_len, neg_vert_len=neg_vert_len,
                               pos_vert_speed=pos_vert_speed, neg_vert_speed=neg_vert_speed,
                               horiz_len=horiz_len, horiz_speed=horiz_speed, margin=margin * 100)

    return render_template('index.html', duration=None, 
                           pos_vert_len='', neg_vert_len='',
                           pos_vert_speed=DEFAULT_POS_VERT_SPEED, neg_vert_speed=DEFAULT_NEG_VERT_SPEED,
                           horiz_len='', horiz_speed=DEFAULT_HORIZ_SPEED, margin=DEFAULT_MARGIN)

if __name__ == '__main__':
    app.run(debug=True)