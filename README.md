# Hiking Duration Calculator

This little app calculates the total duration of a hiking trip based on various parameters such as vertical elevations and horizontal distance and speeds. Optionally process a GPX file with elevation data to extract these parameters.

The app has two flavors: an interractive question-answers in command line or a simple web app.  

## Requirements

The app was successfully tested on Python 3.10. 

The following Python packages are required to run the script:

- `geographiclib==2.0`
- `geopy==2.4.1`
- `gpxpy==1.6.2`

You can install these dependencies using the following usual pip command:

```bash
pip install -r requirements.txt
```

## Usage

### Running the web app

execute in a terminal:

```bash
python app.py
```

and use your favourite browser to go to the URL http://127.0.0.1:5000/ .

### Running in command line

do: 
```
python hiking_duration.py [--test] [gpx_file_path] 
```

**Arguments*:*

- `gpx_file_path` (optional): Path to the GPX file to be processed.

#### Options

- `--test`: Run tests.

### Example

To calculate the hiking duration using a GPX file:

```
python hiking_duration.py path/to/your/file.gpx
```

To run the script without a GPX file:

```
python hiking_duration.py
```

To run the tests:

```
python hiking_duration.py --test
```