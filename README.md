# senka

## docker

### for start

$ docker-compose up -d

### for access to shell in the container

$ docker-compose exec senka bash

### for end

$ docker-compose down

### for remove

$ docker-compose down --rmi all --volumes --remove-orphans

## for developers

1. Install poetry to set up python environment

```
If you have not yet installed poetry, first install poetry as follows
$ curl -sSL https://install.python-poetry.org | python3 -
Set the poetry path as the log shows.
$ export PATH="$HOME/.local/bin:$PATH"
Set up the python environment as follows.
$ poetry config virtualenvs.in-project true && poetry install
```

2. Install pre-commit

```
# Before committing, we use pre-commmit hook to check the code style.
# Install pre-commit in the following way
$ pre-commit install

# If you are using docker and the venv environment is not enabled, please do the following to enable it.
$ source /app/.venv/bin/activate

```

## for test

```

$ cd /app
$ curl -sSL https://install.python-poetry.org | python -
$ poetry config virtualenvs.in-project true && poetry install
$ poetry shell
$ pytest --cov=src --cov-branch --cov-report=term-missing -vv

```

## for adding plugin

1. Add plugin pacakage definition to `[tool.poetry.dependencies]` section in `pyproject.toml`.
2. Add plugin pacakage to list of `senka_plugin` variable of `[senka.plugin]` section in `pyproject.toml`.

ex. Here is a part of `pyproject.toml`. Now osmosis_plugin is activated in this example.

```

[tool.poetry.dependencies]
python = "^3.8"
web3 = "^5.28.0"
bscscan-python = "^2.0.0"
pandas = "^1.4.1"
senkalib = "latest"
toml = "^0.10.2"
osmosis_plugin = {git = 'https://github.com/ca3-caaip/osmosis_plugin.git', rev ='5b7357194426efad263a021824d82a67bca02220' }

[senka.plugin]
senka_plugin = [
    'osmosis_plugin'
]

```

change plugin repository url for what you want.

## for execution from CLI

```

$ cd /app/
$ curl -sSL https://install.python-poetry.org | python -
$ poetry config virtualenvs.in-project true && poetry install
$ poetry shell

# If you want to execute senka with platform and address, please use the following command.
$ python src/main.py --platform=<platform> --address=<address>
ex.
$ python src/main.py --platform=osmosis --address=0x0000000000000000000000000000000000000

# If you want to execute senka with platform and data, please use the following command.
$ python src/main.py --platform=<platform> --data_path=<data>
ex.
$ python src/main.py --platform bitbank --data_path test/testdata/bitbank/bitbank_exchange.csv
```
