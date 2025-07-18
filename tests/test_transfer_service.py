from chaincash.core.transfer_service import TransferService
from chaincash.core.blockchain_client import BlockchainClient
from chaincash.core.models import TransferResult
from chaincash.utils.exceptions import TransferError
from unittest.mock import AsyncMock, MagicMock
import pytest

@pytest.mark.asyncio
async def test_send_bnb_success():
    client = MagicMock(spec=BlockchainClient)
    client.web3 = MagicMock()
    client.web3.to_checksum_address = lambda x: x
    client.web3.to_wei = lambda x, _: int(x * 1e18)
    client.web3.from_wei = lambda x, _: x / 1e18

    client.web3.eth.get_transaction_count = AsyncMock(return_value=1)
    client.web3.eth.get_balance = AsyncMock(return_value=int(2e18))
    client.web3.eth.gas_price = 1
    client.web3.eth.send_raw_transaction = AsyncMock(return_value=b"\x12\x34")

    client.usdt_contract = MagicMock()

    sender_account = MagicMock()
    sender_account.address = "0xSender"
    sender_account.sign_transaction.return_value.rawTransaction = b"signed"

    client.web3.eth.account.from_key.return_value = sender_account

    service = TransferService(client, "private_key")

    result = await service.send_bnb("0xRecipient", 1)

    assert isinstance(result, TransferResult)
    assert result.token == "BNB"
    assert result.amount == 1


@pytest.mark.asyncio
async def test_send_bnb_insufficient_balance():
    client = MagicMock(spec=BlockchainClient)
    client.web3 = MagicMock()
    client.web3.to_checksum_address = lambda x: x
    client.web3.to_wei = lambda x, _: int(x * 1e18)

    client.web3.eth.get_transaction_count = AsyncMock(return_value=1)
    client.web3.eth.get_balance = AsyncMock(return_value=int(0.5e18))
    client.web3.eth.gas_price = 1

    client.usdt_contract = MagicMock()

    sender_account = MagicMock()
    sender_account.address = "0xSender"
    client.web3.eth.account.from_key.return_value = sender_account

    service = TransferService(client, "private_key")

    with pytest.raises(TransferError):
        await service.send_bnb("0xRecipient", 1)


@pytest.mark.asyncio
async def test_send_usdt_success():
    client = MagicMock(spec=BlockchainClient)
    client.web3 = MagicMock()
    client.web3.to_checksum_address = lambda x: x

    client.web3.eth.get_transaction_count = AsyncMock(return_value=1)
    client.web3.eth.gas_price = 1
    client.web3.eth.send_raw_transaction = AsyncMock(return_value=b"\x12\x34")

    usdt_contract = MagicMock()
    balanceOf_func = AsyncMock(return_value=int(2e18))
    usdt_contract.functions.balanceOf.return_value.call = balanceOf_func
    usdt_contract.functions.transfer.return_value.build_transaction.return_value = {}

    client.usdt_contract = usdt_contract

    sender_account = MagicMock()
    sender_account.address = "0xSender"
    sender_account.sign_transaction.return_value.rawTransaction = b"signed"

    client.web3.eth.account.from_key.return_value = sender_account

    service = TransferService(client, "private_key")

    result = await service.send_usdt("0xRecipient", 1)

    assert isinstance(result, TransferResult)
    assert result.token == "USDT"
    assert result.amount == 1


@pytest.mark.asyncio
async def test_send_usdt_insufficient_balance():
    client = MagicMock(spec=BlockchainClient)
    client.web3 = MagicMock()
    client.web3.to_checksum_address = lambda x: x

    client.web3.eth.get_transaction_count = AsyncMock(return_value=1)
    client.web3.eth.gas_price = 1

    usdt_contract = MagicMock()
    balanceOf_func = AsyncMock(return_value=int(0.5e18))
    usdt_contract.functions.balanceOf.return_value.call = balanceOf_func
    usdt_contract.functions.transfer.return_value.build_transaction.return_value = {}

    client.usdt_contract = usdt_contract

    sender_account = MagicMock()
    sender_account.address = "0xSender"
    client.web3.eth.account.from_key.return_value = sender_account

    service = TransferService(client, "private_key")

    with pytest.raises(TransferError):
        await service.send_usdt("0xRecipient", 1)
