from typing import Callable, Dict
from chaincash.core.blockchain_client import BlockchainClient
from chaincash.core.models import DepositEvent
import asyncio

class Monitor:
    """
    Monitor class for monitoring blockchain transactions and events.
    """

    def __init__(self, blockchain_client: BlockchainClient, address_map: Dict[str | int, str], poll_interval: int = 10):
        """
        Initialize the Monitor class.

        Args:
            blockchain_client (BlockchainClient): An instance of the BlockchainClient class.
            address_map (Dict[str | int, str]): A dictionary mapping user IDs to addresses.
            poll_interval (int, optional): The interval in seconds at which to poll the blockchain. Defaults to 10.
        """

        self.poll_interval     = poll_interval
        self.blockchain_client = blockchain_client
        self.address_map       = {k: v.lower() for k, v in address_map.items()}

    async def start(self, callback: Callable[[DepositEvent], None]) -> None:
        """
        Start the monitoring process.

        Args:
            callback: function(user_id, address, amount, tx_hash)
        """

        print("[Monitor] Stating monitoring process...")
        latest_block = await self.blockchain_client.web3.eth.block_number
        
        while True:
            block = await self.blockchain_client.web3.eth.get_block(latest_block + 1, full_transactions=True)
            if block is None:
                await asyncio.sleep(self.poll_interval)
                continue

            for tx in block["transactions"]:
                to_address = (tx.get("to") or "").lower()
                if to_address in self.address_map.values():
                    user_id    = next(uid for uid, addr in self.address_map.items() if addr == to_address)
                    amount_bnb = float(self.blockchain_client.web3.from_wei(tx["value"], "ether"))
                    tx_hash    = tx["hash"].hex()

                    print(f"[Monitor] New transaction: {user_id} - {to_address} - {amount_bnb:.6f} BNB - {tx_hash}")

                    await callback(DepositEvent(
                        user_id = user_id,
                        token   = "BNB",
                        amount  = amount_bnb,
                        tx_hash = tx_hash
                    ))

            latest_block += 1