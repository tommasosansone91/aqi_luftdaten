<h1>AQI Luftdaten app</h1>
    
<br>

<p>
    Questa applicazione permette di conoscere 
    i valori del particolato atmosferico di un'area selezionata in tempo reale.
</p>

<p>
    L'app funziona grazie ai dati registrati dalle centraline <a target="_blank" href="https://luftdaten.info/it/benvenuto/">Luftdaten</a>, 
    un progetto di scienza partecipata che permette ai cittadini di <a target="_blank" href="https://www.produzionidalbasso.com/project/1-000-centraline-dal-basso-in-italia/">acquistare</a> o <a target="_blank" href="http://centralinedalbasso.org/">costruire</a> in maniera autonoma delle centraline di rilevamento del particolato.
</p>    

<p>
    Le centraline trasmettono i dati in tempo reale ad un server centrale, 
    che raffigura i valori di qualità dell'aria su una <a target="_blank" href="https://italia.maps.sensor.community/#6/42.000/12.000">mappa interattiva</a> 
    e li rende disponibili in formato open-source ad altre applicazioni tramite <a target="_blank" href="https://github.com/opendata-stuttgart/meta/wiki/EN-APIs">API</a>.
</p>

<p>
    Questa applicazione seleziona i dati registrati dalle centraline Luftdaten presenti in una certa area definita dall'utente,
    esegue una media aritmetica tra i valori registrati per il particolato e infine li mostra all'utente, 
    specificando la categoria della qualità dell'aria in cui ricadono i valori monitorati.
</p>

<br>


![Grafico dei valori storici orari del PM 10 nella città di roma](/static/img/grafico_Roma.jpg?raw=true "Optional Title")

## Guida all'installazione

https://github.com/tommasosansone91/aqi_luftdaten/blob/master/dev_docs/install_on_raspberrypi.md