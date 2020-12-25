# creamos la aplicación 
from flask import Flask

app = Flask(__name__)

from movimientos import views # para que encuentre la route hay que importar las vistas.