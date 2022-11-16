#!/usr/bin/env python3
import logging
import pandas as pd
from colorama import Fore, Back, Style
from binance.um_futures import UMFutures
from binance.lib.utils import config_logging
from binance.error import ClientError
from binance.client import Client

# config_logging(logging, logging.DEBUG)

key = ""
secret = ""

client = Client(api_key=key, api_secret=secret)

um_futures_client = UMFutures(key=key, secret=secret)

crypto_symbol = input('\n' + Fore.GREEN + '\033[1m' + "Insert asset: " + '\033[0m' + Fore.RESET).upper()

def get_av_balance():
        params = {
                "asset": "USDT",
        }

        acc_balance = client.futures_account_balance(**params)

        for check_balance in acc_balance:
                if check_balance["asset"] == "USDT":
                        test = check_balance["withdrawAvailable"]

        av_balance = test[0:6]
        return av_balance

def get_balance():
        params = {
                "asset": "USDT",
        }

        acc_balance = client.futures_account_balance(**params)

        for check_balance in acc_balance:
                if check_balance["asset"] == "USDT":
                        test = check_balance["balance"]

        balance = test[0:6]
        return balance

# Calculate quantity
def calc_quantity():
        av_balance_float = float(get_av_balance())
        usd_position = (av_balance_float * 0.01) * 20
        
        return usd_position

# Get asset price from Entry Price order
def get_asset_price():
        logg = um_futures_client.mark_price()

        for loger in logg:
            if loger["symbol"] == crypto_symbol:
                return loger["markPrice"]

# Convert quantity
asset_price = get_asset_price()[0:5]
quant = float(calc_quantity()) / float(asset_price)
qq = str(quant)
qq_to_int = int(qq.split('.')[0])
if qq_to_int == 0:
    q2 = qq[0:5]
else:
    q2 = qq_to_int

def new_order():
        client.futures_create_order(symbol=crypto_symbol, positionSide='SHORT', side='SELL', type='MARKET', quantity=q2)

new_order()

def trailing_stop():
    params = {
        "symbol": crypto_symbol
    }
    
    position_info = client.futures_position_information(**params)

    for entryPrice in position_info:
        en_price = entryPrice["entryPrice"]
    
    act_price = (float(en_price) * 0.05) + float(en_price)

    return client.futures_create_order(symbol=crypto_symbol, positionSide='SHORT', side='SELL', type='TRAILING_STOP_MARKET', callbackRate="3", activationPrice=act_price, quantity=q2)

trailing_stop()

def en_price_of_order():
    params = {
        "symbol": crypto_symbol
    }
    
    position_info = client.futures_position_information(**params)

    for entryPrice in position_info:
        en_price = entryPrice["entryPrice"]
    return en_price

print('\n' + Fore.CYAN + '\033[1m' + "--------RESULTS--------" + '\033[0m' + Fore.RESET)        

print(Fore.YELLOW + '\033[1m' + "Entry price:" + '\033[0m' + Fore.RESET, en_price_of_order(), "$")
print(Fore.YELLOW + '\033[1m' + "Position quanitity:" + '\033[0m' + Fore.RESET, q2, crypto_symbol) 
print(Fore.YELLOW + '\033[1m' + "Fixed balance:" + '\033[0m' + Fore.RESET, get_balance(), "$")
print(Fore.YELLOW + '\033[1m' + "Available balance:" + '\033[0m' + Fore.RESET, get_av_balance()[:-2], "$")

print('\n' + Fore.CYAN + '\033[1m' + "-----------------------" + '\033[0m' + Fore.RESET) 
