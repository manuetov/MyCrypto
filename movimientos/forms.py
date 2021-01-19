from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField, TextField, FloatField, DateField, DateTimeField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Length
from movimientos.api import Crypto


class MovementForm (FlaskForm):
    crypto10 = Crypto()
    listaCrypto = crypto10.get10Crypto()
    print (listaCrypto)

    date = StringField('date')
    time = StringField('time')
    from_currency = SelectField('From:', choices=[('EUR, BTC, XRP, BCH, USDT, BSV, ADA')], validators=[DataRequired(message='valor requerido')]) # los validadores de la clase Forms hay que ponerles parentesis. los que creeemos nosotros no hay quen ponerle el parentesis
    from_quantity = FloatField('Q:')  
    to_currency = SelectField('To:', choices=[('BTC, XRP, BCH, USDT, BSV, ADA,')], validators=[DataRequired()])
    to_quantity = FloatField('Q:')
    PU = FloatField('P.U.:')

    submit = SubmitField('Ok')
    
