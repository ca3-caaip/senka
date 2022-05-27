import argparse
import os
from pathlib import Path

from senka.senka import Senka

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--chain",
        help="--chain [chain]",
    )
    parser.add_argument(
        "--address",
        help="--address [address]",
    )
    parser.add_argument(
        "--data_path",
        help="--data_path [address]",
    )
    setting = {}
    args = parser.parse_args()
    if args.chain is not None and args.address is not None:
        if args.chain == "bsc":
            setting["bscscan_key"] = os.environ["BSCSCAN_KEY"]
        senka = Senka(setting, "./pyproject.toml")
        caaj = senka.get_caaj_csv("address", args.chain, args.address)
    elif args.chain is not None and args.data_path is not None:
        senka = Senka(setting, "./pyproject.toml")
        data = Path(f"{os.path.abspath(args.data_path)}").read_text()
        caaj = senka.get_caaj_csv("csv", args.chain, data)
    else:
        raise Exception("Invalid arguments")

    print(caaj)
