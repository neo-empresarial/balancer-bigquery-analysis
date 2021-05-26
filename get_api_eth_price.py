from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()
from web3 import Web3
import pandas as pd
import os
import datetime
from functools import reduce

web3_provider = 'wss://mainnet.infura.io/ws/v3/0cf6452466de4abf87ff0d9c07d484d8'
w3 = Web3(Web3.WebsocketProvider(web3_provider))
start_block_timestamp = w3.eth.getBlock(9195000).timestamp  # 01/05/2020
end_block_timestamp = int(datetime.datetime.now().timestamp())

w3.eth.getBlock(9195000).timestamp

eth_price = cg.get_coin_market_chart_range_by_id('ethereum', 'usd', from_timestamp=start_block_timestamp, to_timestamp=end_block_timestamp)['prices']

def format_datetime_str(time_price):
    timestamp = time_price[0] / 1000
    time_price[0] = datetime.datetime.fromtimestamp(timestamp).strftime("%m/%d/%Y %H:%M:%S")
    return time_price

api_eth_price = pd.DataFrame(map(format_datetime_str, eth_price), columns=['date', 'price'])