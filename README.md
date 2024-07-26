# Hiking Duration Calculator

This script calculates the total duration of a hiking trip based on various parameters such as vertical and horizontal lengths and speeds. It can optionally process a GPX file to extract these parameters.

## Requirements

The following Python packages are required to run the script:

- `geographiclib==2.0`
- `geopy==2.4.1`
- `gpxpy==1.6.2`

You can install these dependencies using the following command:

```
pip install -r requirements.txt
```

## Usage

To run the script, you can provide the path to a GPX file as an optional argument. If no GPX file is provided, the script will use default values for the parameters.

```
python hiking_duration.py [gpx_file_path]
```

### Arguments

- `gpx_file_path` (optional): Path to the GPX file to be processed.

### Options

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