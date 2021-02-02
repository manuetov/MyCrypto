import sqlite3
from movimientos import bbdd

cryptoCoin = ('BTC','ETH','XRP','LTC','BCH','BNB','USDT','EOS','BSV','XLM','ADA','TRX') 

def cryptoSaldo():
    cryptoBalance = []
    for coin in cryptoCoin:
        cryptoBalanceCoin = bbdd.dbconsulta('''
                                WITH BALANCE
                                AS
                                (
                                SELECT SUM(to_quantity) AS saldo
                                FROM MOVIMIENTOS
                                WHERE to_currency LIKE "%{}%"
                                UNION ALL
                                SELECT SUM(from_quantity) AS saldo
                                FROM MOVIMIENTOS
                                WHERE from_currency LIKE "%{}%"
                                )
                                SELECT SUM(saldo)
                                FROM BALANCE
                                '''.format(coin, coin))
        if cryptoBalanceCoin[0] == (None,):
            cryptoBalanceCoin=0
            cryptoBalance.append(cryptoBalanceCoin)
        else:
            cryptoBalance.append(cryptoBalanceCoin[0][0])
    return cryptoBalance
