# servono a convert_timezone
import datetime
import pytz
import time


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
def add_hours_to_array(date_and_time_input_array, hours):

    hours_added = datetime.timedelta(hours = hours)

    future_date_and_time = [ i + hours_added for i in date_and_time_input_array ]

    return future_date_and_time



def fix_timezone_mismatch_in_array_of_datetimes(date_and_time_input_array):

    # se è attiva l'ora legale nel tempo locale
    if time.localtime().tm_isdst != 0:        
        hours = -time.timezone/3600 + 1

    elif time.localtime().tm_isdst == 0:
        hours = -time.timezone/3600

    future_date_and_time = add_hours_to_array(date_and_time_input_array, hours)

    return future_date_and_time