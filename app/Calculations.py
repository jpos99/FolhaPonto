from datetime import timedelta, time, datetime
from dateutil.relativedelta import relativedelta
from app.FolhaPontoMODELS import fullDay
import random

'''
quem é responsavel pelo que? (calculo, resposta e configuração...)
'''


def calculate_schedules(form):
    form.date_of_end.data = calculate_end_date(form.date_of_begin.data, form.date_of_end.data)
    form.day_work_minutes.data = calculate_day_work_hours(form)
    return assemble_days_list(form)


def calculate_end_date(initial_date, date_of_end):
    if date_of_end == '':
        return initial_date + relativedelta(months=1) - relativedelta(days=1)
    return date_of_end


def calculate_day_work_hours(form):
    return period_work_hours(
            convert_schedules_in_minutes(form.begin_lunch.data), convert_schedules_in_minutes(form.begin_hour.data)) + \
            period_work_hours(
            convert_schedules_in_minutes(form.end_hour.data), convert_schedules_in_minutes(form.end_lunch.data))


def convert_schedules_in_minutes(schedule):
    print(type(schedule))
    schedule_in_minutes = (schedule.hour * 60) + schedule.minute
    return schedule_in_minutes


def period_work_hours(end_hour, start_hour):
    return end_hour - start_hour


def assemble_days_list(form):
    list_of_dates = []
    day = form.date_of_begin.data
    while day <= form.date_of_end.data:
        full_day = fullDay(day, form)
        calculate_day_working_schedules(form, full_day)
        list_of_dates.append(full_day)
        day += timedelta(days=1)
    return list_of_dates


def calculate_day_working_schedules(form, full_day):
    aceptable_schedules = False
    if is_work_day(form.work_on_saturday.data, full_day):
        while not aceptable_schedules:
            full_day.start_hour = randomize_schedule(form.begin_hour.data, form.tolerance_in_minutes.data, full_day.date)
            full_day.out_to_lunch = randomize_schedule(form.begin_lunch.data, form.tolerance_in_minutes.data, full_day.date)
            full_day.in_from_lunch = randomize_schedule(form.end_lunch.data, form.tolerance_in_minutes.data, full_day.date)
            full_day.stop_hour = randomize_schedule(form.end_hour.data, form.tolerance_in_minutes.data, full_day.date)
            aceptable_schedules = validate_aceptable_schedules(full_day, form)


def is_work_day(saturday, full_day):
    work_day = False
    if saturday:
        if full_day.date.weekday() < 6:
            work_day = True
    if full_day.date.weekday() < 5:
        work_day = True
    return work_day


def randomize_schedule(schedule, tolerance, date):
    randomized_schedule = random.randint((convert_schedules_in_minutes(schedule) - tolerance),
                                         (convert_schedules_in_minutes(schedule) + tolerance))
    return convert_to_date(randomized_schedule, date)


def convert_to_date(schedule_in_minutes, date):
    schedule = time((schedule_in_minutes // 60), (schedule_in_minutes % 60))
    return datetime.combine(date, schedule)


def validate_aceptable_schedules(full_day, form):
    if form.day_work_minutes.data + form.tolerance_in_minutes.data > calculate_worked_hours(full_day) > \
            form.day_work_minutes.data - form.tolerance_in_minutes.data:
        return True
    return False


def calculate_worked_hours(full_day):
    return (convert_schedules_in_minutes(full_day.out_to_lunch) - convert_schedules_in_minutes(full_day.start_hour)) + \
           (convert_schedules_in_minutes(full_day.stop_hour) - convert_schedules_in_minutes(full_day.in_from_lunch))


def is_british_hour(schedule):
    if schedule.minute == 0:
        return True
    return False
