# servono a convert_timezone
import datetime

import pytz

import time

# servono a save_in_history()
from pm_lookup.models import target_area
from pm_lookup.models import RealtimeDatapoints
from pm_lookup.models import HistoricalDatapoints


def save_in_history():

    latest_data = RealtimeDatapoints.objects.all()
    

    for element in latest_data: 

        element_id = element.target_area.id
        element_name = element.target_area.Name
        

        try:       

            new_record = HistoricalDatapoints(
                                                    target_area=target_area.objects.get(id=element_id),
                                                    
                                                    # all'inizio del ciclo savlo la id dell'oggetto che sto scorrendo
                                                    # quindi qui dico: salva i dati nel campo foreign key 
                                                    # che rimanda all'oggetto avente per id quello che mi sono salvato                                                                                            
                                                    
                                                    Last_update_time=element.Last_update_time,

                                                    PM10_mean=element.PM10_mean,
                                                    PM25_mean=element.PM25_mean,

                                                    PM10_mean_quality_cathegory_label=element.PM10_mean_quality_cathegory_label, 
                                                    PM25_mean_quality_cathegory_label=element.PM25_mean_quality_cathegory_label,

                                                    PM10_mean_quality_cathegory=element.PM10_mean_quality_cathegory,
                                                    PM25_mean_cathegory=element.PM25_mean_cathegory,

                                                    number_of_contributing_sensors=element.number_of_contributing_sensors,

                                                    # la pk è insieme di nome e timestamp
            )
        
            new_record.save()

            print("Dati per %s salvati nel modello storico!" % element_name)

        except:
            # dovrei aggiungere che si tratta di errore di unique together

            print("Vincolo unique together violato: i dati acquisiti sono uguali ai precedenti.")
            # questo vincolo c'è solo sui dati storici

            print("Viene impedita l'aggiunta del record [Località: %s Timestamp: %s PM10: %s PM2.5: %s] alla serie storica ." % (element.target_area.Name, element.Last_update_time, element.PM10_mean, element.PM25_mean) )
            print("I dati acquisiti non sono stati salvati.")


    print("---------------------------------------------------")
    



def evaluate_PM10(PM10_value):

    # categorie di qualità dell'aria rispetto a PM 10

    if PM10_value <=20:
        PM10_mean_quality_cathegory_label="Ottima"
        PM10_mean_quality_cathegory="prima"

    elif PM10_value>=20 and PM10_value <=35:
        PM10_mean_quality_cathegory_label="Buona"
        PM10_mean_quality_cathegory="seconda"
    
    elif PM10_value>=35 and PM10_value <=50:
        PM10_mean_quality_cathegory_label="Accettabile"
        PM10_mean_quality_cathegory="terza"

    elif PM10_value>=50 and PM10_value <=100:
        PM10_mean_quality_cathegory_label="Fuori legge"
        PM10_mean_quality_cathegory="quarta"

    elif PM10_value>=100 and PM10_value <=200:
        PM10_mean_quality_cathegory_label="Pericolosa"
        PM10_mean_quality_cathegory="quinta"

    elif PM10_value>=200:
        PM10_mean_quality_cathegory_label="Emergenziale"
        PM10_mean_quality_cathegory="sesta"

    else:
        PM10_mean_quality_cathegory_label="No data"
        PM10_mean_quality_cathegory="nessuna"

    return (PM10_mean_quality_cathegory_label, PM10_mean_quality_cathegory)



def evaluate_PM25(PM25_value):

    # categorie di qualità dell'aria rispetto a PM 2.5

    if PM25_value <=10:
        PM25_mean_quality_cathegory_label="Ottima"
        PM25_mean_cathegory="prima"

    elif PM25_value>=10 and PM25_value <=20:
        PM25_mean_quality_cathegory_label="Buona"
        PM25_mean_cathegory="seconda"
    
    elif PM25_value>=20 and PM25_value <=25:
        PM25_mean_quality_cathegory_label="Accettabile"
        PM25_mean_cathegory="terza"

    elif PM25_value>=25 and PM25_value <=50:
        PM25_mean_quality_cathegory_label="Fuori legge"
        PM25_mean_cathegory="quarta"

    elif PM25_value>=50 and PM25_value <=100:
        PM25_mean_quality_cathegory_label="Pericolosa"
        PM25_mean_cathegory="quinta"

    elif PM25_value>=100:
        PM25_mean_quality_cathegory_label="Emergenziale"
        PM25_mean_cathegory="sesta"

    else:
        PM25_mean_quality_cathegory_label="No_data"
        PM25_mean_cathegory="nessuna"

    return (PM25_mean_quality_cathegory_label, PM25_mean_cathegory)


# converte da una timezone ad un'altra
def convert_datetime_timezone(date_and_time_input, tz1, tz2):
    tz1 = pytz.timezone(tz1)
    tz2 = pytz.timezone(tz2)

    dt = datetime.datetime.strptime(date_and_time_input,"%Y-%m-%d %H:%M:%S")
    dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)
    dt = dt.strftime("%Y-%m-%d %H:%M:%S")

    return dt

#sposta le lancette avanti di uno
def add_one_hour(date_and_time_input):
    # modo semplice per dire che sposti le ore avanti di 1
    dt = convert_datetime_timezone(date_and_time_input, "Europe/London", "Europe/Berlin")
    return dt


# aggiunto per fixare il fatto che nei grafici è mostrato orario come se fosse in UTC
# errore sopraggiunto dopo il reset del db?
def add_hours_to_array(date_and_time_input, hours):

    hours_added = datetime.timedelta(hours = hours)

    future_date_and_time = [ i + hours_added for i in date_and_time_input ]

    return future_date_and_time



def fix_timezone_mismatch_1(date_and_time_input):

    # se è attiva l'ora legale nel tempo locale
    if time.localtime().tm_isdst != 0:        
        hours = -time.timezone/3600 + 1

    elif time.localtime().tm_isdst == 0:
        hours = -time.timezone/3600

    future_date_and_time = add_hours_to_array(date_and_time_input, hours)

    return future_date_and_time