# servono a convert_timezone
import datetime

import pytz

# servono a save_in_history()
from pm_lookup.models import target_area_input_data
from pm_lookup.models import target_area_output_data
from pm_lookup.models import target_area_history_data


def save_in_history():

    latest_data = target_area_output_data.objects.all()
    

    for element in latest_data: 

        element_id = element.Target_area_input_data.id
        element_name = element.Target_area_input_data.Name
        

        try:       

            new_record = target_area_history_data(
                                                    Target_area_input_data=target_area_input_data.objects.get(id=element_id),
                                                    
                                                    # all'inizio del ciclo savlo la id dell'oggetto che sto scorrendo
                                                    # quindi qui dico: salva i dati nel campo foreign key 
                                                    # che rimanda all'oggetto avente per id quello che mi sono salvato                                                                                            
                                                    
                                                    Last_update_time=element.Last_update_time,

                                                    PM10_mean=element.PM10_mean,
                                                    PM25_mean=element.PM25_mean,

                                                    PM10_quality=element.PM10_quality, 
                                                    PM25_quality=element.PM25_quality,

                                                    PM10_cathegory=element.PM10_cathegory,
                                                    PM25_cathegory=element.PM25_cathegory,

                                                    n_selected_sensors=element.n_selected_sensors,

                                                    # la pk è insieme di nome e timestamp
            )
        
            new_record.save()

            print("Dati per %s salvati nel modello storico!" % element_name)

        except:
            # dovrei aggiungere che si tratta di errore di unique together

            print("Vincolo unique together violato: i dati acquisiti sono uguali ai precedenti.")
            # questo vincolo c'è solo sui dati storici

            print("Viene impedita l'aggiunta del record [Località: %s Timestamp: %s PM10: %s PM2.5: %s] alla serie storica ." % (element.Target_area_input_data.Name, element.Last_update_time, element.PM10_mean, element.PM25_mean) )
            print("I dati acquisiti non sono stati salvati.")


    print("---------------------------------------------------")
    



def evaluate_PM10(PM10_value):

    # categorie di qualità dell'aria rispetto a PM 10

    if PM10_value <=20:
        PM10_quality="Ottima"
        PM10_cathegory="prima"

    elif PM10_value>=20 and PM10_value <=35:
        PM10_quality="Buona"
        PM10_cathegory="seconda"
    
    elif PM10_value>=35 and PM10_value <=50:
        PM10_quality="Al limite dell'accettabilità"
        PM10_cathegory="terza"

    elif PM10_value>=50 and PM10_value <=100:
        PM10_quality="Fuori legge"
        PM10_cathegory="quarta"

    elif PM10_value>=100 and PM10_value <=200:
        PM10_quality="Pericolosa"
        PM10_cathegory="quita"

    elif PM10_value>=200:
        PM10_quality="Emergenza! Evacuazione!"
        PM10_cathegory="sesta"

    else:
        PM10_quality="No data"
        PM10_cathegory="nessuna"

    return (PM10_quality, PM10_cathegory)



def evaluate_PM25(PM25_value):

    # categorie di qualità dell'aria rispetto a PM 2.5

    if PM25_value <=10:
        PM25_quality="Ottima"
        PM25_cathegory="prima"

    elif PM25_value>=10 and PM25_value <=20:
        PM25_quality="Buona"
        PM25_cathegory="seconda"
    
    elif PM25_value>=20 and PM25_value <=25:
        PM25_quality="Al limite dell'accettabilità"
        PM25_cathegory="terza"

    elif PM25_value>=25 and PM25_value <=50:
        PM25_quality="Fuori legge"
        PM25_cathegory="quarta"

    elif PM25_value>=50 and PM25_value <=100:
        PM25_quality="Pericolosa"
        PM25_cathegory="quinta"

    elif PM25_value>=100:
        PM25_quality="Emergenza! Evacuazione!"
        PM25_cathegory="sesta"

    else:
        PM25_quality="No_data"
        PM25_cathegory="nessuna"

    return (PM25_quality, PM25_cathegory)


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



# controlla se è attiva l'ora legale
# def is_dst(dt,timeZone):
#    aware_dt = timeZone.localize(dt)
#    return aware_dt.dst() != datetime.timedelta(0,0)





# def convert_timezone_and_add_one_hour(date_and_time_input, tz1, tz2):
#     dt = convert_datetime_timezone(date_and_time_input, tz1, tz2)
#     dt = add_one_hour(dt)
#     return dt

# controlla se è attiva l'ora legale
# def is_dst(dt=None, timezone="UTC"):
#     if dt is None:
#         dt = datetime.utcnow()
#     timezone = pytz.timezone(timezone)
#     timezone_aware_date = timezone.localize(dt, is_dst=None)
#     return timezone_aware_date.tzinfo._dst.seconds != 0




# def convert_timezone_and_check_summertime(date_and_time_input, tz1, tz2):

#     # converte da una zona all'altra
#     dt = convert_datetime_timezone(date_and_time_input, tz1, tz2)

#     # se è attiva l'ora legale nella timezone di destinazione
#     if is_dst(dt, tz2):
#         dt = add_one_hour(dt)

#     return dt