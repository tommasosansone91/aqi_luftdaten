
from .utils.auxiliary_processing import copy_RealtimeDatapoints_objects_in_HistoricalDatapoints
from .realtime_processing_1 import get_data_from_luftdaten_api_and_save_them_in_RealtimeDatapoints


# currently unused
def update_realtime_pm_values_and_save_them_in_HistoricalDatapoints():    

    get_data_from_luftdaten_api_and_save_them_in_RealtimeDatapoints()

    # salvo tutto ciò che c'è nel modello output anche nel modello history
    copy_RealtimeDatapoints_objects_in_HistoricalDatapoints() 
                
    print("I nuovi dati per tutte le località sono stati salvati nel modello storico!")

    print("---------------------------------------------------")




