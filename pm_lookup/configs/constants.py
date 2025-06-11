
# it multiplies a radius given in km into a distance of the cartesian filed of coordinates wgs84
# this should be dismissed and a python library be used to calculate distance between points of wgs84 geoid

KILOMETERS_TO_COORDINATES_POINTS_DISTANCE: float = 0.011300045235255235

TEMPLATE_URL_OF_MAP_SEARCH_ENGINE = "https://www.google.com/search?q={latitude}, {longitude}"
# TEMPLATE_URL_OF_MAP_SEARCH_ENGINE = "https://www.openstreetmap.org/#map=11/{latitude}/{longitude}"

ALL_SENSORS_DATA_URL = "https://data.sensor.community/static/v2/data.json"
 # https://data.sensor.community/static/v2/data.1h.json dati 1h
# https://data.sensor.community/static/v2/data.json dati 5 min


SET_OF_PARAMETERS_OF_SERIE_META_VERBOSE_NAME = "set of parameters of serie"
COMPUTED_SERIE_META_VERBOSE_NAME = "computed serie"


ASYNCHRONOUS_COMPONENTS_TOOLBOX_CALLER_CHOICE_MODEL = "save method of a model"
ASYNCHRONOUS_COMPONENTS_TOOLBOX_CALLER_CHOICE_BASECOMMAND = "baseCommand"