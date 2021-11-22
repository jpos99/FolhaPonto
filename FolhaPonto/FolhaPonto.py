from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from FolhaPontoMODELS import fullDay
import random


def format_into_hour_minute(valor_in_minutes):
    if valor_in_minutes != '':
        hour = valor_in_minutes // 60
        minutes = int((valor_in_minutes % 60))
        hour = str(hour).zfill(2)
        minutes = str(minutes).zfill(2)
        return f'{hour}:{minutes}'
    return valor_in_minutes


def convert_str_to_date(date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    return date


def calculate_end_date(initial_date, date_of_end):
    if date_of_end == '':
        return initial_date + relativedelta(months=1) - relativedelta(days=1)
    return convert_str_to_date(date_of_end)


def assemble_days_list(day, final_date):
    list_of_dates = []
    while day <= final_date:
        list_of_dates.append(day)
        day += timedelta(days=1)
    return list_of_dates


def convert_strdate_to_intminutes(date_str):
    return int(date_str.split(':')[1]) + (int(date_str.split(':')[0]) * 60)


def randomizing_schedules(dict_config_in_minutes, date):
    date["start_hour"] = round(
        random.randint((dict_config_in_minutes["begin_hour"] - dict_config_in_minutes["tolerance"]),
                       (dict_config_in_minutes["begin_hour"] + dict_config_in_minutes["tolerance"])), 2)
    date["out_to_break"] = round(
        random.randint((dict_config_in_minutes["begin_lunch"] - dict_config_in_minutes["tolerance"]),
                       (dict_config_in_minutes["begin_lunch"] + dict_config_in_minutes["tolerance"])), 2)
    date["in_from_break"] = round(
        random.randint((dict_config_in_minutes["end_lunch"] - dict_config_in_minutes["tolerance"]),
                       (dict_config_in_minutes["end_lunch"] + dict_config_in_minutes["tolerance"])), 2)
    date["stop_hour"] = round(random.randint((dict_config_in_minutes["end_hour"] - dict_config_in_minutes["tolerance"]),
                                             (dict_config_in_minutes["end_hour"] + dict_config_in_minutes["tolerance"])), 2)
    return date


def convert_standard_schedules_in_minutes(dict_config):
    dict_config["tolerance"] = int(dict_config["tolerance"])
    dict_config["begin_hour"] = convert_strdate_to_intminutes(dict_config["begin_hour"])
    dict_config["begin_lunch"] = convert_strdate_to_intminutes(dict_config["begin_lunch"])
    dict_config["end_lunch"] = convert_strdate_to_intminutes(dict_config["end_lunch"])
    dict_config["end_hour"] = convert_strdate_to_intminutes(dict_config["end_hour"])
    return dict_config


def validate_aceptable_schedules(dict_config_in_minutes, date):
    if (dict_config_in_minutes["standard_work_hours"] + dict_config_in_minutes["tolerance"]) > (
            date["stop_hour"] - date["in_from_break"]) + (date["out_to_break"] - date["start_hour"]) > (
            dict_config_in_minutes["standard_work_hours"] - dict_config_in_minutes["tolerance"]) and (
            (date["stop_hour"] - date["in_from_break"]) + (date["out_to_break"] - date["start_hour"])) % 60 != 0:
        return True
    return False


def calculate_day_working_schedules(dict_config_in_minutes, date):
    if date["date"].weekday() > dict_config_in_minutes["has_saturday"]:
        date["start_hour"] = ''
        date["out_to_break"] = ''
        date["in_from_break"] = ''
        date["stop_hour"] = ''
        return date
    date = randomizing_schedules(dict_config_in_minutes, date)
    while not validate_aceptable_schedules(dict_config_in_minutes, date):
        date = randomizing_schedules(dict_config_in_minutes, date)
    return date


def assemble_period_schedules(dict_config, list_of_days):
    date = {}
    list_of_dates = []
    dict_config_in_minutes = convert_standard_schedules_in_minutes(dict_config)
    dict_config_in_minutes["standard_work_hours"] = (dict_config_in_minutes["begin_lunch"] - dict_config_in_minutes[
        "begin_hour"]) + (dict_config_in_minutes["end_hour"] - dict_config_in_minutes["end_lunch"])

    for day in list_of_days:
        date["date"] = day
        date = calculate_day_working_schedules(dict_config_in_minutes, date)
        date["date"] = day.strftime('%d/%m/%Y')
        date["start_hour"] = format_into_hour_minute(date["start_hour"])
        date["out_to_break"] = format_into_hour_minute(date["out_to_break"])
        date["in_from_break"] = format_into_hour_minute(date["in_from_break"])
        date["stop_hour"] = format_into_hour_minute(date["stop_hour"])
        date_obj = fullDay(date)
        list_of_dates.append(date_obj)
    return list_of_dates

def calculate_schedules(dict_config):
    initial_date = convert_str_to_date(dict_config["date_of_begin"])
    final_date = calculate_end_date(initial_date, dict_config["date_of_end"])
    list_of_days = assemble_days_list(initial_date,final_date)
    return assemble_period_schedules(dict_config, list_of_days)