import json
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

class CryptoMonedas():

    def getCrypto(self):
        #conversion = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'

        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

        parameters = {'start': '1', 'limit':'10', 'convert': 'USD',}

        headers = {'Accepts': 'aplication/json', 'X-CMC_PRO_API_KEY': '37d49a04-de45-445f-b473-fa22982fdc5d',}

        session = Session()
        session.headers.update(headers)

        response = session.get(url, params=parameters)
        datos = json.loads(response.text)

        bitcoinlist=[]
        for i in range (9):
            bitcoin = datos['data'][i]
            sym = bitcoin['symbol']

            pri = bitcoin['quote']['USD']['price']
            bitcoinlist.append({"coin" : sym, "price" : pri})

        return json.dumps(bitcoinlist)

cryp10 = CryptoMonedas()
lista = cryp10.getCrypto()
print (lista)

'''
#coin_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
# price_url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'
coin_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
''' 