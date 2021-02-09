from movimientos import app
from flask import render_template, request, url_for, redirect
import csv
import sqlite3
from movimientos import bbdd
import datetime
from movimientos.forms import MovementForm
import requests
from movimientos import api
from movimientos.cryptoSaldo import cryptoSaldo

#la unica manera para que un boton redirija a otra pagina es metiendolo en un formulario html, sino se deberia usar un hiperviculo html
cryptoCoin = ('BTC','ETH','XRP','LTC','BCH','BNB','USDT','EOS','BSV','XLM','ADA','TRX') 

DBFILE = app.config['DBFILE']

@app.route('/')
def listaMovimientos():
    try:
        ingresos = bbdd.dbconsulta('SELECT date, time, from_currency, from_quantity, to_currency, to_quantity, pu FROM movimientos') 
    
        return render_template ('listaMovimientos.html', menu='listaMovimientos', ingresos=ingresos)

    except sqlite3.Error: 
        ingresos = None
        errorDB = "**ERROR** no se puede acceder a la base de datos, intentelo más tarde"
        return render_template('listaMovimientos.html', menu='listaMovimientos', errorDB=errorDB, ingresos=ingresos)


@app.route('/nuevacompra', methods = ['GET', 'POST'])
def nuevaCompra():
    form = MovementForm(request.form) # crea la instancia y se inicializa con los datos que vienen en request que es un objeto con todos los datos de la peticion creada en el navegador
    
    fromC= request.values.get('from_currency')
    toC = request.values.get('to_currency')
    fromQ = request.values.get('from_quantity')    

    if request.method == 'GET':

        return render_template('compra.html', menu='nuevacompra', form = form)

    if request.values.get ('submitCalculadora'):
        
        if not form.validate():
            cryptoError = "OPERACIÓN INCORRECTA - LA CANTIDAD DEBE SER NUMÉRICA Y SUPERIOR A 0" # comprueba que se introduzcan solo numeros mayor de 0
            return render_template("compra.html", menu='nuevacompra', cryptoError=cryptoError, form=form )
        if fromC == toC: #comprueba seleccion de monedas para que sea distintas
            cryptoError = "Error: Debe elegir monedas distintas"
            return render_template('compra.html', menu= 'nuevacompra', cryptoError=cryptoError, form=form)

        apiConsulta = api.api(fromC, toC) # devuelve ('', pu)

        if apiConsulta[0] =='error':
            messageError = api.apiErrors(apiConsulta[1])
            errorAPI = "ERROR EN API - {}".format(messageError)
            return render_template("compra.html", menu='nuevacompra', form=form, errorAPI=errorAPI)
        else:
            dataQuant = apiConsulta[1] # pu
        
        form.to_quantity.data = float(fromQ)/float(dataQuant) # cantidad Q / pu 
        form.pu.data = dataQuant

        return render_template("compra.html", menu="nuevacompra", form = form)
            
    if request.values.get ('submitCompra'):
        if not form.validate():
            cryptoError = "OPERACIÓN INCORRECTA - LA CANTIDAD DEBE SER NUMÉRICA Y SUPERIOR A 0"
            return render_template("compra.html", menu='nuevacompra', cryptoError=cryptoError, form=form )

        if fromC == toC: #comprueba seleccion de monedas para que sea distintas
            cryptoError = "Error: Debe elegir monedas distintas"
            return render_template('compra.html', menu='nuevacompra', cryptoError=cryptoError, form=form)    
     
        #if form.validate_on_submit():

        if fromC == 'EUR':
            saldo = 999999999999
        else:
            try:
                saldo = bbdd.dbconsulta('''
                            WITH RESULTADO
                            AS
                            (
                            SELECT SUM(to_quantity) AS saldo
                            FROM MOVIMIENTOS
                            WHERE to_currency LIKE "%{}%"
                            UNION ALL
                            SELECT -SUM(from_quantity) AS saldo
                            FROM MOVIMIENTOS
                            WHERE from_currency LIKE "%{}%"
                            )
                            SELECT SUM(saldo)
                            FROM RESULTADO;
                            '''.format(fromC, fromC))
            except sqlite3.Error:
                errorDB = "ERROR EN BASE DE DATOS, INTENTE EN UNOS MINUTOS"
                return render_template("compra.html", menu='nuevacompra', form=form , errorDB=errorDB)

            if saldo[0] == (None,):
                saldo = 0
            else:
                saldo = saldo[0][0]

        if fromC == 'EUR' or saldo != 0:

            dt = datetime.datetime.now()
            fecha=dt.strftime("%d/%m/%Y")
            hora=dt.strftime("%H:%M:%S")
            apiConsulta = api.api(fromC, toC)
            if apiConsulta[0] =='error':
                messageError = api.apiErrors(apiConsulta[1])
                errorAPI = "ERROR EN API - {}".format(messageError)
                return render_template("compra.html", menu='nuevacompra', form=form , errorAPI=errorAPI)
            else:
                dataQuant = apiConsulta[1]
                form.to_quantity.data = float(fromQ)/float(dataQuant)

                form.pu.data = dataQuant

            # Comprobación de saldo suficiente de la moneda a comprar

            if saldo >= form.from_quantity.data or fromC == 'EUR':
            # se conecta a la bbdd e inserta los datos introducidos y el resultado de la conversion de cryptos
                try:    
                    conn = sqlite3.connect(DBFILE)
                    cursor = conn.cursor()
                    mov_bbdd = ' INSERT INTO movimientos (date, time, from_currency, from_quantity, to_currency, to_quantity, pu) VALUES (?,?,?,?,?,?,?);'
                    cursor.execute(mov_bbdd, (fecha, hora, fromC, fromQ, toC, form.to_quantity.data, form.pu.data))  
                    conn.commit()
                except sqlite3.Error:
                    errorDB = "ERROR EN BASE DE DATOS, INTENTE EN UNOS MINUTOS"
                    return render_template("compra.html", menu='nuevacompra', form=form , errorDB=errorDB)

                try:
                    ingresos = bbdd.dbconsulta('SELECT date, time, from_currency, from_quantity, to_currency, to_quantity, pu FROM movimientos') 
                    conn.close()
                except sqlite3.Error:
                    errorDB = "ERROR EN BASE DE DATOS, INTENTE EN UNOS MINUTOS"
                    return render_template("compra.html", menu='nuevacompra', form=form , errorDB=errorDB)    
                return render_template("listaMovimientos.html", menu='listaMovimientos', form = form, ingresos=ingresos)
            else: # comprueba que las monedas seleccionadas tengan saldo
                form.pu.data  = dataQuant
                sinSaldo = "NO TIENE SALDO SUFICIENTE EN {} PARA REALIZAR ESTA OPERACIÓN".format(fromC)
                return render_template("compra.html", menu='nuevacompra', form=form , sinSaldo=sinSaldo)
        else: 
            sinSaldo = "NO TIENE SALDO SUFICIENTE EN {} PARA REALIZAR ESTA OPERACIÓN".format(fromC)
            return render_template("compra.html", menu='nuevacompra', form=form , sinSaldo=sinSaldo)




@app.route('/status', methods = ['GET','POST'])

def inversion():
    # lee la bbdd y la guarda en una variable, si no tiene movimientos se mostrará por pantalla 
    try:
        movimientos_bbdd = bbdd.dbconsulta("SELECT date, time, from_currency, from_quantity, to_currency, to_quantity FROM MOVIMIENTOS;")
    except sqlite3.Error:
        errorDB = "ERROR EN BASE DE DATOS, INTENTE EN UNOS MINUTOS"
        return render_template("status.html", menu="status", errorDB=errorDB, movimientos_bbdd=True)

    if movimientos_bbdd == None:
        return render_template("status.html", menu="status", movimientos_bbdd=True)

    # guarda la suma en EUR de las cantidades compradas y vendidas
    try:
        Invertido_From_bbdd = bbdd.dbconsulta('SELECT SUM (from_quantity) FROM MOVIMIENTOS WHERE from_currency LIKE "%EUR%";')
        Invertido_To_bbdd = bbdd.dbconsulta('SELECT SUM (from_quantity) FROM MOVIMIENTOS WHERE to_currency LIKE "%EUR%";')
    except sqlite3.Error:
        errorDB = "ERROR EN BASE DE DATOS, INTENTE EN UNOS MINUTOS"
        return render_template("status.html", menu="status", errorDB=errorDB, movimientos_bbdd=True)
    
    total_Invertido_From = 0
    total_Invertido_To = 0
    for x in range(len(Invertido_From_bbdd)):
        if Invertido_From_bbdd[x] == (None,):
            total_Invertido_From += 0
        else:
            Invertido_FromInt = Invertido_From_bbdd[x][0]
            total_Invertido_From += Invertido_FromInt

    for x in range(len(Invertido_To_bbdd)):
        if Invertido_To_bbdd[x] == (None,):
            total_Invertido_To += 0
        else:
            Invertido_ToInt = Invertido_To_bbdd[x][0]
            total_Invertido_To += Invertido_ToInt
    
    total_Invertido = total_Invertido_From + total_Invertido_To
    
    try: 
        cryptoSaldo()
    except sqlite3.Error:
        errorDB = "ERROR EN BASE DE DATOS, INTENTE EN UNOS MINUTOS"
        return render_template("status.html", menu="status", errorDB=errorDB, movimientos_bbdd=True)
    
    xx = 0
    crypto_valor_Actual = {}
    valor_Actual = 0
    for coin in cryptoCoin:
        apiConsulta = api.api('EUR',coin)
        
        cotizacion = apiConsulta[1]
        saldoCoin = cryptoSaldo()[xx]
        crypto_valor_Actual[coin] = cotizacion * saldoCoin
        valor_Actual += crypto_valor_Actual[coin]
        xx += 1    

    beneficio_Perdida = valor_Actual - total_Invertido

    return render_template("status.html", menu="status", total_Invertido=total_Invertido, valor_Actual=valor_Actual, cryptoBalance=cryptoSaldo(), beneficio_Perdida=beneficio_Perdida)



    
    

