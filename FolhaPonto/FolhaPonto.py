from os.path import exists
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import tkinter
from tkinter import filedialog
import random
arquivo_csv = ''

def coleta_datas():

    data_inicio = input("inserir data inicial (dd-mm-yyyy) : ")
    data_inicio = datetime.strptime(data_inicio, '%d-%m-%Y').date()
    data_fim = data_inicio + relativedelta(months=1) - relativedelta(days=1)
    #print(f'coletei {data_inicio} e {data_fim}')
    return data_inicio, data_fim


def verifica_arquivo():
    global arquivo_csv
    if len(arquivo_csv) == 0:
        arquivo_csv= filedialog.askopenfilename()
    if exists(arquivo_csv):
        tabela_horarios = open(arquivo_csv, 'a')
        return tabela_horarios

    tabela_horarios = open(arquivo_csv, 'w')

    return tabela_horarios


def transforma_em_horario(valor_float):
    hora = int(valor_float)
    minuto = int((valor_float % 1)*60)
    hora = str(hora).zfill(2)

    minuto = str(minuto).zfill(2)
    horario = f'{hora}:{minuto}'
    #print('transformou em horario', )
    return horario


def calcula_horarios():
    gap = 7
    start_hour = random.randint(((9 * 60) - gap), ((9 * 60) + gap)) / 60
    out_to_break = random.randint(((12 * 60) - gap), ((12 * 60) + gap)) / 60
    in_from_break = random.randint(((13 * 60) - gap), ((13 * 60) + gap)) / 60
    stop_hour = random.randint(((18 * 60) - gap), ((18 * 60) + gap)) / 60
    aceitavel = False
    #print("calcula horarios")
    while not aceitavel:

        gap = 7
        start_hour = round(random.randint(((9 * 60) - gap), ((9 * 60) + gap)) / 60, 2)
        out_to_break = round(random.randint(((12 * 60) - gap), ((12 * 60) + gap)) / 60, 2)
        in_from_break = round(random.randint(((13 * 60) - gap), ((13 * 60) + gap)) / 60, 2)
        stop_hour = round(random.randint(((18 * 60) - gap), ((18 * 60) + gap)) / 60, 2)

        if 8.1 > (stop_hour - in_from_break) + (out_to_break - start_hour) > 7.9 and ((stop_hour - in_from_break) + (out_to_break - start_hour)) != 8 :
            aceitavel = True
    #print(start_hour, out_to_break, in_from_break, stop_hour)
    start_hour_str = transforma_em_horario(start_hour)

    out_to_break_str = transforma_em_horario(out_to_break)

    in_from_break_str = transforma_em_horario(in_from_break)

    stop_hour_str = transforma_em_horario(stop_hour)

    linha_horarios = f'{start_hour_str};{out_to_break_str};{in_from_break_str};{stop_hour_str}\n'

    return linha_horarios


def write_to_csv(linha_horarios):

    tabela_horarios = verifica_arquivo()
    tabela_horarios.write(linha_horarios)
    #print("gravei", str(linha_horarios))
    tabela_horarios.close()


def monta_tabela_horarios():

    day, data_fim = coleta_datas()
    #print("w csv")
    while day <= data_fim:
        #print("while day")
        if 5 > day.weekday():

            linha_horarios = calcula_horarios()
            write_to_csv(linha_horarios)
            day = day + timedelta(days=1)

        else:
            linha_horarios = '\n'
            write_to_csv(linha_horarios)
            day = day + timedelta(days=1)


def main():

    monta_tabela_horarios()
    exit()

main()
