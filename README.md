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
# python src/main chain_name address > result.csv

ex.
$ python src/main.py osmosis 0x0000000000000000000000000000000000000 > result.csv
```

change chain or address whatever you want to check.
