from os.path import exists
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from tkinter import filedialog
import random


class Calendar:

    def colect_date(self):
        self.begin_date = input("inserir data inicial (dd-mm-yyyy) : ")
        self.begin_date = datetime.strptime(data_inicio, '%d-%m-%Y').date()
        return self.begin_date

    def __calculate_end_date(data_inicio):
        ending_date = data_inicio + relativedelta(months=1) - relativedelta(days=1)

        return ending_date


class Scheduler:
    while day <= data_fim:
        day_to_write = day.strftime('%d/%m/%Y')
        line_to_write = f'{day_to_write};'
        if 5 > day.weekday():

            linha_horarios = calculate_working_hours()
            line_to_write = line_to_write + linha_horarios
            write_to_csv(line_to_write)

            day = day + timedelta(days=1)

        else:
            linha_horarios = '\n'
            line_to_write = line_to_write + linha_horarios
            write_to_csv(line_to_write)
            day = day + timedelta(days=1)
