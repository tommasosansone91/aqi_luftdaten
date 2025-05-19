
from .utils.auxiliary_processing import copy_RealtimeDatapoint_objects_in_HistoricalDatapoint
from .realtime_processing_1 import get_data_from_luftdaten_api_and_save_them_in_RealtimeDatapoint


# currently unused
def update_realtime_pm_values_and_save_them_in_HistoricalDatapoint():    

    get_data_from_luftdaten_api_and_save_them_in_RealtimeDatapoint()

    # salvo tutto ciò che c'è nel modello output anche nel modello history
    copy_RealtimeDatapoint_objects_in_HistoricalDatapoint() 
                
    print("I nuovi dati per tutte le aree di interesse sono stati salvati nel modello storico!")

    print("---------------------------------------------------")




