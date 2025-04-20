

def evaluate_PM10(PM10_value):

    # categorie di qualità dell'aria rispetto a PM 10

    if PM10_value <= 20:
        PM10_mean_cathegory_label = "Ottima"
        PM10_mean_cathegory = "prima"

    elif PM10_value >= 20 and PM10_value  <= 35:
        PM10_mean_cathegory_label = "Buona"
        PM10_mean_cathegory = "seconda"
    
    elif PM10_value >= 35 and PM10_value  <= 50:
        PM10_mean_cathegory_label = "Accettabile"
        PM10_mean_cathegory = "terza"

    elif PM10_value >= 50 and PM10_value  <= 100:
        PM10_mean_cathegory_label = "Fuori legge"
        PM10_mean_cathegory = "quarta"

    elif PM10_value >= 100 and PM10_value  <= 200:
        PM10_mean_cathegory_label = "Pericolosa"
        PM10_mean_cathegory = "quinta"

    elif PM10_value >= 200:
        PM10_mean_cathegory_label = "Emergenziale"
        PM10_mean_cathegory = "sesta"

    else:
        PM10_mean_cathegory_label = "No data"
        PM10_mean_cathegory = None

    return (PM10_mean_cathegory_label, PM10_mean_cathegory)



def evaluate_PM25(PM25_value):

    # categorie di qualità dell'aria rispetto a PM 2.5

    if PM25_value <= 10:
        PM25_mean_cathegory_label = "Ottima"
        PM25_mean_cathegory = "prima"

    elif PM25_value >= 10 and PM25_value  <= 20:
        PM25_mean_cathegory_label = "Buona"
        PM25_mean_cathegory = "seconda"
    
    elif PM25_value >= 20 and PM25_value  <= 25:
        PM25_mean_cathegory_label = "Accettabile"
        PM25_mean_cathegory = "terza"

    elif PM25_value >= 25 and PM25_value  <= 50:
        PM25_mean_cathegory_label = "Fuori legge"
        PM25_mean_cathegory = "quarta"

    elif PM25_value >= 50 and PM25_value  <= 100:
        PM25_mean_cathegory_label = "Pericolosa"
        PM25_mean_cathegory = "quinta"

    elif PM25_value >= 100:
        PM25_mean_cathegory_label = "Emergenziale"
        PM25_mean_cathegory = "sesta"

    else:
        PM25_mean_cathegory_label = "No_data"
        PM25_mean_cathegory = None

    return (PM25_mean_cathegory_label, PM25_mean_cathegory)


def evaluate_PM_in_HistoricalDatapoints_elements(records_serie_storica):

    # evaluate pm mean values into cathegories to add them to the series
    list_of_PM10_mean_cathegory_label = list()
    list_of_PM10_mean_cathegory = list()
    list_of_PM25_mean_cathegory_label = list()
    list_of_PM25_mean_cathegory = list()

    for i in records_serie_storica:

        PM10_mean_cathegory_label, PM10_mean_cathegory = evaluate_PM10(i.PM10_mean)
        PM25_mean_cathegory_label, PM25_mean_cathegory = evaluate_PM25(i.PM25_mean)

        list_of_PM10_mean_cathegory_label.append(PM10_mean_cathegory_label)
        list_of_PM10_mean_cathegory.append(PM10_mean_cathegory)
        list_of_PM25_mean_cathegory_label.append(PM25_mean_cathegory_label)
        list_of_PM25_mean_cathegory.append(PM25_mean_cathegory)

    results_dict = {
        "list_of_PM10_mean_cathegory_label": list_of_PM10_mean_cathegory_label,
        "list_of_PM10_mean_cathegory": list_of_PM10_mean_cathegory,
        "list_of_PM25_mean_cathegory_label": list_of_PM25_mean_cathegory_label,
        "list_of_PM25_mean_cathegory": list_of_PM25_mean_cathegory
    }

    return results_dict

