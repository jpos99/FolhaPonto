from os.path import exists
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from tkinter import filedialog
import streamlit as lt
import random

csv_file = ''


def colect_dates():
    data_inicio = input("inserir data inicial (dd-mm-yyyy) : ")
    data_inicio = datetime.strptime(data_inicio, '%d-%m-%Y').date()

    return data_inicio


def calculate_end_date(data_inicio):
    data_fim = data_inicio + relativedelta(months=1) - relativedelta(days=1)

    return data_fim


def ask_for_csv_file_name_with_path():
    global csv_file
    if len(csv_file) == 0:
        csv_file = filedialog.asksaveasfilename()
    return csv_file


def verify_if_csv_file_exsists():
    if exists(csv_file):
        tabela_horarios = open(csv_file, 'a')
        return tabela_horarios

    else:
        create_csv_file()


def create_csv_file():
    tabela_horarios = open(csv_file, 'w')

    return tabela_horarios


def format_into_hour_minute(valor_float):
    hour = int(valor_float)
    minutes = int((valor_float % 1) * 60)
    hour = str(hour).zfill(2)

    minutes = str(minutes).zfill(2)
    horario = f'{hour}:{minutes}'

    return horario


def calculate_day_working_schedule():
    gap_in_minutes = 5
    start_hour = random.randint(((9 * 60) - gap_in_minutes), ((9 * 60) + gap_in_minutes)) / 60
    out_to_break = random.randint(((12 * 60) - gap_in_minutes), ((12 * 60) + gap_in_minutes)) / 60
    in_from_break = random.randint(((13 * 60) - gap_in_minutes), ((13 * 60) + gap_in_minutes)) / 60
    stop_hour = random.randint(((18 * 60) - gap_in_minutes), ((18 * 60) + gap_in_minutes)) / 60
    aceptable = False

    while not aceptable:
        start_hour = round(random.randint(((9 * 60) - gap_in_minutes), ((9 * 60) + gap_in_minutes)) / 60, 2)
        out_to_break = round(random.randint(((12 * 60) - gap_in_minutes), ((12 * 60) + gap_in_minutes)) / 60, 2)
        in_from_break = round(random.randint(((13 * 60) - gap_in_minutes), ((13 * 60) + gap_in_minutes)) / 60, 2)
        stop_hour = round(random.randint(((18 * 60) - gap_in_minutes), ((18 * 60) + gap_in_minutes)) / 60, 2)

        if 8.15 > (stop_hour - in_from_break) + (out_to_break - start_hour) > 7.85 \
                and ((stop_hour - in_from_break) + (out_to_break - start_hour)) != 8:
            aceptable = True

    start_hour_str = format_into_hour_minute(start_hour)

    out_to_break_str = format_into_hour_minute(out_to_break)

    in_from_break_str = format_into_hour_minute(in_from_break)

    stop_hour_str = format_into_hour_minute(stop_hour)

    linha_horarios = f'{start_hour_str};{out_to_break_str};{in_from_break_str};{stop_hour_str}\n'

    return linha_horarios


def write_to_csv(linha_horarios):
    tabela_horarios = verify_if_csv_file_exsists()
    tabela_horarios.write(linha_horarios)
    tabela_horarios.close()


def monta_tabela_horarios(day, data_fim):
    while day <= data_fim:
        day_to_write = day.strftime('%d/%m/%Y')
        line_to_write = f'{day_to_write};'
        print(line_to_write)
        if 5 > day.weekday():

            linha_horarios = calculate_day_working_schedule()
            line_to_write = line_to_write + linha_horarios
            write_to_csv(line_to_write)

            day = day + timedelta(days=1)

        else:
            linha_horarios = '\n'
            line_to_write = line_to_write + linha_horarios
            write_to_csv(line_to_write)
            day = day + timedelta(days=1)



def get_user_config():
    config = open('UserConfig.txt', 'r').readlines()
    nome = config[0].replace('nome:', '').replace('\n', '').strip()
    funcao = config[1].replace('função:', '').replace('\n', '').strip()
    dict_company = {(config[0].split(':')[0]): (config[0].split(':')[1].replace('\n', '').strip()),
                    (config[1].split(':')[0]): (config[1].split(':')[1].replace('\n', '').strip()),
                    (config[2].split(':')[0]): (config[2].split(':')[1].replace('\n', '').strip()),
                    (config[3].split(':')[0]): (config[3].split(':')[1].replace('\n', '').strip())}
    return nome, funcao, dict_company


def main():
    day = colect_dates()
    data_fim = calculate_end_date(day)
    ask_for_csv_file_name_with_path()
    monta_tabela_horarios(day,data_fim)


main()
