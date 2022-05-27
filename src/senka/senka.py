from typing import List, Tuple, Union

import pandas as pd
from senkalib.caaj_journal import CaajJournal
from senkalib.senka_lib import SenkaLib
from senkalib.senka_setting import SenkaSetting
from senkalib.token_original_id_table import TokenOriginalIdTable

from senka.plugin_manager import PluginManager
from senka.unknown_transaction import UnknownTransaction

pd.set_option("display.max_columns", 50)


class Senka:
    TOKEN_ORIGINAL_IDS_URL = "https://raw.githubusercontent.com/ca3-caaip/token_original_id/master/token_original_id.csv"

    def __init__(self, setting_dict, setting_toml_path: str):
        self.setting = SenkaSetting(setting_dict)
        self.setting_toml_path = setting_toml_path
        pass

    def get_caaj_csv(
        self,
        data_type: str,
        chain: str,
        data: str,
        starttime: Union[int, None] = None,
        endtime: Union[int, None] = None,
        startblock: Union[int, None] = None,
        endblock: Union[int, None] = None,
    ) -> str:
        transaction_params = {
            "type": data_type,
            "data": data,
            "starttime": starttime,
            "endtime": endtime,
            "startblock": startblock,
            "endblock": endblock,
        }

        caaj_list, unknown_transactions_list = self.get_caaj(
            chain,
            transaction_params,
        )
        caaj_dict_list = list(map(lambda x: vars(x), caaj_list))
        df = pd.DataFrame(caaj_dict_list)
        df = df.sort_values("executed_at")
        caaj_csv = df.to_csv(None, index=False)
        return caaj_csv

    def get_caaj(
        self,
        chain: str,
        transaction_params: dict,
    ) -> Tuple[List[CaajJournal], List[UnknownTransaction]]:
        token_original_ids = TokenOriginalIdTable(Senka.TOKEN_ORIGINAL_IDS_URL)
        available_chains = self.get_available_chains()
        if chain.lower() not in available_chains:
            raise ValueError("this chain is not supported.")

        transaction_generator = list(
            filter(
                lambda x: x.chain.lower() == chain.lower(),
                SenkaLib.get_available_chain(),
            )
        )[0]

        transaction_params["settings"] = self.setting
        transactions = transaction_generator.get_transactions(transaction_params)
        plugins = PluginManager.get_plugins(chain, self.setting_toml_path)
        address = ""
        if transaction_params["type"] == "address":
            address = transaction_params["data"]

        elif transaction_params["type"] == "csv":
            address = "self"

        return Senka._make_caaj_from_transaction_and_plugins(
            transactions, plugins, token_original_ids, chain, address
        )

    @staticmethod
    def get_available_chains() -> List[str]:
        chains = SenkaLib.get_available_chain()
        chains = list(map(lambda x: x.chain, chains))
        return chains

    @staticmethod
    def _make_caaj_from_transaction_and_plugins(
        transactions: List[CaajJournal],
        plugins: list,
        token_original_ids: TokenOriginalIdTable,
        chain: str,
        address: str,
    ) -> Tuple[List[CaajJournal], List[UnknownTransaction]]:
        caaj = []
        unknown_transactions = []
        for transaction in transactions:
            for plugin in plugins:
                if plugin.can_handle(transaction):
                    caaj_peace = plugin.get_caajs(
                        address, transaction, token_original_ids
                    )
                    caaj.extend(caaj_peace)
                    break
                else:
                    unknown_transactions.append(
                        UnknownTransaction(
                            chain,
                            address,
                            transaction.transaction_id,
                            "there is no applicable plugin",
                        )
                    )
        return caaj, unknown_transactions
