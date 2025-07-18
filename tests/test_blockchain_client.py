import pytest
from chaincash.core.blockchain_client import BlockchainClient

TEST_ADDRESS = "0xF977814e90dA44bFA03b6295A0616a897441aceC"

@pytest.mark.asyncio
async def test_connection():
    """
    Test the connection to the blockchain.
    """
    client = BlockchainClient()
    await client.check_connection()

@pytest.mark.asyncio
async def test_get_bnb_balance():
    """
    Test fetching BNB balance of a known address.
    """
    client = BlockchainClient()
    balance = await client.get_bnb_balance(TEST_ADDRESS)
    assert balance > 0

@pytest.mark.asyncio
async def test_get_usdt_balance():
    """
    Test fetching USDT balance of a known address
    """
    client = BlockchainClient()
    balance = await client.get_usdt_balance(TEST_ADDRESS)
    assert balance > 0