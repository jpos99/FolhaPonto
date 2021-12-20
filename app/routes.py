from flask import render_template
from app import app
from app.forms import FormUserConfiguration
from app.FolhaPontoRegister import WorkedDates
from app.FolhaPontoTransactional import UserConfiguration


@app.route('/', methods=['GET', 'POST'])
def index():
    form = FormUserConfiguration()
    configuration = UserConfiguration(form)
    if form.validate_on_submit():
        period_of_dates = WorkedDates(configuration)
        list_of_dates = period_of_dates.assemble_days_list(configuration)
        return render_template('SchedulesTable.html', titulo='Folha Ponto', list_of_dates=list_of_dates, form=form)
    return render_template('FrontPage.html', titulo='Folha Ponto', form=form)
