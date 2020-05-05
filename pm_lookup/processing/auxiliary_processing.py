# servono a save_in_history()
from pm_lookup.models import target_area_input_data
from pm_lookup.models import target_area_output_data
from pm_lookup.models import target_area_history_data


def save_in_history():

    latest_data = target_area_output_data.objects.all()

    for element in latest_data:        

        new_record = target_area_history_data(
                                                # Target_area_name=target_area_output_data.objects.get(Name=place_name),
                                                Target_area_name=element.Target_area_name,
                                                
                                                Latitude = element.Longitude,
                                                Longitude = element.Latitude,
                                                Radius = element.Radius,                                             
                                                
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
        

        try:
            new_record.save()
        except:
            print("Viene impedita l'aggiunta del record [Località: %s Timestamp: %s PM10: %s PM2.5: %s] alla serie storica perchè questo record è già presente nella serie storica e si vogliono evitare ripetizioni." % (element.Target_area_name, element.Last_update_time, element.PM10_mean, element.PM25_mean) )

        print("I nuovi dati per %s sono stati aggiunti alla serie storica!" % element.Target_area_name)

    print("I nuovi dati di tutte le località sono stati aggiunti alle serie storiche!")

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
        PM10_quality="Al_limite_dell'accettabilità"
        PM10_cathegory="terza"

    elif PM10_value>=50 and PM10_value <=100:
        PM10_quality="Fuori_legge"
        PM10_cathegory="quarta"

    elif PM10_value>=100 and PM10_value <=200:
        PM10_quality="Pericolosa"
        PM10_cathegory="quita"

    elif PM10_value>=200:
        PM10_quality="Emergenza!_Evacuazione!"
        PM10_cathegory="sesta"

    else:
        PM10_quality="No_data"
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
        PM25_quality="Al_limite_dell'accettabilità"
        PM25_cathegory="terza"

    elif PM25_value>=25 and PM25_value <=50:
        PM25_quality="Fuori_legge"
        PM25_cathegory="quarta"

    elif PM25_value>=50 and PM25_value <=100:
        PM25_quality="Pericolosa"
        PM25_cathegory="quinta"

    elif PM25_value>=100:
        PM25_quality="Emergenza!_Evacuazione!"
        PM25_cathegory="sesta"

    else:
        PM25_quality="No_data"
        PM25_cathegory="nessuna"

    return (PM25_quality, PM25_cathegory)