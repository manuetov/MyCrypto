import requests
import json
from requests import Request, Session

api_request = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

headers = {'Accepts': 'aplication/json', 'X-CMC_PRO_API_KEY': '37d49a04-de45-445f-b473-fa22982fdc5d',}

session = Session()
session.headers.update(headers)

response = session.get(api_request)

data = json.loads(response.content)

posible_coins = ['BTC','XRP','BCH','USDT','BSV','ADA']
coins = ['EUR','ETH','LTC','BNB','EOS','XLM','TRX']

lista_posible_coins = []
dict = {}
for x in data['data']:
    for coin in posible_coins:
        if coin == x["symbol"]:
            dict['clave'] = (x["symbol"])
            dict['valor'] = ("${0:.2f}".format(float(x['quote']['USD']['price'])))
            lista_posible_coins.append(dict)
print (lista_posible_coins)

lista_coins = []
dict = {}
for x in data['data']:
    for coin in coins:
        if coin == x["symbol"]:
            dict['clave'] = (x["symbol"])
            dict['valor'] = ("${0:.2f}".format(float(x['quote']['USD']['price'])))
            lista_coins.append(dict)
print (lista_coins)

'''
nuevo_dic = {}
nuevo_dic['clave'] = 'valor'
nuevo_dic['otra_clave'] = 'otro_valor'
...
mi_lista.append(nuevo_dic)
'''