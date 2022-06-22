from typing import List
from xmlrpc.client import boolean

from senkalib.caaj_journal import CaajJournal
from senkalib.platform.transaction import Transaction
from senkalib.token_original_id_table import TokenOriginalIdTable


class TestZeroPlugin:
    platform = "test_zero"

    @classmethod
    def can_handle(cls, transaction: Transaction) -> boolean:
        return True

    @classmethod
    def get_caajs(
        cls,
        address: str,
        transaction: Transaction,
        token_original_ids: TokenOriginalIdTable,
    ) -> List[CaajJournal]:
        return []
