from flask import Flask, render_template, request, url_for, redirect
from FolhaPonto import *

app = Flask(__name__)


def calculate_schedules(dict_config):
    initial_date = convert_str_to_date(dict_config["date_of_begin"])
    final_date = calculate_end_date(initial_date, dict_config["date_of_end"])
    list_of_days = assemble_days_list(initial_date,final_date)
    return assemble_period_schedules(dict_config, list_of_days)
    # monta_tabela_horarios(fullDay, data_fim)


@app.route('/')
def inicio():
    return render_template('FrontPage.html', titulo='Folha Ponto')


@app.route('/generate_hours_table', methods=['POST',])
def generate_hours_table():

    minutes_of_tolerance = request.form['tolerancia']
    if request.form.get("sabados"):
        has_saturday = 5
    else:
        has_saturday = 4
    print(has_saturday)
    date_of_begin = request.form['calendario-inicio']
    date_of_end = request.form['calendario-fim']
    begin_hour = request.form['inicio-expediente']
    begin_lunch = request.form['inicio-almoco']
    end_lunch = request.form['termino-almoco']
    end_hour = request.form['termino-expediente']

    dict_config = {"date_of_end": date_of_end, "date_of_begin": date_of_begin, "tolerance": minutes_of_tolerance,
                   "has_saturday": has_saturday, "begin_hour": begin_hour,"begin_lunch": begin_lunch,
                   "end_lunch":end_lunch, "end_hour": end_hour}
    print(dict_config["begin_hour"])
    list_of_dates = calculate_schedules(dict_config)
    #print(list_of_dates)

    return render_template('SchedulesTable.html', titulo='Folha Ponto', list_of_dates=list_of_dates)


app.run(host='127.0.0.1', port=15000)
