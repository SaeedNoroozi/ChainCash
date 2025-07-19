from web3 import AsyncWeb3
from web3.middleware import ExtraDataToPOAMiddleware
from chaincash.utils.logger import logger
from chaincash.utils.exceptions import BlockchainConnectionError
from chaincash.core.constants import RPC_URL, USDT_CONTRACT

class BlockchainClient:
    """
    A class for interacting with the blockchain.

    Provides methods for getting balances of BNB and USDT tokens.

    Attributes:
        web3 (AsyncWeb3): An instance of AsyncWeb3 for interacting with the blockchain.
        usdt_contract (str): The address of the USDT contract.

    Methods:
        check_connection(): Checks if the connection to the blockchain is established.
        get_bnb_balance(address: str): Gets the balance of BNB tokens for a given address.
        get_usdt_balance(address: str): Gets the balance of USDT tokens for a given address.
    """

    def __init__(self, rpc_url: str | None = None) -> None:
        """
        Initializes the BlockchainClient instance.

        Args:
            rpc_url (str): The RPC URL of the blockchain. if not provided, it will use the RPC URL from the constants.

        Raises:
            ValueError: If the RPC URL is not provided.
        """

        self.rpc_url = rpc_url or RPC_URL
        if not self.rpc_url:
            raise ValueError("RPC URL not provided.")
        
        self.web3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(self.rpc_url))
        self.web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        self.USDT_CONTRACT = AsyncWeb3.to_checksum_address(USDT_CONTRACT)
        self.usdt_contract = self.web3.eth.contract(
            address = self.USDT_CONTRACT,
            abi     = self.USDT_ABI,
        )

    async def check_connection(self) -> None:
        """
        Checks if the connection to the blockchain is established.

        Raises:
            ValueError: If the connection to the blockchain is not established.
        """

        if not await self.web3.is_connected():
            logger.error("Failed to connect to blockchain RPC.")
            raise BlockchainConnectionError("Unable to connect to RPC node.")

        logger.info("Connected to blockchain RPC.")

    async def get_bnb_balance(self, address: str) -> float:
        """
        Gets the balance of BNB tokens for a given address.

        Args:
            address (str): The address of the account.

        Returns:
            float: The balance of BNB tokens.
        """

        wei_balance = await self.web3.eth.get_balance(
            self.web3.to_checksum_address(address)
        )
        return self.web3.from_wei(wei_balance, "ether")

    async def get_usdt_balance(self, address: str) -> float:
        """
        Gets the balance of USDT tokens for a given address.

        Args:
            address (str): The address of the account.

        Returns:
            float: The balance of USDT tokens.
        """
        
        balance = await self.usdt_contract.functions.balanceOf(
            self.web3.to_checksum_address(address)
        ).call()

        return balance / 1e18

    @property
    def USDT_ABI(self):
        return [
            {
                "constant": False,
                "inputs": [
                    {"name": "_to", "type": "address"},
                    {"name": "_value", "type": "uint256"}
                ],
                "name": "transfer",
                "outputs": [{"name": "", "type": "bool"}],
                "type": "function",
                "stateMutability": "nonpayable",
            },
            {
                "constant": True,
                "inputs": [
                    {"name": "_owner", "type": "address"}
                ],
                "name": "balanceOf",
                "outputs": [
                    {"name": "balance", "type": "uint256"}
                ],
                "type": "function",
                "stateMutability": "view",
            },
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "name": "from", "type": "address"},
                    {"indexed": True, "name": "to", "type": "address"},
                    {"indexed": False, "name": "value", "type": "uint256"}
                ],
                "name": "Transfer",
                "type": "event"
            }
        ]
