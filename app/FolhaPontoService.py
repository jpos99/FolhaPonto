from datetime import time
from random import randint


class Schedules:
    def __init__(self):
        self.start_hour = ''
        self.out_to_lunch = ''
        self.in_from_lunch = ''
        self.stop_hour = ''

    def calculate_day_working_schedules(self, configuration):
        aceptable_schedules = False
        while not aceptable_schedules:
            self.start_hour = self.randomize_schedule(
                self.convert_schedules_in_minutes(configuration.initial_work_hour), configuration)
            self.out_to_lunch = self.randomize_schedule(
                self.convert_schedules_in_minutes(configuration.initial_lunch_hour), configuration)
            self.in_from_lunch = self.randomize_schedule(
                self.convert_schedules_in_minutes(configuration.final_lunch_hour), configuration)
            self.stop_hour = self.randomize_schedule(
                self.convert_schedules_in_minutes(configuration.final_work_hour), configuration)
            aceptable_schedules = self.validate_aceptable_schedules(configuration)
        self.start_hour = self.convert_to_time(self.start_hour)
        self.stop_hour = self.convert_to_time(self.stop_hour)
        self.out_to_lunch = self.convert_to_time(self.out_to_lunch)
        self.in_from_lunch = self.convert_to_time(self.in_from_lunch)
        return self.start_hour, self.out_to_lunch, self.in_from_lunch, self.stop_hour

    @staticmethod
    def convert_to_time(schedule_in_minutes):
        return time.strftime(time((schedule_in_minutes // 60), (schedule_in_minutes % 60)), '%H:%M')

    @staticmethod
    def randomize_schedule(schedule, configuration):
        randomized_schedule = randint((schedule - configuration.minutes_of_tolerance),
                                      (schedule + configuration.minutes_of_tolerance))
        return randomized_schedule

    @staticmethod
    def convert_schedules_in_minutes(schedule):
        schedule_in_minutes = (schedule.hour * 60) + schedule.minute
        return schedule_in_minutes

    def validate_aceptable_schedules(self, configuration):
        worked_minutes = self.calculate_worked_hours()
        if configuration.day_work_minutes + configuration.minutes_of_tolerance > \
                worked_minutes \
                > configuration.day_work_minutes - configuration.minutes_of_tolerance:
            return True
        return False

    def calculate_worked_hours(self):
        return int(self.out_to_lunch) - int(self.start_hour) + int(self.stop_hour) - int(self.in_from_lunch)
