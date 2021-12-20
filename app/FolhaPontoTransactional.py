class UserConfiguration:

    def __init__(self, form):
        self.initial_date = form.date_of_begin.data
        self.final_date = form.date_of_end.data
        self.work_on_saturday = form.work_on_saturday.data
        self.minutes_of_tolerance = form.tolerance_in_minutes.data
        self.initial_work_hour = form.begin_hour.data
        self.initial_lunch_hour = form.begin_lunch.data
        self.final_lunch_hour = form.end_lunch.data
        self.final_work_hour = form.end_hour.data
        self.day_work_minutes = form.day_work_minutes.data
