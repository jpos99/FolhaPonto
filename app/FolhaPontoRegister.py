from datetime import timedelta
from dateutil.relativedelta import relativedelta
from app.FolhaPontoService import Schedules


class FullDay:

    def __init__(self, date, configuration):
        self.date = date
        self.week_day = date.weekday()
        self.day_schedules = Schedules()
        if self.is_work_day(configuration):
            self.day_schedules = self.day_schedules.calculate_day_working_schedules(configuration)

    def is_work_day(self, configuration):
        work_day = False
        if configuration.work_on_saturday:
            if self.date.weekday() < 6:
                work_day = True
        if self.date.weekday() < 5:
            work_day = True
        return work_day


class WorkedDates:
    def __init__(self, configuration):
        self.initial_date = configuration.initial_date
        self.final_date = configuration.final_date
        self.saturday_worked = configuration.work_on_saturday
        self.list_of_dates = []

    def calculate_end_date(self):
        if self.final_date is None:
            self.final_date = self.initial_date + relativedelta(months=1) - relativedelta(days=1)

    def assemble_days_list(self, configuration):
        day = self.initial_date
        self.calculate_end_date()
        while day <= self.final_date:
            full_day = FullDay(day, configuration)
            self.list_of_dates.append(full_day)
            day += timedelta(days=1)
        return self.list_of_dates
