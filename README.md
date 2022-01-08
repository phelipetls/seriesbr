# seriesbr: Uma biblioteca de Python para consultar bancos de dados com séries temporais do BCB, IPEA e IBGE

[![pypi version](https://img.shields.io/pypi/v/seriesbr.svg)](https://pypi.org/project/seriesbr/)
[![readthedocs status](https://readthedocs.org/projects/seriesbr/badge/?version=latest)](https://seriesbr.readthedocs.io/en/latest/?badge=latest)

**seriesbr** é útil para pesquisadores e estudantes que precisam consultar
séries temporais dos bancos de dados do Banco Central do Brasil (BCB),
Instituto de Pesquisa Econômica Aplicada (IPEA) e Instituto Brasileiro de
Geografia e Estatística (IBGE) de forma automatizada.

É inspirado nos seguintes pacotes escritos em R:
[rbcb](https://github.com/wilsonfreitas/rbcb),
[ipeaData](https://github.com/ipea/ipeaData) e
[sidrar](https://github.com/cran/sidrar).

# API

A biblioteca possui três módulos, `bcb`, `ipea` e `ibge`. Cada uma possui uma
função chamada `get_series` que aceita o identificador da série e retorna um
pandas `DataFrame` com os dados.

Leia a [documentação](https://seriesbr.readthedocs.io/) para aprender mais.

# Exemplo

```python
from seriesbr import bcb

bcb.get_series({"Spread": 20786, "Selic": 11}, start="2015", end="2016", join="inner")
```

```
            Spread     Selic
Date                        
2015-04-01   28.41  0.047279
2015-06-01   29.75  0.049037
2015-07-01   30.67  0.050788
2015-09-01   30.89  0.052531
2015-10-01   32.00  0.052531
2015-12-01   31.08  0.052531
2016-02-01   35.15  0.052531
2016-03-01   36.44  0.052531
2016-04-01   38.05  0.052531
2016-06-01   38.36  0.052531
2016-07-01   39.21  0.052531
2016-08-01   39.71  0.052531
2016-09-01   40.22  0.052531
2016-11-01   40.84  0.051660
2016-12-01   39.12  0.050788
```

# Licença

[MIT](https://github.com/phelipetls/seriesbr/blob/master/LICENSE)
