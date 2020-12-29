from movimientos import app
from flask import render_template, request
import csv


#la unica manera para que un boton redirija a otra pagina es metiendolo en un formulario html, sino se deberia usar un hiperviculo html

@app.route('/')
def listaMovimientos():
    bitIngresos = open ("movimientos/Data/basededatos.csv", "r")
    csvReader = csv.reader(bitIngresos, delimiter=',', quotechar='"')
    ingresos = list(csvReader)
    suma = 0
    for ingreso in ingresos:
        suma += float (ingreso[6])
    print (ingresos)
    
    
    return render_template ('listaMovimientos.html', total=suma, datos=ingresos)

@app.route('/creacompra', methods = ['GET', 'POST'])
def nuevaCompra():
    if request.method == 'POST':
        print (request.method)
       
    
    return render_template('compra.html')