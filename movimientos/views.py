from movimientos import app
from flask import render_template, request, url_for, redirect
import csv
import sqlite3
from movimientos.forms import MovementForm
from movimientos.api import Crypto


#la unica manera para que un boton redirija a otra pagina es metiendolo en un formulario html, sino se deberia usar un hiperviculo html
DBFILE = app.config['DBFILE'] # DBFILE='movimientos/Data/basededatos.db


def dbconsulta(query, params=()):
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()

    c.execute(query, params)
    conn.commit()

    filas = c.fetchall()
    
    conn.close()

    if len(filas) == 0:
        return filas

    columNames = []
    for columName in c.description:
        columNames.append(columName[0])
    
    listaDeDiccionarios = []
    
    for fila in filas:
        d = {}
        for ix, columName in enumerate(columNames):
            d[columName] = fila[ix]
        listaDeDiccionarios.append(d)

    return listaDeDiccionarios

@app.route('/')
def listaMovimientos():
    
    ingresos = dbconsulta('SELECT date, time, from_currency, from_quantity, to_currency, to_quantity, PU FROM movimientos') 
    
    sumador = 0
    for subpu in ingresos:
        sumador += float(subpu['PU'])
    
    return render_template ('listaMovimientos.html', datos=ingresos, total=sumador)

@app.route('/creacompra', methods = ['GET', 'POST'])
def nuevaCompra():
    form = MovementForm(request.form) # crea la instancia y se inicializa con los datos que vienen en request que es un objeto con todos los datos de la peticion creada en el navegador
    
    if request.method == 'POST' and form.validate_on_submit():
        dbconsulta('INSERT INTO movimientos (date, time, from_currency, from_quantity, to_currency, to_quantity, PU) VALUES (?,?,?,?,?,?,?);', 
            (
            form.date.data, form.time.data, form.from_currency.data, form.from_quantity.data, 
            form.to_currency.data, form.to_quantity.data, form.PU.data
            ))  

        return redirect(url_for('listaMovimientos'))
    else:
        return render_template("compra.html", form = form)

    return render_template("compra.html", form = form)