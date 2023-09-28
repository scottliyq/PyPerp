#py310btc
import ccxt
import requests
from hexbytes import HexBytes
from eth_account import Account
from pyperp.providers import OptimismProvider
from pyperp.contracts.clearingHouse import ClearingHouse
from pyperp.contracts import ClearingHouse
from pyperp.contracts.types import OpenPositionParams
# from pyperp.commom.utils import getDeadline
import time
from pyperp.common.types import GasParams

TRADE_SYMBOL = 'PERP'
TRADE_PAIR = TRADE_SYMBOL+'USDT'
MAX_INDEX = 1
TRADE_BN_FLG = True
# TARGET_POS_SIZE = 500
ICE_AMOUNT = 300

BN_DIRECTION = 'buy'
PERP_DIRECTION = 'sell'

import os
from dotenv import load_dotenv

load_dotenv()


binance = ccxt.binance()

binance.apiKey =os.getenv('bn_api_key_huangjie')
binance.secret = os.getenv('bn_api_secret_huangjie')

#eth8
account = Account.from_key(os.getenv('private_key_eth9'))
provider = OptimismProvider(
    # 'https://mainnet.optimism.io',
    'https://opt-mainnet.g.alchemy.com/v2/LUv4Dm1PU4IurUyEKbkfJd9-UBzQv0bW',
    account
)

gas_params = GasParams(
    gas=9000000,
    gas_price=1000000
)

def getDeadline(expiry_seconds: int):
    return int(time.time()) + expiry_seconds

def get_pos_amount(symbol_pair):
    account = binance.fapiPrivateGetAccount()

    positions = account['positions']

    for pos in positions:
        if pos['symbol'] == symbol_pair:
            return float(pos['positionAmt'])

def trade_future_market(pair, direction, price, amount) : #交易

    params = {'symbol':pair,'side':direction.upper(),'type':'MARKET', "quantity":str(amount)}
    binance.fapiPrivatePostOrder(params)
    print(f"bn trade {pair} {direction} {amount} success")
        
    return 

def open_position(symbol, direction, amount):
  clearing_house = ClearingHouse(provider)
  is_base_to_quote = True
  is_exact_input = True
  if direction == 'buy':
    is_base_to_quote = False
    is_exact_input = False

    # todo add more tokens
  base_token = clearing_house.vbtc.address
  if symbol == 'ETH':
    base_token = clearing_house.veth.address
  elif symbol == 'SOL':
    base_token = clearing_house.vsol.address
  elif symbol == 'FTM':
    base_token = clearing_house.vftm.address
  elif symbol == 'AAVE':
    base_token = clearing_house.vaave.address
  elif symbol == 'FLOW':
    base_token = clearing_house.vflow.address
  elif symbol == 'DOGE':
    base_token = clearing_house.vdoge.address
  elif symbol == 'AVAX':
    base_token = clearing_house.vavax.address
  elif symbol == 'ATOM':
    base_token = clearing_house.vatom.address
  elif symbol == 'MATIC':
    base_token = clearing_house.vmatic.address
  elif symbol == 'CRV':
    base_token = clearing_house.vcrv.address
  elif symbol == 'PERP':
    base_token = clearing_house.vperp.address
  elif symbol == 'OP':
    base_token = clearing_house.vop.address
  elif symbol == 'APE':
    base_token = clearing_house.vape.address
    
  bytes32_value = b'\x01' * 32
  
  # tx_hash = bytes32_value.transact()
  params = OpenPositionParams(
    base_token = base_token,
    is_base_to_quote = is_base_to_quote,
    is_exact_input = is_exact_input,
    amount = int(amount*10**18),
    # amount =size,
    opposite_amount_bound = 0,
    deadline = getDeadline(120), #deadline is 120 secs from now
    sqrt_price_limit_x96 = 0,
    referral_code=bytes32_value

  )
  print(f"perp trade {symbol} {direction} {amount} success")
  receipt = clearing_house.open_position(
    params, gas_params
  )

  # print(receipt)

def main():
    index = 0
    while(True):
        # pos_amount = get_pos_amount(TRADE_PAIR)
        # print(f"bn amount: {pos_amount}")
        if index >= MAX_INDEX:
            print('final hedge finished')
            break
        else:
            print(f"hedge start: {index}")
            index += 1
            open_position(TRADE_SYMBOL, PERP_DIRECTION, ICE_AMOUNT)
            if TRADE_BN_FLG:
              trade_future_market(TRADE_PAIR, BN_DIRECTION, 0, ICE_AMOUNT)
            print('hedge finished')

        time.sleep(6)



if __name__ == '__main__':
    main()