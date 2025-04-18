
# servono a copy_RealtimeDatapoints_objects_in_HistoricalDatapoints()
from pm_lookup.models import TargetArea
from pm_lookup.models import RealtimeDatapoints
from pm_lookup.models import HistoricalDatapoints


def copy_RealtimeDatapoints_objects_in_HistoricalDatapoints():

    latest_data = RealtimeDatapoints.objects.all()
    

    for element in latest_data: 

        element_id = element.target_area.id
        element_name = element.target_area.name
        

        try:       

            new_record = HistoricalDatapoints(
                                                    TargetArea=TargetArea.objects.get(id=element_id),
                                                    
                                                    # all'inizio del ciclo savlo la id dell'oggetto che sto scorrendo
                                                    # quindi qui dico: salva i dati nel campo foreign key 
                                                    # che rimanda all'oggetto avente per id quello che mi sono salvato                                                                                            
                                                    
                                                    last_update_time=element.last_update_time,

                                                    PM10_mean=element.PM10_mean,
                                                    PM25_mean=element.PM25_mean,

                                                    # the air cathegory and label are not saved in the historical element
                                                    # since the legend culd change

                                                    number_of_contributing_sensors=element.number_of_contributing_sensors,

                                                    # la pk è insieme di nome e timestamp
            )
        
            new_record.save()

            print("Dati per %s salvati nel modello storico!" % element_name)

        except Exception as e:
            # dovrei aggiungere che si tratta di errore di unique together

            print(e)

            print("Vincolo unique together violato: i dati acquisiti sono uguali ai precedenti.")
            # questo vincolo c'è solo sui dati storici

            print("Viene impedita l'aggiunta del record [Località: %s Timestamp: %s PM10: %s PM2.5: %s] alla serie storica ." % (element.target_area.name, element.last_update_time, element.PM10_mean, element.PM25_mean) )
            print("I dati acquisiti non sono stati salvati.")


    print("---------------------------------------------------")
    


