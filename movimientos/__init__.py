# creamos la aplicación. siempre que una carpeta tenga el init se puede importar como si fuera un modulo. es el primer fichero que se ejecuta 
from flask import Flask

app = Flask(__name__, instance_relative_config=True) # app es una instancia de Flask contenedor de la aplicación
app.config.from_object('config')


from movimientos import views # para que encuentre la route hay que importar las vistas.