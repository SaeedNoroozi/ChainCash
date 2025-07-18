class ChainCashError(Exception):
    """
    Base exception for all ChainCash errors.
    """
    pass

class BlockchainConnectionError(ChainCashError):
    """
    Raised when blockchain connection to the RPC node fails.
    """
    pass

class WalletCreationError(ChainCashError):
    """
    Raised when wallet creation or validation fails.
    """
    pass

class TransferError(ChainCashError):
    """
    Raised when a transfer transaction fails.
    """
    pass
