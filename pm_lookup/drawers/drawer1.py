   
import numpy as np
import plotly.offline as pyo
import plotly.graph_objs as go


def draw_timeserie_PM10_graph(time_values, PM10_values, PM10_daily_max_35_days_max=None, AQ_intervals=None, graph_title=None):

    PM10_line = go.Scatter(
                    x=time_values, 
                    y=PM10_values,
                    mode='lines+markers',
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


    # Aggiungo delle fasce colorate indicative della qualità dell’aria
    fig.update_layout(
        shapes=[
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
            ),
            
            
        ]
    )




    # padding dell'asse y rispetto alla linea del grafico    

    padding_sup_linea_PM10 = 0.1 * ( max(PM10_values) - min(PM10_values) ) #[µg/m³]

    if min(PM10_values)-padding_sup_linea_PM10<=0:
        padding_inf_linea_PM10 = 0

    else:
        padding_inf_linea_PM10 = padding_sup_linea_PM10


    fig.update_layout(
        
        showlegend=True,

        # posizionamento legenda fuori dal grafico in basso iniziale
        legend=dict(
            yanchor="top",
            y=-0.25, # il meno la manda sotto il grafico
            xanchor="left",
            x=0.05 # poco prima di metà
        ),
    
        yaxis=dict(
            range=[min(PM10_values)-padding_inf_linea_PM10 ,max(PM10_values)+ padding_sup_linea_PM10]
            )
        )

    # con una sola traccia, showlegend funziona solo dopo
    


    plt_div = pyo.plot(fig, output_type='div')

    return plt_div











    # -------------------------------------

def draw_timeserie_PM25_graph(time_values, PM25_values, AQ_intervals=None, graph_title=None):
   
    PM25_line = go.Scatter(
                    x=time_values, 
                    y=PM25_values,
                    mode='lines+markers',
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


    # Aggiungo delle fasce colorate indicative della qualità dell’aria

    fig.update_layout(
        shapes=[
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
            ),
            
            
        ]
    )




    # padding dell'asse y rispetto alla linea del grafico    

    padding_sup_linea_PM25 = 0.1 * ( max(PM25_values) - min(PM25_values) ) #[µg/m³]

    if min(PM25_values)-padding_sup_linea_PM25<=0:
        padding_inf_linea_PM25 = 0

    else:
        padding_inf_linea_PM25 = padding_sup_linea_PM25


    fig.update_layout(
                    showlegend=True, 

                    # posizionamento legenda fuori dal grafico in basso iniziale
                    legend=dict(
                        yanchor="top",
                        y=-0.25, # il meno la manda sotto il grafico
                        xanchor="left",
                        x=0.05 # poco prima di metà
                    ),

                    yaxis=dict(
                        range=[min(PM25_values)-padding_inf_linea_PM25 ,max(PM25_values)+ padding_sup_linea_PM25]
                        )
                    )
    
    # con una sola traccia, showlegend funziona solo dopo



    plt_div = pyo.plot(fig, output_type='div')

    return plt_div