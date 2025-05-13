from datetime import timedelta

# using lists of two elements since dictionaries do not admit keys being integers or float

POLLUTANTS_DATA = {
    "PM10":
        {
            "name": "PM10",
            "unit_of_measure": "[µg/m³]",
            "aggregation_period_vs_pollutant_concentration_thresholds_map": 
                ( 
                    ( timedelta(days=1)   , 50 ) ,
                    ( timedelta(days=365) , 40 ) 
                )
            ,
            "air_quality_categories_geometries":
                [
                    # Fascia colorata di qualità dell’aria 1
                    dict(
                        type="rect",
                        xref="paper", # i valori che fornirò per x si riferitranno agli assi
                        yref="y", # i valori he fornirò per y non hanno limiti
                        x0=0, #fine x
                        y0=0, #[µg/m³]
                        x1=1, #fine x
                        y1=20, #[µg/m³]
                        fillcolor="#50f085", #colore
                        opacity=0.5,
                        layer="below",
                        line_width=0,

                    ),
                    
                    # Fascia colorata di qualità dell’aria 2
                    dict(
                        type="rect",
                        xref="paper", # i valori che fornirò per x si riferitranno agli assi
                        yref="y", # i valori he fornirò per y non hanno limiti
                        x0=0, #fine x
                        y0=20, #[µg/m³]
                        x1=1, #fine x
                        y1=35, #[µg/m³]
                        fillcolor="#80ca3a", #colore
                        opacity=0.5,
                        layer="below",
                        line_width=0,
                    ),
                    
                    # Fascia colorata di qualità dell’aria 3
                    dict(
                        type="rect",
                        xref="paper", # i valori che fornirò per x si riferitranno agli assi
                        yref="y", # i valori he fornirò per y non hanno limiti
                        x0=0, #fine x
                        y0=35, #[µg/m³]
                        x1=1, #fine x
                        y1=50, #[µg/m³]
                        fillcolor="#f0e641", #colore
                        opacity=0.5,
                        layer="below",
                        line_width=0,
                    ),
                    
                    
                    # Fascia colorata di qualità dell’aria 4
                    dict(
                        type="rect",
                        xref="paper", # i valori che fornirò per x si riferitranno agli assi
                        yref="y", # i valori he fornirò per y non hanno limiti
                        x0=0, #fine x
                        y0=50, #[µg/m³]
                        x1=1, #fine x
                        y1=100, #[µg/m³]
                        fillcolor="#fa5050", #colore
                        opacity=0.5,
                        layer="below",
                        line_width=0,
                    ),
                    
                    # Fascia colorata di qualità dell’aria 5
                    dict(
                        type="rect",
                        xref="paper", # i valori che fornirò per x si riferitranno agli assi
                        yref="y", # i valori he fornirò per y non hanno limiti
                        x0=0, #fine x
                        y0=100, #[µg/m³]
                        x1=1, #fine x
                        y1=200, #[µg/m³]
                        fillcolor="#960032", #colore
                        opacity=0.5,
                        layer="below",
                        line_width=0,
                    ),
                    
                    
                    # Fascia colorata di qualità dell’aria 6
                    dict(
                        type="rect",
                        xref="paper", # i valori che fornirò per x si riferitranno agli assi
                        yref="y", # i valori he fornirò per y non hanno limiti
                        x0=0, #fine x
                        y0=200, #[µg/m³]
                        x1=1, #fine x
                        y1=1000, #[µg/m³]
                        fillcolor="#50003c", #colore
                        opacity=0.5,
                        layer="below",
                        line_width=0,
                    )
                    
                ]
        }
        ,
    "PM25":
        {
            "name": "PM2.5",
            "unit_of_measure": "[µg/m³]",
            "aggregation_period_vs_pollutant_concentration_thresholds_map": 
                ( 
                    ( timedelta(days=1)   , 25 ) ,
                    ( timedelta(days=365) , 10 ) 
                )
            ,
            "air_quality_categories_geometries":
                [
                    # Fascia colorata di qualità dell’aria 1
                    dict(
                        type="rect",
                        xref="paper", # i valori che fornirò per x si riferitranno agli assi
                        yref="y", # i valori he fornirò per y non hanno limiti
                        x0=0, #fine x
                        y0=0, #[µg/m³]
                        x1=1, #fine x
                        y1=10, #[µg/m³]
                        fillcolor="#50f085", #colore
                        opacity=0.5,
                        layer="below",
                        line_width=0,

                    ),
                    
                    # Fascia colorata di qualità dell’aria 2
                    dict(
                        type="rect",
                        xref="paper", # i valori che fornirò per x si riferitranno agli assi
                        yref="y", # i valori he fornirò per y non hanno limiti
                        x0=0, #fine x
                        y0=10, #[µg/m³]
                        x1=1, #fine x
                        y1=20, #[µg/m³]
                        fillcolor="#80ca3a", #colore
                        opacity=0.5,
                        layer="below",
                        line_width=0,
                    ),
                    
                    # Fascia colorata di qualità dell’aria 3
                    dict(
                        type="rect",
                        xref="paper", # i valori che fornirò per x si riferitranno agli assi
                        yref="y", # i valori he fornirò per y non hanno limiti
                        x0=0, #fine x
                        y0=20, #[µg/m³]
                        x1=1, #fine x
                        y1=25, #[µg/m³]
                        fillcolor="#f0e641", #colore
                        opacity=0.5,
                        layer="below",
                        line_width=0,
                    ),
                    
                    
                    # Fascia colorata di qualità dell’aria 4
                    dict(
                        type="rect",
                        xref="paper", # i valori che fornirò per x si riferitranno agli assi
                        yref="y", # i valori he fornirò per y non hanno limiti
                        x0=0, #fine x
                        y0=25, #[µg/m³]
                        x1=1, #fine x
                        y1=50, #[µg/m³]
                        fillcolor="#fa5050", #colore
                        opacity=0.5,
                        layer="below",
                        line_width=0,
                    ),
                    
                    # Fascia colorata di qualità dell’aria 5
                    dict(
                        type="rect",
                        xref="paper", # i valori che fornirò per x si riferitranno agli assi
                        yref="y", # i valori he fornirò per y non hanno limiti
                        x0=0, #fine x
                        y0=50, #[µg/m³]
                        x1=1, #fine x
                        y1=100, #[µg/m³]
                        fillcolor="#960032", #colore
                        opacity=0.5,
                        layer="below",
                        line_width=0,
                    ),
                    
                    
                    # Fascia colorata di qualità dell’aria 6
                    dict(
                        type="rect",
                        xref="paper", # i valori che fornirò per x si riferitranno agli assi
                        yref="y", # i valori he fornirò per y non hanno limiti
                        x0=0, #fine x
                        y0=100, #[µg/m³]
                        x1=1, #fine x
                        y1=1000, #[µg/m³]
                        fillcolor="#50003c", #colore
                        opacity=0.5,
                        layer="below",
                        line_width=0,
                    )
                ]

        }
}



# keys should be unique
# the constant should be immutable

# data summaries
#----------------

POLLUTANTS_LABELS = list(POLLUTANTS_DATA.keys())



# data checks
#-------------

for pollutant, data in POLLUTANTS_DATA.items():
    if "air_quality_categories_geometries" in data:
        assert isinstance(data["air_quality_categories_geometries"], list), \
            f"{pollutant} -> 'air_quality_categories_geometries' deve essere una lista"