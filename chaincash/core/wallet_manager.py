from web3 import AsyncWeb3
from chaincash.core.models import Wallet

class WalletManager:
    """
    WalletManager is a class for generating and managing wallet keypairs.
    """

    @staticmethod
    def create_wallet(user_id: int) -> Wallet:
        """
        Creates a new wallet keypair and returns it as a Wallet object.

        Args:
            user_id (int): The ID of the user associated with the wallet.

        Returns:
            Wallet: The generated wallet instance.
        """
        account = AsyncWeb3().eth.account.create()
        return Wallet(
                user_id     = user_id,
                address     = account.address,
                private_key = account.key.hex()
        )