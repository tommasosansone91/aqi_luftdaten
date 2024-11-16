# models

## Input models

#### target_areas	

This models contains the information about the areas in which we want to track data.

Locations are defined by a name, a center (expressed in latitude and longitude) and a radius.

The application will query all the sensors in that area and process their data.

In order for the application to get and record data, it has to be filled with at least one location.


## Output models

### Single-record data models

#### history_datapointss	

This is the so-called "history data model".

It contains all the processed data got from the raw data coming from the Luftdaten API, for each location.


#### realtime_datapointss	

This model contains the lastest recorded raw data, for each location.

### Series data models

#### datapoints_data_series	

This model contains the raw serie of data, for each location.


#### daily_aggregated_data_series	

This model contains the daily-aggregated month-long serie of data, for each location.

