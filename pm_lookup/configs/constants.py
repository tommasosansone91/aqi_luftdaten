

# numbers
#----------

# it multiplies a radius given in km into a distance of the cartesian filed of coordinates wgs84
# this should be dismissed and a python library be used to calculate distance between points of wgs84 geoid

KILOMETERS_TO_COORDINATES_POINTS_DISTANCE: float = 0.011300045235255235


# urls
#------

TEMPLATE_URL_OF_MAP_SEARCH_ENGINE = "https://www.google.com/search?q={latitude}, {longitude}"
# TEMPLATE_URL_OF_MAP_SEARCH_ENGINE = "https://www.openstreetmap.org/#map=11/{latitude}/{longitude}"


ALL_SENSORS_DATA_URL = "https://data.sensor.community/static/v2/data.json"
 # https://data.sensor.community/static/v2/data.1h.json dati 1h
# https://data.sensor.community/static/v2/data.json dati 5 min


# model names
#-------------

#         "{}".format()
# "".format(MODEL_SERIEPARAMETERSSET_API_NAME)

# API_NAME have underscores
# META_VERBOSE_NAME have spaces

MODEL_AREAPARAMETERSSET_API_NAME = "area_parameters_set"
MODEL_AREAPARAMETERSSET_API_PLURAL_NAME = "list_of_area_parameters_set"

MODEL_SERIEPARAMETERSSET_API_NAME = "serie_parameters_set"
MODEL_SERIEPARAMETERSSET_API_PLURAL_NAME = "list_of_serie_parameters_set"
MODEL_SERIEPARAMETERSSET_META_NAME = "set of parameters of serie"

DATA_REALTIMEDATAPOINT_API_NAME = "realtime_datapoint"

# MODEL_HISTORICALDATAPOINT_API_NAME = "historical_datapoint"  # no need to define it
MODEL_HISTORICALDATAPOINT_API_PLURAL_NAME = "historical_datapoints_subset"
                                            # "list_of_historical_datapoints"

MODEL_COMPUTEDSERIE_API_NAME = "computed_serie"
MODEL_COMPUTEDSERIE_META_NAME = "computed serie"
# MODEL_COMPUTEDSERIE_META_PLURAL_NAME = "computed series"


# choices
#---------

ASYNCHRONOUS_COMPONENTS_TOOLBOX_CALLER_CHOICE_MODEL = "save method of a model"
ASYNCHRONOUS_COMPONENTS_TOOLBOX_CALLER_CHOICE_BASECOMMAND = "baseCommand"