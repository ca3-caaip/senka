from decimal import Decimal
from typing import List
from xmlrpc.client import boolean

from senkalib.caaj_journal import CaajJournal
from senkalib.platform.transaction import Transaction
from senkalib.token_original_id_table import TokenOriginalIdTable


class TestOnePlugin:
    platform = "test_one"

    @classmethod
    def can_handle(cls, transaction: Transaction) -> boolean:
        if transaction.transaction_id != "unknown":
            return True
        else:
            return False

    @classmethod
    def get_caajs(
        cls,
        address: str,
        transaction: Transaction,
        token_original_ids: TokenOriginalIdTable,
    ) -> List[CaajJournal]:
        executed_at = "2022-01-12 11:11:11"
        platform = "platform"
        application = "application"
        service = "service"
        transaction_id = (
            "0x36512c7e09e3570dfc53176252678ee9617660550d36f4da797afba6fc55bba6"
        )
        trade_uuid = "bbbbbbddddddd"
        type = "deposit"
        amount = Decimal("0.005147")
        token_symbol = "testone"
        token_original_id = (
            "ibc/46B44899322F3CD854D2D46DEEF881958467CDD4B3B10086DA49296BBED94BED"
        )
        token_symbol_uuid = "3a2570c5-15c4-2860-52a8-bff14f27a236"
        caaj_from = "0x111111111111111111111"
        caaj_to = "0x222222222222222222222"
        comment = "hello world"

        cj = CaajJournal(
            executed_at,
            platform,
            application,
            service,
            transaction_id,
            trade_uuid,
            type,
            amount,
            token_symbol,
            token_original_id,
            token_symbol_uuid,
            caaj_from,
            caaj_to,
            comment,
        )
        return [cj]
