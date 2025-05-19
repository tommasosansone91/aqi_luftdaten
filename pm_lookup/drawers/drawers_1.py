   

from typing import Dict, List, Optional
import plotly.offline as pyo
import plotly.graph_objs as go


def draw_timeserie_pollutant_graph(
        *,
        time_values, 
        pollutant_values, 
        pollutant_threshold=None, 
        AQ_cathegories_geometries: Optional[List[Dict]] = None, 
        graph_title=None,
        pollutant_name=None,
        pollutant_uom=None,
        customdata=None,
        ):
    
    # starting by the asterisk, all aruments must be passed with their names, as keyword arguments

    pollutant_line = go.Scatter(
                        x=time_values, 
                        y=pollutant_values,
                        mode='lines+markers',
                        name="{} {}".format(pollutant_name, pollutant_uom), 

                        marker=dict(
                                    color='rgb(128,128,128)',
                                    ),
                        
                        # include the variable in input here as plotly graph element
                        customdata=customdata,

                        hovertemplate=
                            'Data: %{x|%d-%m-%Y}<br>' +
                            'Ora: %{x|%H:%M}<br>' +
                            'Sensori contribuenti: %{customdata[0]}<br>' +
                            'Concentrazione {}: %{{y:.2f}} {}<br>'.format(pollutant_name, pollutant_uom) +
                            'Categoria AQI: %{customdata[1]}<br>'        
                    )

    #scelta di aggiunta al grafico della linea di massima della normativa
    #se la linea è in input col giusto nome, aggiungila alla lista data, altrimenti no

    if pollutant_threshold is None: 
        data = [ pollutant_line, ]

    else:         

        pollutant_threshold_line = go.Scatter(
                                                x=time_values, 
                                                y=pollutant_threshold,
                                                mode='lines',
                                                name="Soglia massima per la concentrazione giornaliera del {}".format(pollutant_name), 
                                                
                                                marker=dict(
                                                            # size=12,
                                                            color='rgb(220,20,60)',
                                                            # symbol='pentagon',
                                                            # line = {'width':2}    
                                                            )

                                                ) 

        data = [ pollutant_line, pollutant_threshold_line ]   

    #scelta di aggiunta al grafico il titolo del grafico
    #se il titolo è in input col giusto nome, aggiungilo al grafico, altrimenti no

    if graph_title is None:
        layout = go.Layout(showlegend=True, )
    else:
        layout = go.Layout(showlegend=True, title=graph_title)

    fig = go.Figure(data=data, layout=layout)


    # Aggiungo delle fasce colorate indicative della qualità dell’aria
    fig.update_layout(
        shapes=AQ_cathegories_geometries
    )




    # padding dell'asse y rispetto alla linea del grafico  

    # Si calcola il 10% del range (cioè della differenza tra massimo e minimo dei valori dell’inquinante).
    # Questo serve per aggiungere un po’ di spazio sopra la linea nel grafico, in modo che non finisca attaccata al bordo.  
    padding_sup_linea_pollutant = 0.1 * ( max(pollutant_values) - min(pollutant_values) ) #[µg/m³]

    # Se togliere il padding rischia di portare l’asse Y sotto zero (valori negativi), allora non viene aggiunto nessun padding sotto (0).
    # Altrimenti, si aggiunge lo stesso padding anche sotto.
    if min(pollutant_values) - padding_sup_linea_pollutant <=0 :
        padding_inf_linea_pollutant = 0
    else:
        padding_inf_linea_pollutant = padding_sup_linea_pollutant


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
            range=[
                min(pollutant_values) - padding_inf_linea_pollutant ,
                max(pollutant_values) + padding_sup_linea_pollutant
                ]
            )
        )

    # con una sola traccia, showlegend funziona solo dopo
    


    plt_div = pyo.plot(fig, output_type='div')

    return plt_div
