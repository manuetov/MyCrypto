# Instalación
- pip install Flask-WTF
## Dependencias
- Flask
pip3 install coinmarketcap
# Se guarda el url del api para bitcoin
bitcoin_api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
# Se guarda la consulta al url de bitcoin
respuesta = requests.get(bitcoin_api_url)
# Se obtiene el json de la respuesta
resp_json = respuesta.json()
# cual es el tipo de dato de resp_json
type(resp_json)
# El tipo de datos de resp_json es una lista, se muestra el primer elemento de la lista
resp_json[0]
# Se tiene un json con los datos de la cotización actual de Bitcoin BTC.
# Ahora se usa la libreria coinmarketcap y la clase Market.
from coinmarketcap import Market
# Se crea la instancia de la clase
coinmarketcap = Market()
# Se obtiene la cotizacion de bitcoin
coinmarketcap.ticker("bitcoin")
# Se tienen dos formas de obtener la información del sitio coinmarketcap, una es usando request y otra la librería que accede directamente al API,
pip install requests==2.18.4
pip install Flask-Bootstrap