from datetime import timedelta

# using lists of two elements since dictionaries do not admit keys being integers or float

POLLUTANTS_DATA = {
    "PM10":
        {
            "name": "PM10",
            "unit_of_measure": "[µg/m³]",
            "AGGREGATION_PERIOD_VS_POLLUTANT_CONCENTRATION_THRESHOLDS_MAP": 
                ( 
                    ( timedelta(days=1) , 50) ,
                    ( timedelta(days=365) , 40) 
                )
        }
        ,
    "PM25":
        {
            "name": "PM2.5",
            "unit_of_measure": "[µg/m³]",
            "AGGREGATION_PERIOD_VS_POLLUTANT_CONCENTRATION_THRESHOLDS_MAP": 
                ( 
                    ( timedelta(days=1) , 25) ,
                ( timedelta(days=365) , 10) 
                )
        }
}




# keys should be unique
# the constant should be immutable

def return_graph_title(pollutant_name="", set_of_parameters_title=""):
   return "Serie storiche del {} per {}".format(pollutant_name, set_of_parameters_title)
