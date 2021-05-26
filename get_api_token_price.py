from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()
from web3 import Web3
import pandas as pd
import os
import datetime
from functools import reduce

def get_api_token_price(token_id, start_block, end_block=-1):

    web3_provider = 'wss://mainnet.infura.io/ws/v3/0cf6452466de4abf87ff0d9c07d484d8'
    w3 = Web3(Web3.WebsocketProvider(web3_provider))
    start_block_timestamp = w3.eth.getBlock(start_block).timestamp  # 01/05/2020
    if end_block != -1:
        end_block_timestamp = w3.eth.getBlock(end_block).timestamp
    else:
        end_block_timestamp = int(datetime.datetime.now().timestamp())

    token_price = cg.get_coin_market_chart_range_by_id(token_id, 'usd', from_timestamp=start_block_timestamp, to_timestamp=end_block_timestamp)['prices']

    def format_datetime_str(time_price):
        timestamp = time_price[0] / 1000
        time_price[0] = datetime.datetime.fromtimestamp(timestamp).strftime("%m/%d/%Y %H:%M:%S")
        return time_price

    api_token_price = pd.DataFrame(map(format_datetime_str, token_price), columns=['date', 'price'])

    api_token_price['date'] = pd.to_datetime(api_token_price['date'], format='%m/%d/%Y  %H:%M:%S')
    api_token_price['date'] = api_token_price['date'].dt.strftime('%m/%d/%Y')   

    return api_token_price