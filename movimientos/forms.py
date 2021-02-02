from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField, FloatField, Label, IntegerField, ValidationError, HiddenField
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired
from movimientos.api import api

class MovementForm (FlaskForm):
    
    cryptoCoin =[('EUR'),('BTC'),('ETH'),('XRP'),('LTC'),('BCH'),('BNB'),('USDT'),('EOS'),('BSV'),('XLM'),('ADA'),('TRX')]  

    from_currency = SelectField('From: ', choices=cryptoCoin, validators=[DataRequired()])
    to_currency = SelectField('To: ', choices=cryptoCoin, validators=[DataRequired()]) 
    from_quantity = FloatField('Q: ', validators=[InputRequired(),NumberRange(min=0.00001, max=9999999)])
    to_quantity = HiddenField ()
    pu = HiddenField ()

    submitCalculadora = SubmitField('Calcular')
    submitCompra= SubmitField('Ok')


'''
coin = CryptoMonedas()
    compraCoin = coin.getCrypto_posibles()
    # print (compraCoin)

    coin1 = CryptoMonedas()
    pagoCoin = coin1.getCrypto_my()

    monedasFrom=[]
    for x in compraCoin:
        moneda = x['coin']
        monedasFrom.append(moneda)
    #print (moneda)
    
    monedasTo=[]
    for x in pagoCoin:
        moneda = x['coin']
        monedasTo.append(moneda)
        '''