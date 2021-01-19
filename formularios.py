from wtforms import Form
from wtforms import StringField, TextField
from wtforms.validators import DataRequired

class Formulario (Form):
    date = StringField('date')
    time = StringField('time')
    f_currency = TextField('from_currency')
    f_quantity = TextField('from_quantity')
    t_currency = TextField('to_currency')
    t_currency = TextField('to_quantity')
    PU = TextField('PU')