from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectMultipleField, TextField, FloatField, DateField, DateTimeField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Length
from movimientos.api import Crypto


class MovementForm (FlaskForm):
    listofdates = Crypto()
    date = DateField('date')
    time = DateTimeField('time')
    from_currency = SelectMultipleField('from_currency', choices=[('EUR, ETH, LTC, BNB, EOS, XLM, TRX')], validators=[DataRequired(message='valor requerido')]) # los validadores de la clase Forms hay que ponerles parentesis. los que creeemos nosotros no hay quen ponerle el parentesis
    from_quantity = SelectMultipleField('from_quantity', choices=[('BTC, XRP, BCH, USDT, BSV, ADA,')], validators=[DataRequired(message='valor requerido')]) 
    to_currency = TextField('to_currency')
    to_quantity = FloatField('to_quantity')
    PU = FloatField('PU')

    submit = SubmitField('Aceptar')
