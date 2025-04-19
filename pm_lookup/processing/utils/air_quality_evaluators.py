



def evaluate_PM10(PM10_value):

    # categorie di qualità dell'aria rispetto a PM 10

    if PM10_value <= 20:
        PM10_mean_cathegory_label = "Ottima"
        PM10_mean_cathegory = 1

    elif PM10_value >= 20 and PM10_value  <= 35:
        PM10_mean_cathegory_label = "Buona"
        PM10_mean_cathegory = 2
    
    elif PM10_value >= 35 and PM10_value  <= 50:
        PM10_mean_cathegory_label = "Accettabile"
        PM10_mean_cathegory = 3

    elif PM10_value >= 50 and PM10_value  <= 100:
        PM10_mean_cathegory_label = "Fuori legge"
        PM10_mean_cathegory = 4

    elif PM10_value >= 100 and PM10_value  <= 200:
        PM10_mean_cathegory_label = "Pericolosa"
        PM10_mean_cathegory = 5

    elif PM10_value >= 200:
        PM10_mean_cathegory_label = "Emergenziale"
        PM10_mean_cathegory = 6

    else:
        PM10_mean_cathegory_label = "No data"
        PM10_mean_cathegory = None

    return (PM10_mean_cathegory_label, PM10_mean_cathegory)



def evaluate_PM25(PM25_value):

    # categorie di qualità dell'aria rispetto a PM 2.5

    if PM25_value <= 10:
        PM25_mean_cathegory_label = "Ottima"
        PM25_mean_cathegory = 1

    elif PM25_value >= 10 and PM25_value  <= 20:
        PM25_mean_cathegory_label = "Buona"
        PM25_mean_cathegory = 2
    
    elif PM25_value >= 20 and PM25_value  <= 25:
        PM25_mean_cathegory_label = "Accettabile"
        PM25_mean_cathegory = 3

    elif PM25_value >= 25 and PM25_value  <= 50:
        PM25_mean_cathegory_label = "Fuori legge"
        PM25_mean_cathegory = 4

    elif PM25_value >= 50 and PM25_value  <= 100:
        PM25_mean_cathegory_label = "Pericolosa"
        PM25_mean_cathegory = 5

    elif PM25_value >= 100:
        PM25_mean_cathegory_label = "Emergenziale"
        PM25_mean_cathegory = 6

    else:
        PM25_mean_cathegory_label = "No_data"
        PM25_mean_cathegory = None

    return (PM25_mean_cathegory_label, PM25_mean_cathegory)


def evaluate_PM_in_HistoricalDatapoints_elements(records_serie_storica):

    # evaluate pm mean values into cathegories to add them to the series
    PM10_mean_cathegory_label_records_serie_storica = list()
    PM10_mean_cathegory_records_serie_storica = list()
    PM25_mean_cathegory_label_records_serie_storica = list()
    PM25_mean_cathegory_records_serie_storica = list()

    for i in records_serie_storica:
        PM10_mean_cathegory_label, PM10_mean_cathegory = evaluate_PM10(i.PM10_mean)
        PM25_mean_cathegory_label, PM25_mean_cathegory = evaluate_PM25(i.PM25_mean)

        PM10_mean_cathegory_label_records_serie_storica.append(PM10_mean_cathegory_label)
        PM10_mean_cathegory_records_serie_storica.append(PM10_mean_cathegory)
        PM25_mean_cathegory_label_records_serie_storica.append(PM25_mean_cathegory_label)
        PM25_mean_cathegory_records_serie_storica.append(PM25_mean_cathegory)

    results_dict = {
        "PM10_mean_cathegory_label_records_serie_storica": PM10_mean_cathegory_label_records_serie_storica,
        "PM10_mean_cathegory_records_serie_storica": PM10_mean_cathegory_records_serie_storica,
        "PM25_mean_cathegory_label_records_serie_storica": PM25_mean_cathegory_label_records_serie_storica,
        "PM25_mean_cathegory_records_serie_storica": PM25_mean_cathegory_records_serie_storica
    }

    return results_dict

