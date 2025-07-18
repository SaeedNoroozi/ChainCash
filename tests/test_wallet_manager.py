from chaincash.core.wallet_manager import WalletManager
from chaincash.core.models import Wallet

def test_create_wallet():
    """
    Test that WalletManager.create_wallet() returns a valid Wallet instance
    with correct user_id, address and private_key.
    """
    user_id = "test_user_001"
    wallet = WalletManager.create_wallet(user_id)

    assert isinstance(wallet, Wallet), "Returned object is not an instance of Wallet"
    assert wallet.user_id == user_id, "Wallet user_id mismatch"
    assert wallet.address.startswith("0x"), "Wallet address is invalid"
    assert len(wallet.private_key) == 64, "Wallet private_key is invalid"