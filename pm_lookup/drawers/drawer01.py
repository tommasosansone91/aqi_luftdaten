   
import numpy as np
import plotly.offline as pyo
import plotly.graph_objs as go


def draw_timeserie_PM10_graph(time_values, PM10_values, PM10_daily_max_35_days_max=None, AQ_intervals=None, graph_title=None):

    PM10_line = go.Scatter(
                    x=time_values, 
                    y=PM10_values,
                    mode='lines',
                    name="PM 10 [µg/m³]", 

                    marker=dict(
                                color='rgb(128,128,128)',
                                )                    
                    )

    #scelta di aggiunta al grafico della linea di massima della normativa
    #se la linea è in input col giusto nome, aggiungila alla lista data, altrimenti no

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

    #scelta di aggiunta al grafico il titolo del grafico
    #se il titolo è in input col giusto nome, aggiungilo al grafico, altrimenti no

    if graph_title is None:
        layout = go.Layout(showlegend=True, )
    else:
        layout = go.Layout(showlegend=True, title=graph_title)


    fig = go.Figure(data=data, layout=layout)

    # con una sola traccia funziona solo dopo
    fig.update_layout(showlegend=True)

    

    plt_div = pyo.plot(fig, output_type='div')

    return plt_div











    # -------------------------------------

def draw_timeserie_PM25_graph(time_values, PM25_values, AQ_intervals=None, graph_title=None):
   
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

    #scelta di aggiunta al grafico il titolo del grafico
    #se il titolo è in input col giusto nome, aggiungilo al grafico, altrimenti no

    if graph_title is None:
        layout = go.Layout(showlegend=True)
    else:
        layout = go.Layout(showlegend=True, title=graph_title)


    fig = go.Figure(data=data, layout=layout)

    # con una sola traccia funziona solo dopo
    fig.update_layout(showlegend=True)

    plt_div = pyo.plot(fig, output_type='div')

    return plt_div