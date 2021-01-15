from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField, TextField, FloatField, DateField, DateTimeField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Length
from movimientos.api import Crypto


class MovementForm (FlaskForm):
    crypto10 = Crypto()
    listaCrypto = crypto10.get10Crypto()
    print (listaCrypto)

    date = DateField('date')
    time = DateTimeField('time')
    from_currency = SelectField('from_currency', choices=listaCrypto, validators=[DataRequired(message='valor requerido')]) # los validadores de la clase Forms hay que ponerles parentesis. los que creeemos nosotros no hay quen ponerle el parentesis
    from_quantity = SelectField('from_quantity', choices=[('BTC, XRP, BCH, USDT, BSV, ADA,')], validators=[DataRequired(message='valor requerido')]) 
    to_currency = FloatField('to_currency')
    to_quantity = FloatField('to_quantity')
    PU = FloatField('PU')

    submit = SubmitField('Ok')
