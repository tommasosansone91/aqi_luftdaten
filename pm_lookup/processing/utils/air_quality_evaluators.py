from pm_lookup.configs.pollutants_data import POLLUTANTS_LABELS
from pm_lookup.exceptions import UnknownPollutantException


def evaluate_pollutant_concentration(pollutant_label, pollutant_concentration):  # [µg/m³]
    """
    Valuta la concentrazione di un inquinante.

    Parametri:
    - pollutant_concentration (float): espresso in [µg/m³]
    - pollutant_label (str): es. "PM10", "PM25"
    """

    if pollutant_label == "PM10":

        # categorie di qualità dell'aria rispetto a PM 10

        if pollutant_concentration <= 20:
            pollutant_concentration_cathegory_label = "Ottima"
            pollutant_concentration_cathegory_number = "prima"

        elif pollutant_concentration >= 20 and pollutant_concentration  <= 35:
            pollutant_concentration_cathegory_label = "Buona"
            pollutant_concentration_cathegory_number = "seconda"
        
        elif pollutant_concentration >= 35 and pollutant_concentration  <= 50:
            pollutant_concentration_cathegory_label = "Accettabile"
            pollutant_concentration_cathegory_number = "terza"

        elif pollutant_concentration >= 50 and pollutant_concentration  <= 100:
            pollutant_concentration_cathegory_label = "Fuori legge"
            pollutant_concentration_cathegory_number = "quarta"

        elif pollutant_concentration >= 100 and pollutant_concentration  <= 200:
            pollutant_concentration_cathegory_label = "Pericolosa"
            pollutant_concentration_cathegory_number = "quinta"

        elif pollutant_concentration >= 200:
            pollutant_concentration_cathegory_label = "Emergenziale"
            pollutant_concentration_cathegory_number = "sesta"

        else:
            pollutant_concentration_cathegory_label = "No data"
            pollutant_concentration_cathegory_number = None


    elif pollutant_label == "PM25":

    # categorie di qualità dell'aria rispetto a PM 2.5

        if pollutant_concentration <= 10:
            pollutant_concentration_cathegory_label = "Ottima"
            pollutant_concentration_cathegory_number = "prima"

        elif pollutant_concentration >= 10 and pollutant_concentration  <= 20:
            pollutant_concentration_cathegory_label = "Buona"
            pollutant_concentration_cathegory_number = "seconda"
        
        elif pollutant_concentration >= 20 and pollutant_concentration  <= 25:
            pollutant_concentration_cathegory_label = "Accettabile"
            pollutant_concentration_cathegory_number = "terza"

        elif pollutant_concentration >= 25 and pollutant_concentration  <= 50:
            pollutant_concentration_cathegory_label = "Fuori legge"
            pollutant_concentration_cathegory_number = "quarta"

        elif pollutant_concentration >= 50 and pollutant_concentration  <= 100:
            pollutant_concentration_cathegory_label = "Pericolosa"
            pollutant_concentration_cathegory_number = "quinta"

        elif pollutant_concentration >= 100:
            pollutant_concentration_cathegory_label = "Emergenziale"
            pollutant_concentration_cathegory_number = "sesta"

        else:
            pollutant_concentration_cathegory_label = "No_data"
            pollutant_concentration_cathegory_number = None

    else:
        raise UnknownPollutantException(pollutant_label, POLLUTANTS_LABELS)
    
    tuple_of_results = (
        pollutant_concentration_cathegory_label, 
        pollutant_concentration_cathegory_number
    )

    return  tuple_of_results