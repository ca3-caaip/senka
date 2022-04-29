import os
import sys

from senka.senka import Senka

if __name__ == "__main__":
    args = sys.argv
    chain = args[1]
    address = args[2]
    setting = {}
    if chain == "bsc":
        setting["bscscan_key"] = os.environ["BSCSCAN_KEY"]
    senka = Senka(setting, "./pyproject.toml")
    caaj = senka.get_caaj_csv(chain, address)
    print(caaj)
