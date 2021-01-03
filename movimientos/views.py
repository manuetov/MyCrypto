from movimientos import app
from flask import render_template, request, url_for, redirect
import csv
import sqlite3
import formularios

#la unica manera para que un boton redirija a otra pagina es metiendolo en un formulario html, sino se deberia usar un hiperviculo html

def dbconsulta(query, params=()):
    conn = sqlite3.connect('movimientos/Data/basededatos.db')
    c = conn.cursor()

    c.execute(query, params)
    filas = c.fetchall()
    conn.commit()
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
    
    '''
    bitIngresos = open ("movimientos/Data/basededatos.csv", "r")
    csvReader = csv.reader(bitIngresos, delimiter=',', quotechar='"')
    ingresos = list(csvReader)
    '''
    sumador = 0
    for subpu in ingresos:
        sumador += float(subpu['PU'])
    
    return render_template ('listaMovimientos.html', datos=ingresos, total=sumador)

@app.route('/creacompra', methods = ['GET', 'POST'])
def nuevaCompra():
    
    if request.method == 'POST':
        print (request.method)

        dbconsulta('INSERT INTO movimientos (date, time, from_currency, from_quantity, to_currency, to_quantity, PU) VALUES (?,?,?,?,?,?,?);', 
                    (
                    request.form.get('date'), request.form.get('time'), request.form.get('from_currency'), float(request.form.get('from_quantity')),
                    request.form.get('to_currency'), float(request.form.get('to_quantity')), float(request.form.get('PU'))
                    ))      

        return render_template(url_for('listaMovimientos'))
    return render_template("compra.html")