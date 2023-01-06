from eth_account import Account
from pyperp.providers import OptimismProvider
from pyperp.contracts.clearingHouse import ClearingHouse
from pyperp.contracts import ClearingHouse
from pyperp.contracts.types import OpenPositionParams
# from pyperp.commom.utils import getDeadline
from pyperp.contracts.marketRegistry import MarketRegistry

# import sys
# import os

# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))

import time
from pyperp.common.types import GasParams

def get_market_info():
  market_registry = MarketRegistry(provider)
  clearing_house = ClearingHouse(provider)
  print(
      market_registry.get_market_info(clearing_house.vbtc.address)
  ) 

def getDeadline(expiry_seconds: int):
    return int(time.time()) + expiry_seconds

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

  params = OpenPositionParams(
    base_token = base_token,
    is_base_to_quote = is_base_to_quote,
    is_exact_input = is_exact_input,
    amount = int(amount*10**18),
    # amount =size,
    opposite_amount_bound = 0,
    deadline = getDeadline(120), #deadline is 120 secs from now
    sqrt_price_limit_x96 = 0
  )

  receipt = clearing_house.open_position(
    params, gas_params
  )

  print(receipt)

  print(
    clearing_house.get_account_value(account.address)
  ) 

  

if __name__ == "__main__":

  gas_params = GasParams(
    gas=1000000,
    gas_price=1000000
  )
  #eth test
  account = Account.from_key('aaa')
  provider = OptimismProvider(
    'https://mainnet.optimism.io',
    account
  )
  # get_market_info()
  open_position('ETH', 'buy', 0.01)


