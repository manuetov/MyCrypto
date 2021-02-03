# Instalación
- pip install Flask-WTF
## Dependencias
- Flask
### Requisitos de instalación 

pip install -r requirements.txt

pip install requests==2.18.4

# Crear variable de entorno

Crear variable de entorno **FLASK_APP** con el valor **run.py**

# Se guarda la url del api para bitcoin
api_request = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount=1&symbol={}&convert={}&CMC_PRO_API_KEY=<API_KEY>"

# Introducir su APIKEY en el archivo config_Template.py

Visitar la web de CoinMarketCap para conseguir una APIKEY:

Renombrar **config_Template.py** por **config.py**

**Lanzar aplicación**

flask run
