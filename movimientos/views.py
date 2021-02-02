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
        errorDB = "an error has occurred in the database, try again in a few minutes"
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
            cryptoError = "OPERACIÓN INCORRECTA - LA CANTIDAD DEBE SER NUMÉRICA Y SUPERIOR A 0"
            return render_template("compra.html", menu='nuevacompra', cryptoError=cryptoError, form=form )
        if fromC == toC: #comprueba seleccion de monedas para que sea distintas
            cryptoError = "Error: Debe elegir monedas distintas"
            return render_template('compra.html', menu= 'nuevacompra', cryptoError=cryptoError, form=form)

        apiConsulta = api.api(fromC, toC)

        if apiConsulta[0] =='error':
            messageError = api.apiErrors(apiConsulta[1])
            errorAPI = "ERROR EN API - {}".format(messageError)
            return render_template("compra.html", menu='nuevacompra', form=form , errorAPI=errorAPI)
        else:
            dataQuant = apiConsulta[1]
        
        form.to_quantity.data = float(fromQ)/float(dataQuant)
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
                            WITH BALANCE
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
                            FROM BALANCE;
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

            # Comprobación de saldo suficiente con la crypto que se quiere comprar

            if saldo >= form.from_quantity.data or fromC == 'EUR':
            
                #form.from_currency.choices.append(toC)
                #dt = datetime.datetime.now()
                #fecha=dt.strftime("%d/%m/%Y")
                #hora=dt.strftime('%H:%M:%S')
                conn = sqlite3.connect(DBFILE)
                cursor = conn.cursor()
                mov = ' INSERT INTO movimientos (date, time, from_currency, from_quantity, to_currency, to_quantity, pu) VALUES (?,?,?,?,?,?,?);'
                cursor.execute(mov, (fecha, hora, fromC, fromQ, toC, form.to_quantity.data, form.pu.data))  

                #return redirect(url_for('listaMovimientos'))
                #return render_template("compra.html", menu='nuevacompra', form = form)
                conn.commit()

                ingresos = bbdd.dbconsulta('SELECT date, time, from_currency, from_quantity, to_currency, to_quantity, pu FROM movimientos') 
                conn.close()
                return render_template("listaMovimientos.html", menu='listaMovimientos', form = form, ingresos=ingresos)
            else:
                form.pu.data  = dataQuant
                sinSaldo = "NO TIENE SALDO SUFICIENTE EN {} PARA REALIZAR ESTA OPERACIÓN".format(fromC)
                return render_template("compra.html", menu='nuevacompra', form=form , sinSaldo=sinSaldo)
        else: 
            sinSaldo = "NO TIENE SALDO SUFICIENTE EN {} PARA REALIZAR ESTA OPERACIÓN".format(fromC)
            return render_template("compra.html", menu='nuevacompra', form=form , sinSaldo=sinSaldo)




@app.route('/status', methods = ['GET','POST'])

def inversion():

    try:
        movOrNot = bbdd.dbconsulta("SELECT date, time, from_currency, from_quantity, to_currency, to_quantity FROM MOVIMIENTOS;")
    except sqlite3.Error:
        totalInver = 0
        valorAct = 0
        dif = 0
        errorDB = "ERROR EN BASE DE DATOS, INTENTE EN UNOS MINUTOS"
        return render_template("status.html", menu="status", errorDB=errorDB, movOrNot=True)

    if movOrNot == None:
        return render_template("status.html", menu="status", movOrNot=True)


    InverFrom = bbdd.dbconsulta('SELECT SUM (from_quantity) FROM MOVIMIENTOS WHERE from_currency LIKE "%EUR%";')
    InverTo = bbdd.dbconsulta('SELECT SUM (from_quantity) FROM MOVIMIENTOS WHERE to_currency LIKE "%EUR%";')

    
    totalInverFrom = 0
    totalInverTo = 0
    for x in range(len(InverFrom)):
        if InverFrom[x] == (None,):
            totalInverFrom += 0
        else:
            InverFromInt = InverFrom[x][0]
            totalInverFrom += InverFromInt

    for x in range(len(InverTo)):
        if InverTo[x] == (None,):
            totalInverTo += 0
        else:
            InverToInt = InverTo[x][0]
            totalInverTo += InverToInt
    
    totalInver = totalInverFrom + totalInverTo
    cryptoSaldo()

    xi = 0
    cryptoValorActual = {}
    valorAct = 0
    for coin in cryptoCoin:
        apiConsulta = api.api('EUR',coin)
        
        cotizacion = apiConsulta[1]
        saldoCoin = cryptoSaldo()[xi]
        cryptoValorActual[coin] = cotizacion * saldoCoin
        valorAct += cryptoValorActual[coin]
        xi += 1    

    dif = valorAct - totalInver

    return render_template("status.html", menu="status", totalInver=totalInver, valorAct=valorAct, cryptoBalance=cryptoSaldo(), dif=dif)


    
    

