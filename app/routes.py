from flask import render_template, redirect
from app import app
from app.forms import UserInitialConfiguration
from app.Calculations import calculate_schedules


@app.route('/', methods=['GET','POST'])
def index():
    form = UserInitialConfiguration()
    if form.validate_on_submit():
        print(type(form.end_hour.data))
        list_of_dates = calculate_schedules(form)
        return render_template('SchedulesTable.html', titulo='Folha Ponto', list_of_dates=list_of_dates, form=form)
    return render_template('FrontPage.html', titulo='Folha Ponto', form=form)
