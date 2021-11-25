from flask_wtf import FlaskForm
from wtforms import TimeField, DateField, IntegerField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime


class UserInitialConfiguration(FlaskForm):
    date_of_begin = DateField('Data Inicial', validators=[DataRequired()])
    date_of_end = DateField('Data Final')
    work_on_saturday = BooleanField('considerar os sabados?')
    tolerance_in_minutes = IntegerField('Minutos de tolerancia no dia', default=10)
    begin_hour = TimeField('inicio expediente às', default=datetime.strptime("09:00", "%H:%M" ))
    begin_lunch = TimeField('inicio almoço às', default=datetime.strptime("12:00", "%H:%M" ))
    end_lunch = TimeField('fim almoço às', default=datetime.strptime("13:00", "%H:%M" ))
    end_hour = TimeField('fim expediente às', default=datetime.strptime("18:00", "%H:%M" ))
    day_work_minutes = IntegerField()
    submit = SubmitField('Calcular horarios')