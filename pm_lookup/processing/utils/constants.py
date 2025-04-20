from datetime import timedelta

# using lists of two elements since dictionaries do not admit keys being integers or float

# POLLUTANTS_DATA = {
#     "PM10":
#         {
#             "name": "PM10",
#             "unit_of_measure": "[µg/m³]",
#             "AGGREGATION_PERIOD_VS_POLLUTANT_CONCENTRATION_THRESHOLDS_MAP": 
#                 ( 
#                     ( timedelta(days=1) , 50) ,
#                     ( timedelta(days=365) , 40) 
#                 )
#         }
#         ,
#     "PM25":
#         {
#             "name": "PM2.5",
#             "unit_of_measure": "[µg/m³]",
#             "AGGREGATION_PERIOD_VS_POLLUTANT_CONCENTRATION_THRESHOLDS_MAP": 
#                 ( 
#                     ( timedelta(days=1) , 25) ,
#                 ( timedelta(days=365) , 10) 
#                 )
#         }
# }



# deprecated
AGGREGATION_PERIOD_VS_POLLUTANT_CONCENTRATION_THRESHOLDS_MAP = {
    "PM10": ( 
                ( timedelta(days=1) , 50) ,
                ( timedelta(days=365) , 40) 
             ),
    "PM25": ( 
                ( timedelta(days=1) , 25) ,
                ( timedelta(days=365) , 10) 
             )
}

# keys should be unique
# the constant should be immutable