from movimientos import app
from flask import render_template

@app.route('/')
def listaMovimientos():
    return render_template ('listaMovimientos.html')

