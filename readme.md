# Instalación
- pip install Flask-WTF
## Dependencias
- Flask
### Requisitos de instalación 

pip install -r requirements.txt

pip install requests==2.18.4

# Registrarse en esta web para obtener la apikey
https://pro.coinmarketcap.com/

# Introducir su APIKEY en el archivo config_Template.py

Renombrar **config_Template.py** por **config.py**

# Crear base de datos con sqlite3
- desde el directorio movimientos/Data
■ sqlite3 <nombre_bd>.db
● ejecutar
■ .read migrations/initial.sql
- commprobar que se han creado las tablas
■ .tables
- salir
■ .q

# Crear variable de entorno

Crear variable de entorno **FLASK_APP** con el valor **run.py**

**Ejecución de la aplicación**

flask run

