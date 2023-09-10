'''ClearingHouse class.'''

from pyperp.providers import ApiProvider
from pyperp.contracts.types import (
    AddLiquidityParams,
    OpenPositionParams,
    ClosePositionParams,
    RemoveLiquidityParams
)
from pyperp.common.types import GasParams
from web3 import Web3
import logging
from dataclasses import astuple


class ClearingHouse:
    def __init__(self, provider: ApiProvider):
        '''
        Initialize provider.
        Arguments:
        provider - An object of class derived from ApiProvider
        '''
        self._provider = provider
        self.account = self._provider.account
        self.logger = logging.getLogger("ClearingHouse")

        self.logger.info("Loading ClearingHouse contract")
        clearing_house_meta = self._provider.load_meta("ClearingHouse")
        self.clearing_house = self._provider.api.eth.contract(
            address=clearing_house_meta["address"],
            abi=clearing_house_meta["abi"]
        )
        self.logger.info("ClearingHouse contract loaded")

        self.logger.info("Loading USDC contract")
        usdc_meta = self._provider.load_meta("USDC")
        self.usdc = self._provider.api.eth.contract(
            address=usdc_meta["address"],
            abi=usdc_meta["abi"]
        )
        self.logger.info("USDC contract loaded")

        self.logger.info("Loading vBTC contract")
        vbtc_meta = self._provider.load_meta("vBTC")
        self.vbtc = self._provider.api.eth.contract(
            address=vbtc_meta["address"],
            abi=vbtc_meta["abi"]
        )
        self.logger.info("vBTC contract loaded")

        self.logger.info("Loading vETH contract")
        veth_meta = self._provider.load_meta("vETH")
        self.veth = self._provider.api.eth.contract(
            address=veth_meta["address"],
            abi=veth_meta["abi"]
        )
        self.logger.info("vETH contract loaded")

        self.logger.info("Loading vSOL contract")
        vsol_meta = self._provider.load_meta("vSOL")
        self.vsol = self._provider.api.eth.contract(
            address=vsol_meta["address"],
            abi=vsol_meta["abi"]
        )
        self.logger.info("vSOL contract loaded")

        self.logger.info("Loading vFTM contract")
        vftm_meta = self._provider.load_meta("vFTM")
        self.vftm = self._provider.api.eth.contract(
            address=vftm_meta["address"],
            abi=vftm_meta["abi"]
        )
        self.logger.info("vFTM contract loaded")

        vaave_meta = self._provider.load_meta("vAAVE")
        self.vaave = self._provider.api.eth.contract(
            address=vaave_meta["address"],
            abi=vaave_meta["abi"]
        )

        vdoge_meta = self._provider.load_meta("vDOGE")
        self.vdoge = self._provider.api.eth.contract(
            address=vdoge_meta["address"],
            abi=vdoge_meta["abi"]
        )


        vflow_meta = self._provider.load_meta("vFLOW")
        self.vflow = self._provider.api.eth.contract(
            address=vflow_meta["address"],
            abi=vflow_meta["abi"]
        )

        vatom_meta = self._provider.load_meta("vATOM")
        self.vatom = self._provider.api.eth.contract(
            address=vatom_meta["address"],
            abi=vatom_meta["abi"]
        )

        vavax_meta = self._provider.load_meta("vAVAX")
        self.vavax = self._provider.api.eth.contract(
            address=vavax_meta["address"],
            abi=vavax_meta["abi"]
        )

        vatom_meta = self._provider.load_meta("vATOM")
        self.vatom = self._provider.api.eth.contract(
            address=vatom_meta["address"],
            abi=vatom_meta["abi"]
        )

        vcrv_meta = self._provider.load_meta("vCRV")
        self.vcrv = self._provider.api.eth.contract(
            address=vcrv_meta["address"],
            abi=vcrv_meta["abi"]
        )

        vperp_meta = self._provider.load_meta("vPERP")
        self.vperp = self._provider.api.eth.contract(
            address=vperp_meta["address"],
            abi=vperp_meta["abi"]
        )

        vmatic_meta = self._provider.load_meta("vMATIC")
        self.vmatic = self._provider.api.eth.contract(
            address=vmatic_meta["address"],
            abi=vmatic_meta["abi"]
        )

        vop_meta = self._provider.load_meta("vOP")
        self.vop = self._provider.api.eth.contract(
            address=vop_meta["address"],
            abi=vop_meta["abi"]
        )
        vape_meta = self._provider.load_meta("vAPE")
        self.vape = self._provider.api.eth.contract(
            address=vape_meta["address"],
            abi=vape_meta["abi"]
        )

    def add_liquidity(
        self,
        params: AddLiquidityParams,
        gas_params: GasParams
    ):
        '''
        Add Liquidity
        Arguments:
        params - AddLiquidityParams object
        gas_params - GasParams object
        '''
        nonce = self._provider.api.eth.get_transaction_count(
            self.account.address
        )

        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }

        tx = self.clearing_house.functions.addLiquidity(
            params.to_dict()
        ).buildTransaction(tx_params)

        signed_tx = self._provider.api.eth.account.sign_transaction(
            tx, self.account.key.hex()
        )

        tx_hash = self._provider.api.eth.send_raw_transaction(
            signed_tx.rawTransaction.hex()
        )

        receipt = self._provider.api.eth.wait_for_transaction_receipt(
            tx_hash
        )

        return receipt

    def remove_liquidity(
        self,
        params: RemoveLiquidityParams,
        gas_params: GasParams
    ):
        '''
        Remove Liquidity
        Arguments:
        params - RemoveLiquidityParams object
        gas_params - GasParams object
        '''
        nonce = self._provider.api.eth.get_transaction_count(
            self.wallet.address)

        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }

        tx = self.clearing_house.functions.removeLiquidity(
            astuple(params)
        ).buildTransaction(tx_params)

        signed_tx = self._provider.api.eth.account.sign_transaction(
            tx, self.account.key.hex()
        )

        tx_hash = self._provider.api.eth.send_raw_transaction(
            signed_tx.rawTransaction.hex()
        )

        receipt = self._provider.api.eth.wait_for_transaction_receipt(
            tx_hash
        )

        return receipt

    def settle_all_funding(
        self,
        trader: str,
        gas_params: GasParams
    ):
        '''
        Settle All Funding
        Arguments:
        trader - wallet address of trader
        gas_params - GasParams object
        '''
        assert(
            Web3.isAddress(trader),
            f"Trader address {trader} must be an address"
        )
        nonce = self._provider.api.eth.get_transaction_count(
            self.wallet.address)

        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }

        tx = self.clearing_house.functions.settleAllFunding(
            trader
        ).buildTransaction(tx_params)

        signed_tx = self._provider.api.eth.account.sign_transaction(
            tx, self.account.key.hex()
        )

        tx_hash = self._provider.api.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )

        receipt = self._provider.api.eth.wait_for_transaction_receipt(
            tx_hash
        )

        return receipt

    def open_position(
        self,
        params: OpenPositionParams,
        gas_params: GasParams
    ):
        '''
        Open Position
        Arguments:
        params - OpenPositionParams object
        gas_params - GasParams object
        '''
        nonce = self._provider.api.eth.get_transaction_count(
            self.account.address
        )

        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }

        tx = self.clearing_house.functions.openPosition(
            astuple(params)
        ).build_transaction(tx_params)

        signed_tx = self._provider.api.eth.account.sign_transaction(
            tx, self.account.key.hex()
        )

        tx_hash = self._provider.api.eth.send_raw_transaction(
            signed_tx.rawTransaction.hex()
        )

        receipt = self._provider.api.eth.wait_for_transaction_receipt(
            tx_hash
        )

        return receipt

    def close_position(
        self,
        params: ClosePositionParams,
        gas_params: GasParams
    ):
        '''
        Close Position
        Arguments:
        params - ClosePositionParams object
        gas_params - GasParams object
        '''
        nonce = self._provider.api.eth.get_transaction_count(
            self.account.address
        )

        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }

        tx = self.clearing_house.functions.closePosition(
            astuple(params)
        ).buildTransaction(tx_params)

        signed_tx = self._provider.api.eth.account.sign_transaction(
            tx, self.account.key.hex()
        )

        tx_hash = self._provider.api.eth.send_raw_transaction(
            signed_tx.rawTransaction.hex()
        )

        receipt = self._provider.api.eth.wait_for_transaction_receipt(
            tx_hash
        )

        return receipt

    def liquidate(
        self,
        trader: str,
        base_token: str,
        gas_params: GasParams
    ):
        '''
        Liquidate
        Arguments:
        trader - wallet address of trader
        base_token - contract address of base token
        gas_params - GasParams object
        '''
        assert(
            Web3.isAddress(trader),
            f'trader address {trader} must be a checksum address'
        )
        assert(
            Web3.isAddress(base_token),
            f'Base Token address {base_token} must be a checkcum address'
        )

        nonce = self._provider.api.eth.get_transaction_count(
            self.wallet.address)

        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }

        tx = self.clearing_house.functions.liquidate(
            trader,
            base_token
        ).buildTransaction(tx_params)

        signed_tx = self._provider.api.eth.account.sign_transaction(
            tx, self.account.key.hex()
        )

        tx_hash = self._provider.api.eth.send_raw_transaction(
            signed_tx.rawTransaction.hex()
        )

        receipt = self._provider.api.eth.wait_for_transaction_receipt(
            tx_hash
        )

        return receipt

    # TODO: implement cancelExcessOrders

    def cancel_all_excess_orders(
        self,
        maker: str,
        base_token: str,
        gas_params: GasParams
    ):
        '''
        Cancel All Excess Orders
        Arguments:
        maker - wallet address of maker
        base_token - contract address of base token
        gas_params - GasParams object
        '''
        assert(
            Web3.isAddress(maker),
            f'Maker address {maker} must be a checksum address'
        )
        assert(
            Web3.isAddress(base_token),
            f'Base Token address {base_token} must be a checksum address'
        )

        nonce = self._provider.api.eth.get_transaction_count(
            self.account.address
        )

        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }

        tx = self.clearing_house.functions.cancelAllExcessOrders(
            maker,
            base_token
        ).buildTransaction(tx_params)

        signed_tx = self._provider.api.eth.account.sign_transaction(
            tx, self.account.key.hex()
        )

        tx_hash = self._provider.api.eth.send_raw_transaction(
            signed_tx.rawTransaction.hex()
        )

        receipt = self._provider.api.eth.wait_for_transaction_receipt(
            tx_hash
        )

        return receipt

    def close_position_in_closed_market(
        self,
        trader: str,
        base_token: str,
        gas_params: GasParams
    ):
        '''
        Close Position in Closed Market
        Arguments:
        trader - wallet address of trader
        base_token - contract address of base token
        gas_params - GasParams object
        '''
        assert(
            Web3.isAddress(trader),
            f'trader address {trader} must be a checksum address'
        )
        assert(
            Web3.isAddress(base_token),
            f'Base Token address {base_token} must be a checkcum address'
        )

        nonce = self._provider.api.eth.get_transaction_count(
            self.account.address
        )

        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }

        tx = self.clearing_house.functions.closePositionInClosedMarket(
            trader,
            base_token
        ).buildTransaction({
            'nonce': nonce,
            **gas_params.to_dict()
        })

        signed_tx = self._provider.api.eth.sign_transaction(
            tx, self.wallet.key
        )

        receipt = self._provider.api.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )

        return receipt

    def uniswap_v3_mint_callback(
        self,
        amount0Owed: int,
        amount1Owed: int,
        data: str,
        gas_params: GasParams
    ):
        '''
        Uniswap V3 mint callback.
        '''
        nonce = self._provider.api.eth.get_transaction_count(
            self.account.address
        )

        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }

        tx = self.clearing_house.functions.uninswapV3MintCallback(
            amount0Owed,
            amount1Owed,
            data
        ).buildTransaction(tx_params)

        signed_tx = self._provider.api.eth.account.sign_transaction(
            tx, self.account.key.hex()
        )

        tx_hash = self._provider.api.eth.send_raw_transaction(
            signed_tx.rawTransaction.hex()
        )

        receipt = self._provider.api.eth.wait_for_transaction_receipt(
            tx_hash
        )

        return receipt

    def uniswap_v3_swap_callback(
        self,
        amount0Delta: int,
        amount1Delta: int,
        data: str,
        gas_params: GasParams
    ):
        '''
        Uniswap V3 Swap Callback.
        '''
        nonce = self._provider.api.eth.get_transaction_count(
            self.account.address
        )

        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }

        tx = self.clearing_house.functions.uninswapV3SwapCallback(
            amount0Delta,
            amount1Delta,
            data
        ).buildTransaction(tx_params)

        signed_tx = self._provider.api.eth.account.sign_transaction(
            tx, self.account.key.hex()
        )

        tx_hash = self._provider.api.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )

        receipt = self._provider.api.eth.wait_for_transaction_receipt(
            tx_hash
        )

        return receipt

    def get_quote_token(self):
        '''
        Returns address of quote token contract.
        '''
        return self.clearing_house.functions.getQuoteToken(
        ).call()

    def get_uniswap_v3_factory(self):
        '''
        Returns address of UniswapV3Factory contracy.
        '''
        return self.clearing_house.functions.getUniswapV3Factory(
        ).call()

    def get_clearing_house_config(self):
        '''
        Returns address of ClearingHouseConfig contract.
        '''
        return self.clearing_house.functions.getClearingHouseConfig(
        ).call()

    def get_vault(self):
        '''
        Returns address of Vault contract.
        '''
        return self.clearing_house.functions.getVault().call()

    def get_exchange(self):
        '''
        Returns address of Exchange contract.
        '''
        return self.clearing_house.functions.getExchange().call()

    def get_order_book(self):
        '''
        Returns address of OrderBook contract.
        '''
        return self.clearing_house.functions.getOrderBook().call()

    def get_account_balance(self):
        '''
        Returns address of AccountBalance contract.
        '''
        return self.clearing_house.functions.getAccountBalance().call()

    def get_insurance_fund(self):
        '''
        Returns address of InsuranceFund contract.
        '''
        return self.clearing_house.functions.getInsuraceFund().call()

    def get_account_value(
        self,
        trader: str
    ):
        '''
        Returns account value.
        Arguments:
        trader - wallet address of trader.
        '''
        assert(
            Web3.isAddress(trader),
            f'trader address {trader} must be a checksum address'
        )
        return self.clearing_house.functions.getAccountValue(trader).call()
