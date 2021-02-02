import sqlite3
from movimientos import app

DBFILE = app.config['DBFILE']

def dbconsulta(consulta, params=()):
    conn = sqlite3.connect(DBFILE)
    cursor = conn.cursor()

    cursor.execute(consulta, params)
    
    resultado= cursor.fetchall()
    
    if len(resultado) == 0:
        resultado = None
    
    conn.commit()
    conn.close() 

    return resultado
    
