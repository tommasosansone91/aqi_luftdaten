from datetime import datetime, timedelta
from django.utils import timezone

import numpy as np

from django.db.models import Avg

from pm_lookup.models import target_area_input_data
from pm_lookup.models import target_area_realtime_data
from pm_lookup.models import target_area_history_data
from pm_lookup.models import target_area_daily_time_serie

# importo i drawers
from pm_lookup.drawers.drawer1 import draw_timeserie_PM10_graph
from pm_lookup.drawers.drawer1 import draw_timeserie_PM25_graph

# per rivalutare le categorie di qualità dell'aria dei valori di mede giornalieri
from .auxiliary_processing import evaluate_PM10
from .auxiliary_processing import evaluate_PM25

# aggiunto per fixare il fatto che nei grafici è mostrato orario come se fosse in UTC
# errore sopraggiunto dopo il reset del db?
from pm_lookup.processing.auxiliary_processing import fix_timezone_mismatch_1


def arrange_daily_time_series_and_graphs():

    target_area_daily_time_serie.objects.all().delete()

    print("Eliminate tutte le serie storiche giornaliere in target_area_daily_time_serie!")

    # print("Inizio disposizione dati in serie storiche giornaliere per ogni località...")

    thirty_days_ago = timezone.now() - timedelta(days=30)
    today = timezone.now()


    for area_di_interesse in target_area_input_data.objects.all():

        print("Predisposizione dati ed elementi del grafico per la serie storica giornaliera per %s..." % area_di_interesse.Name)

        daily_data = {}
        current_date = thirty_days_ago.date()

        while current_date <= today.date():
            
            end_of_day = timezone.make_aware(datetime(current_date.year, current_date.month, current_date.day, 23, 59, 59))
            start_of_day = timezone.make_aware(datetime(current_date.year, current_date.month, current_date.day, 0, 0, 0))

            daily_records = target_area_history_data.objects.filter(
                Target_area_input_data=area_di_interesse,
                Last_update_time__gte=start_of_day,
                Last_update_time__lte=end_of_day,
            ).aggregate(
                avg_pm10=Avg('PM10_mean'),
                avg_pm25=Avg('PM25_mean'),
                avg_n_sensors=Avg('n_selected_sensors')
            )

            if daily_records['avg_pm10'] is not None and daily_records['avg_pm25'] is not None:
                daily_data[current_date] = {
                    'PM10_daily_mean': round(daily_records['avg_pm10'], 2),
                    'PM25_daily_mean': round(daily_records['avg_pm25'], 2),
                    'Mean_n_selected_sensors': round(daily_records['avg_n_sensors'], 2) if daily_records['avg_n_sensors'] is not None else 0,
                }
            else:
                daily_data[current_date] = {
                    'PM10_daily_mean': None,
                    'PM25_daily_mean': None,
                    'Mean_n_selected_sensors': 0,
                }

            current_date += timedelta(days=1)

        # Prepare data for the daily time series
        update_dates = list(daily_data.keys())
        pm10_daily_mean = [daily_data[d]['PM10_daily_mean'] for d in update_dates]
        pm25_daily_mean = [daily_data[d]['PM25_daily_mean'] for d in update_dates]
        mean_n_selected_sensors = [daily_data[d]['Mean_n_selected_sensors'] for d in update_dates]

        pm10_daily_quality = [evaluate_PM10(val)[0] if val is not None else "" for val in pm10_daily_mean]
        pm25_daily_quality = [evaluate_PM25(val)[0] if val is not None else "" for val in pm25_daily_mean]

        pm10_daily_cathegory = [evaluate_PM10(val)[1] if val is not None else "" for val in pm10_daily_mean]
        pm25_daily_cathegory = [evaluate_PM25(val)[1] if val is not None else "" for val in pm25_daily_mean]


        serie_storica = {
            "Target_area_input_data": area_di_interesse.Name,
            "Update_date": update_dates,
            "PM10_daily_mean": pm10_daily_mean,
            "PM25_daily_mean": pm25_daily_mean,
            "PM10_daily_quality": pm10_daily_quality,
            "PM25_daily_quality": pm25_daily_quality,
            "PM10_daily_cathegory": pm10_daily_cathegory,
            "PM25_daily_cathegory": pm25_daily_cathegory,
            "Mean_n_selected_sensors": mean_n_selected_sensors,
        }

        # time array
        time_values = np.array(serie_storica['Update_date'])

        # values
        PM10_values = np.array([val if val is not None else np.nan for val in serie_storica['PM10_daily_mean']])
        PM25_values = np.array([val if val is not None else np.nan for val in serie_storica['PM25_daily_mean']])

        # pm10 maxs
        PM10_daily_max_35_days_max = np.array([50 for i in time_values])

        # traccio i grafici e ottengo il javascript
        graph_PM10_title = f"Serie storiche giornaliere del PM10 per {area_di_interesse.Name}"
        graph_PM25_title = f"Serie storiche giornaliere del PM2.5 per {area_di_interesse.Name}"

        graph_PM10 = draw_timeserie_PM10_graph(time_values, PM10_values, PM10_daily_max_35_days_max=PM10_daily_max_35_days_max, graph_title=graph_PM10_title)
        graph_PM25 = draw_timeserie_PM25_graph(time_values, PM25_values, graph_title=graph_PM25_title)

        elementi_grafico = target_area_daily_time_serie(
            Target_area_input_data=target_area_input_data.objects.get(Name=area_di_interesse.Name),
            Record_time_values='[' + ', '.join(f'"{d.isoformat()}"' for d in serie_storica['Update_date']) + ']',
            PM10_mean_values='[' + ', '.join(str(e) if e is not None else 'null' for e in serie_storica['PM10_daily_mean']) + ']',
            PM25_mean_values='[' + ', '.join(str(e) if e is not None else 'null' for e in serie_storica['PM25_daily_mean']) + ']',
            PM10_quality_values='["' + '", "'.join(str(e) for e in serie_storica['PM10_daily_quality']) + '"]',
            PM25_quality_values='["' + '", "'.join(str(e) for e in serie_storica['PM25_daily_quality']) + '"]',
            PM10_cathegory_values='["' + '", "'.join(str(e) for e in serie_storica['PM10_daily_cathegory']) + '"]',
            PM25_cathegory_values='["' + '", "'.join(str(e) for e in serie_storica['PM25_daily_cathegory']) + '"]',
            n_selected_sensors_values='[' + ', '.join(str(e) for e in serie_storica['Mean_n_selected_sensors']) + ']',
            PM10_graph_div=graph_PM10,
            PM25_graph_div=graph_PM25,
        )


        elementi_grafico.save()

        print("Predisposti dati ed elementi del grafico per la serie storica giornaliera per %s!" % area_di_interesse.Name)  

    print("Predisposti dati ed elementi dei grafici per le serie storiche giornaliere per tutte le località!")  