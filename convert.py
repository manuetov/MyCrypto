import json
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


class crypto():

    API_KEY = '37d49a04-de45-445f-b473-fa22982fdc5d'

    cantidad = 1
    cryptoTo ='BTC'
    cryptoFrom ='EUR'

    api_request = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY=<API_KEY>".format(cantidad, cryptoTo, cryptoFrom)
    headers = {'Accepts': 'aplication/json', 'X-CMC_PRO_API_KEY': API_KEY}

    session = Session()
    session.headers.update(headers)

    response = session.get(api_request)

    data = json.loads(response.text)
    
    print(data['data']['quote'][cryptoFrom]['price'])
    print(data['status']['timestamp'])
    print(data)

    
   



'''
    except:
        errorCodeAPI = data['status']['error_code']
        return ('error', errorCodeAPI)

url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'

parameters = {'start': '1', 'limit':'10', 'convert': 'USD',}

headers = {'Accepts': 'aplication/json', 'X-CMC_PRO_API_KEY': '37d49a04-de45-445f-b473-fa22982fdc5d',}

session = Session()
session.headers.update(headers)

response = session.get(url, params=parameters)
data = json.loads(response.text)
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