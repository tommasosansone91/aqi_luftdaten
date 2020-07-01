   
import numpy as np
import plotly.offline as pyo
import plotly.graph_objs as go

def draw_timeserie_PM10_graph(time_values, PM10_values, PM10_daily_max_35_days_max=None, AQ_intervals=None):
   
    PM10_line = go.Scatter(
                    x=time_values, 
                    y=PM10_values,
                    mode='lines',
                    name="PM 10 [µg/m³]", 

                    marker=dict(
                                color='rgb(128,128,128)',
                                )                    
                    )

    if PM10_daily_max_35_days_max is None: 
        data = [ PM10_line, ]

    else:         

        PM10_daily_max_35_days_max_line = go.Scatter(
                                                x=time_values, 
                                                y=PM10_daily_max_35_days_max,
                                                mode='lines',
                                                name="Soglia massima per la concentrazione giornaliera del PM10", 
                                                
                                                marker=dict(
                                                            # size=12,
                                                            color='rgb(220,20,60)',
                                                            # symbol='pentagon',
                                                            # line = {'width':2}    
                                                            )

                                                ) 

        data = [ PM10_line, PM10_daily_max_35_days_max_line ]   



    

    layout = go.Layout(showlegend=True)
    fig = go.Figure(data=data, layout=layout)

    fig = go.Figure(data=data)

    fig.update_layout(showlegend=True)

    plt_div = pyo.plot(fig, output_type='div')

    return plt_div


    # -------------------------------------

def draw_timeserie_PM25_graph(time_values, PM25_values, AQ_intervals=None):
   
    PM25_line = go.Scatter(
                    x=time_values, 
                    y=PM25_values,
                    mode='lines',
                    name="PM 2.5 [µg/m³]", 

                    marker=dict(
                                color='rgb(105,105,105)',
                                )                    
                    )


    data = [ PM25_line ]

    layout = go.Layout(showlegend=True)
    fig = go.Figure(data=data, layout=layout)

    fig = go.Figure(data=data)

    # con una sola traccia funziona solo dopo
    fig.update_layout(showlegend=True)

    plt_div = pyo.plot(fig, output_type='div')

    return plt_div