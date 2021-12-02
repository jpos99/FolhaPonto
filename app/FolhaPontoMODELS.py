from datetime import timedelta, time
from random import randint
from dateutil.relativedelta import relativedelta


class FullDay:

    def __init__(self, date, form):
        self.date = date
        self.week_day = date.weekday()
        self.day_schedules = []

        self.start_hour = ''
        self.out_to_lunch = ''
        self.in_from_lunch = ''
        self.stop_hour = ''
        if self.is_work_day:
            self.calculate_day_working_schedules(form)

    def is_work_day(self, form):
        work_day = False
        if form.work_on_saturday:
            if self.date.weekday() < 6:
                work_day = True
        if self.date.weekday() < 5:
            work_day = True
        return work_day

class WorkedDates:
    def __init__(self, form):
        self.initial_date = form.date_of_begin.data
        self.final_date = form.date_of_end.data
        self.saturday_worked = form.work_on_saturday.data
        self.list_of_dates = []

    def calculate_end_date(self):
        if self.final_date is None:
            self.final_date = self.initial_date + relativedelta(months=1) - relativedelta(days=1)

    def assemble_days_list(self, form):
        day = self.initial_date
        self.calculate_end_date()
        while day <= self.final_date:
            full_day = FullDay(day, form)
            self.list_of_dates.append(full_day)
            day += timedelta(days=1)
        return self.list_of_dates

class Schedules:
    def __init__(self):
        self.start_hour = ''
        self.out_to_lunch = ''
        self.in_from_lunch = ''
        self.stop_hour = ''

    def calculate_day_working_schedules(self, form):
        aceptable_schedules = False
        print(type(form.tolerance_in_minutes.data))
        while not aceptable_schedules:
            self.start_hour = self.randomize_schedule(self.convert_schedules_in_minutes(form.begin_hour.data),form)
            self.out_to_lunch = self.randomize_schedule(self.convert_schedules_in_minutes(form.begin_lunch.data),form)
            self.in_from_lunch = self.randomize_schedule(self.convert_schedules_in_minutes(form.end_lunch.data),form)
            self.stop_hour = self.randomize_schedule(self.convert_schedules_in_minutes(form.end_hour.data),form)
            aceptable_schedules = self.validate_aceptable_schedules(form)
        self.start_hour = self.convert_to_time(self.start_hour)
        self.stop_hour = self.convert_to_time(self.stop_hour)
        self.out_to_lunch = self.convert_to_time(self.out_to_lunch)
        self.in_from_lunch = self.convert_to_time(self.in_from_lunch)

    @staticmethod
    def convert_to_time(schedule_in_minutes):
        return time.strftime(time((schedule_in_minutes // 60), (schedule_in_minutes % 60)), '%H:%M')

    @staticmethod
    def randomize_schedule(schedule, form):
        randomized_schedule = randint((schedule - form.tolerance_in_minutes.data),
                                      (schedule + form.tolerance_in_minutes.data))
        return randomized_schedule

    @staticmethod
    def convert_schedules_in_minutes(schedule):
        print(schedule)
        schedule_in_minutes = (schedule.hour * 60) + schedule.minute
        return schedule_in_minutes

    def validate_aceptable_schedules(self, form):
        worked_minutes = self.calculate_worked_hours()
        if form.day_work_minutes.data + form.tolerance_in_minutes.data > \
                worked_minutes \
                > form.day_work_minutes.data - form.tolerance_in_minutes.data:
            return True
        return False

    def calculate_worked_hours(self):
        return self.out_to_lunch - self.start_hour + self.stop_hour - self.in_from_lunch