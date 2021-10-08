from os.path import exists
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from tkinter import filedialog
from openpyxl.styles import Font
from openpyxl.worksheet.dimensions import RowDimension
import openpyxl
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
    minutes = int((valor_float % 1)*60)
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
    

def header_assembler(data_inicio, data_fim):
    wb = openpyxl.Workbook()
    xlsx_file = 'FolhaPonto.xlsx'

    nome, funcao, dict_company = get_user_config()
    print(dict_company.keys())
    mes_ano = (data_inicio + relativedelta(months=1)).strftime('%b-%y')
    ws = wb.create_sheet(f'{mes_ano}')

    print(ws.row_dimensions)
    ws.calculate_dimension()
    data_inicio = data_inicio.strftime('%d/%m/%Y')
    data_fim = data_fim.strftime('%d/%m/%Y')

    ws.column_dimensions['A'].width = 13
    ws.column_dimensions['B'].width = 13
    ws.column_dimensions['C'].width = 13
    ws.column_dimensions['D'].width = 13
    ws.column_dimensions['E'].width = 13
    ws.column_dimensions['F'].width = 13

    line_1_font = Font(name='Calibri', size = 18, bold = True, color = 'FF000000')
    ws['A1'].font = line_1_font
    ws['A1'] = 'FOLHA PONTO'

    ws['D1'].font = line_1_font
    ws['D1'] = 'CNPJ :'

    ws['E1'].font = line_1_font
    ws['E1'] = f"{dict_company['cnpj']}"


    line_2_font = Font(name='Calibri', size=16, bold=True, color='FF000000')
    ws['A2'].font = line_2_font
    ws['A2'] = f"{dict_company['nome_fantasia']}"

    line_3_font = Font(name='Calibri', size=14, bold=True, color='FF000000')
    ws['A3'].font = line_3_font
    ws['A3'] = f"{'Nome'} : {dict_company['nome']}"

    ws['E3'].font = line_3_font
    ws['E3'] = f"{'Funç'} : {dict_company['funcao']}"

    line_4_font = Font(name='Calibri', size=14, bold=True, color='FF000000')
    ws['A4'].font = line_4_font
    ws['A4'] = f"{mes_ano}"

    ws['D4'].font = line_4_font
    ws['D4'] = f"{data_inicio} à {data_fim}"

    line_5_font = Font(name='Calibri', size=12, bold=True, color='FF000000')
    ws['A5'].font = line_5_font
    ws['A5'] = 'Data'
    ws['B5'].font = line_5_font
    ws['B5'] = 'Horário de\nEntrada'
    ws['C5'].font = line_5_font
    ws['C5'] = 'Entrada no\nIntervalo'
    ws['D5'].font = line_5_font
    ws['D5'] = 'Saída do\nIntervalo'
    ws['E5'].font = line_5_font
    ws['E5'] = 'Hoarario de\nSaída'

    ws.row_dimensions[1].height = 25
    ws.row_dimensions[2].height = 20
    ws.row_dimensions[3].height = 20
    ws.row_dimensions[4].height = 20
    ws.row_dimensions[5].height = 40

    wb.save(xlsx_file)
    linha4 = f'{mes_ano};;;{data_inicio}; a ;{data_fim}\n'
    linha5 = 'Data;Horário de Entrada;Entrada no Intervalo;Saida do Intervalo;Horŕio de Saída; Stand by\n'

    cabecalho = linha1 + linha2 + linha3 + linha4 + linha5
    print(cabecalho)
    return cabecalho


def get_user_config():
    config = open('UserConfig.txt', 'r').readlines()
    nome = config[0].replace('nome:', '').replace('\n', '').strip()
    funcao = config[1].replace('função:', '').replace('\n', '').strip()
    dict_company = {(config[0].split(':')[0]):(config[0].split(':')[1].replace('\n', '').strip()),
                    (config[1].split(':')[0]):(config[1].split(':')[1].replace('\n', '').strip()),
                    (config[2].split(':')[0]):(config[2].split(':')[1].replace('\n', '').strip()),
                    (config[3].split(':')[0]):(config[3].split(':')[1].replace('\n', '').strip())}
    return nome, funcao, dict_company

def main():

    
    day = colect_dates()
    data_fim = calculate_end_date(day)
    cabecalho = header_assembler(day,data_fim)
    #ask_for_csv_file_name_with_path()
    #write_to_csv(cabecalho)
    #monta_tabela_horarios(day,data_fim)
    #footer = footer_assembler()
    #write_to_csv(footer)
    exit()

main()
