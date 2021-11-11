from flask import Flask, render_template, request, url_for, redirect
from FolhaPonto import *

app = Flask(__name__)


@app.route('/')
def inicio():
    return render_template('FrontPage.html', titulo='Folha Ponto')


@app.route('/get_config', methods=['POST',])
def get_config():
    minutes_of_tolerance = request.form['tolerancia']
    hours_day = request.form['horas-dia']
    extra_hours_day = request.form['horas-extra']
    #date_of_begin = request.form['calendario-inicio']
    #date_of_end = request.form['calendario-fim']
    print(minutes_of_tolerance, hours_day, extra_hours_day)
    return redirect('/')

app.run(host='127.0.0.1', port=15000)


def motor():
    day = colect_dates()
    data_fim = calculate_end_date(day)
    # cabecalho = header_assembler(day,data_fim)
    ask_for_csv_file_name_with_path()
    # write_to_csv(cabecalho)
    monta_tabela_horarios(day, data_fim)