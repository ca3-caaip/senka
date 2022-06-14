class UnknownTransaction:
    def __init__(
        self,
        chain: str,
        address: str,
        transaction_id: str,
        reason: str,
        executed_at: str,
    ):
        self.chain = chain
        self.address = address
        self.transaction_id = transaction_id
        self.reason = reason
        self.executed_at = executed_at
