import json
import requests
from movimientos import app
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

API_KEY = app.config['API_KEY']

def api(cryptoFrom, cryptoTo):

    api_request = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount=1&symbol={}&convert={}&CMC_PRO_API_KEY=<API_KEY>".format(cryptoTo, cryptoFrom)
    headers = {'Accepts': 'aplication/json', 'X-CMC_PRO_API_KEY': API_KEY}

    session = Session()
    session.headers.update(headers)

    response = session.get(api_request)
    data = json.loads(response.text)

    try:
        conversion = ('', data['data']['quote'][cryptoFrom]['price'])
        return conversion
    except:
        errorCodeAPI = data['status']['error_code']
        return ('error', errorCodeAPI)

def apiErrors(codigo):
    if codigo == 1001:
        msg = "La API KEY no es válida"
    elif codigo == 1002:
        msg= "No existe API KEY"
    elif codigo == 1003:
        msg= "La API KEY no está activada"
    elif codigo == 1004:
        msg= "La API KEY ha caducado"
    elif codigo == 1005:
        msg= "Se requiere API KEY"
    elif codigo == 1007:
        msg= "API KEY deshabilitada"
    elif codigo == 1009:
        msg= "Excedido límite de tarifa diaria de API KEY"
    elif codigo == 1010:
        msg= "Excedido límite de tarifa mensual de API KEY"
    return msg


'''

class CryptoMonedas():
    
    def getCrypto_posibles(self):
                        
        api_request = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

        headers = {'Accepts': 'aplication/json', 'X-CMC_PRO_API_KEY': '37d49a04-de45-445f-b473-fa22982fdc5d'}

        session = Session()
        session.headers.update(headers)

        response = session.get(api_request)

        datos = json.loads(response.text)

        posible_coins = [
        {'sym':'BTC'},{'sym':'XRP'},{'sym':'BCH'},{'sym':'USDT'},{'sym':'BSV'},{'sym':'ADA'}]
        
        lista_posible_coins = []
                
        for x in datos['data']:
            for coin in posible_coins:
                if coin['sym'] == x["symbol"]:
                    sym = (x["symbol"])
                    lista_posible_coins.append({'coin': sym })
        return lista_posible_coins
    
    def getCrypto_my(self):

        api_request = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

        headers = {'Accepts': 'aplication/json', 'X-CMC_PRO_API_KEY': '37d49a04-de45-445f-b473-fa22982fdc5d'}

        session = Session()
        session.headers.update(headers)

        response = session.get(api_request)

        datos = json.loads(response.text)

        my_coins = [
        {'sym':'ETH'},{'sym':'LTC'},{'sym':'BNB'},{'sym':'EOS'},{'sym':'XLM'},{'sym':'TRX'}]

        lista_my_coins = []

        for i in datos['data']:
            for coin in my_coins:
                if coin['sym'] == i["symbol"]:
                    sym = (i["symbol"])
                    lista_my_coins.append({'coin': sym})
        return lista_my_coins


coin = CryptoMonedas()
monedas_posibles = coin.getCrypto_posibles()
print (monedas_posibles)

coin1 = CryptoMonedas()
mis_monedas = coin1.getCrypto_my()
print (mis_monedas)



        bitcoinlist=[]
        for i in range (9):
            bitcoin = datos['data'][i]
            sym = bitcoin['symbol']

            pri = bitcoin['quote']['USD']['price']
            bitcoinlist.append({"coin" : sym, "price" : pri})

        return json.dumps(bitcoinlist)

#coin_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
# price_url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'
coin_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'


''' 