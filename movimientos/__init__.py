# creamos la aplicación 
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')

from movimientos import views # para que encuentre la route hay que importar las vistas.