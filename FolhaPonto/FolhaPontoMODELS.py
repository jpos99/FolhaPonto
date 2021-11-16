
class fullDay:
    def __init__(self, date):
        self.date = date["date"]
        self.start_hour = date["start_hour"]
        self.out_to_lunch = date["out_to_break"]
        self.in_from_lunch = date["in_from_break"]
        self.stop_hour = date["stop_hour"]
