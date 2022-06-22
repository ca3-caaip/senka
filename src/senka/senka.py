from typing import List, Tuple, Union

import pandas as pd
from senkalib.caaj_journal import CaajJournal
from senkalib.platform.transaction import Transaction
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
        platform: str,
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
            platform,
            transaction_params,
        )
        caaj_dict_list = list(map(lambda x: vars(x), caaj_list))
        df = pd.DataFrame(caaj_dict_list)
        df = df.sort_values("executed_at")
        caaj_csv = df.to_csv(None, index=False)
        return caaj_csv

    def get_caaj(
        self,
        platform: str,
        transaction_params: dict,
    ) -> Tuple[List[CaajJournal], List[UnknownTransaction]]:
        token_original_ids = TokenOriginalIdTable(Senka.TOKEN_ORIGINAL_IDS_URL)
        available_platforms = self.get_available_platforms()
        if platform.lower() not in available_platforms:
            raise ValueError("this platform is not supported.")

        transaction_generator = list(
            filter(
                lambda x: x.platform.lower() == platform.lower(),
                SenkaLib.get_available_platform(),
            )
        )[0]

        transaction_params["settings"] = self.setting
        transactions = transaction_generator.get_transactions(transaction_params)
        plugins = PluginManager.get_plugins(platform, self.setting_toml_path)
        address = ""
        if transaction_params["type"] == "address":
            address = transaction_params["data"]

        elif transaction_params["type"] == "csv":
            address = "self"

        return Senka._make_caaj_from_transaction_and_plugins(
            transactions, plugins, token_original_ids, platform, address
        )

    @staticmethod
    def get_available_platforms() -> List[str]:
        platforms = SenkaLib.get_available_platform()
        platforms = list(map(lambda x: x.platform, platforms))
        return platforms

    @staticmethod
    def _make_caaj_from_transaction_and_plugins(
        transactions: list[Transaction],
        plugins: list,
        token_original_ids: TokenOriginalIdTable,
        platform: str,
        address: str,
    ) -> Tuple[List[CaajJournal], List[UnknownTransaction]]:
        caaj = []
        unknown_transactions = []
        for tx in transactions:
            applicable_plugin = next(filter(lambda p: p.can_handle(tx), plugins), None)
            if applicable_plugin:
                caaj.extend(
                    applicable_plugin.get_caajs(address, tx, token_original_ids)
                )
            else:
                unknown_transactions.append(
                    UnknownTransaction(
                        platform,
                        address,
                        tx.transaction_id,
                        "there is no applicable plugin",
                        tx.get_timestamp(),
                    )
                )
        return caaj, unknown_transactions
