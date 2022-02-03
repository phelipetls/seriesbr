# seriesbr: Uma biblioteca em Python para consultar bancos de dados com séries temporais do BCB, IPEA e IBGE

[![pypi version](https://img.shields.io/pypi/v/seriesbr.svg)](https://pypi.org/project/seriesbr/)
[![readthedocs status](https://readthedocs.org/projects/seriesbr/badge/?version=latest)](https://seriesbr.readthedocs.io/en/latest/?badge=latest)
![codecov](https://codecov.io/gh/phelipetls/seriesbr/branch/master/graph/badge.svg)

**seriesbr** ajuda a consultar, de forma programática, séries temporais dos
bancos de dados do Banco Central do Brasil (BCB), Instituto de Pesquisa
Econômica Aplicada (IPEA) e Instituto Brasileiro de Geografia e Estatística
(IBGE).

É inspirado nos seguintes pacotes escritos em R:
[rbcb](https://github.com/wilsonfreitas/rbcb),
[ipeaData](https://github.com/ipea/ipeaData) e
[sidrar](https://github.com/cran/sidrar).

# API

A biblioteca possui três módulos, `bcb`, `ipea` e `ibge`. Cada uma possui uma
função chamada `get_series` que aceita o identificador da série e retorna um
[`DataFrame`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).

Para mais detalhes, leia a [documentação](https://seriesbr.readthedocs.io/).

# Exemplo

```python
from seriesbr import bcb

bcb.get_series(20786, start="2015", end="2016")
```

```
            20786
Date
2015-01-01  26.54
2015-02-01  27.46
2015-03-01  27.21
2015-04-01  28.41
2015-05-01  29.09
2015-06-01  29.75
2015-07-01  30.67
2015-08-01  31.05
2015-09-01  30.89
2015-10-01  32.00
2015-11-01  32.66
2015-12-01  31.08
2016-01-01  33.62
2016-02-01  35.15
2016-03-01  36.44
2016-04-01  38.05
2016-05-01  38.50
2016-06-01  38.36
2016-07-01  39.21
2016-08-01  39.71
2016-09-01  40.22
2016-10-01  41.18
2016-11-01  40.84
2016-12-01  39.12
```

# Contribuindo

Sinta-se à vontade para abrir issues ou pull requests.

Caso queira contribuir, primeiro instale o `poetry` e depois `poetry install`.
Rode os testes localmente com `poetry run pytest`.

# Licença

[MIT](https://github.com/phelipetls/seriesbr/blob/master/LICENSE)
