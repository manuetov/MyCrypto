import json
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

class Crypto:

    def get10Crypto(self):

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

'''
    mi_lista = []
dict = {}
for x in data['data']:
    for coin in posible_coins:
        if coin == x["symbol"]:
            dict['clave'] = (x["symbol"])
            dict['valor'] = ("${0:.2f}".format(float(x['quote']['USD']['price'])))
            mi_lista.append(dict)
print (mi_lista)

'''

'''
try:
    for x in range (9):
        bitcoin = data['data'][x]
        bitcoinName = bitcoin['name']
        bitcoinSymbol = bitcoin['symbol']
        bitcoinSlug = bitcoin['slug']
        bitcoinPrice = bitcoin['quote']['USD']['price']
        print("bitcoin name is: {}, symbol: {}, slug: {}, price: {} ".format(bitcoinName, bitcoinSymbol, bitcoinSlug, bitcoinPrice))
except (ConnectionAbortedError, Timeout, TooManyRedirects) as e:
    print(e)
#coin_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
# price_url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'
coin_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
'''