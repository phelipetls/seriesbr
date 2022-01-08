Banco Central do Brasil
=======================

Obtendo séries
--------------

Para consultar as séries de código 20786 (spread bancário) e 4189 (Selic), use
a função :py:func:`seriesbr.bcb.get_series`:

.. ipython:: python

   from seriesbr import bcb

   bcb.get_series(20786, 4189)

Para facilitar, é possível passar um dicionário para nomear as colunas:

.. ipython:: python

   bcb.get_series({"Spread": 20786, "Selic": 4189})


É possível filtrar por período com os argumentos ``start_date`` e ``end_date``:

.. ipython:: python

   bcb.get_series(20786, start="2011", end="07-2012")

Ou obter as últimas 5 observações com o argumento ``last_n``:

.. ipython:: python

   bcb.get_series(20786, last_n=5)


Outros argumentos nomeados são passados para a função ``pandas.concat``. Por
exemplo, caso você queira obter somente os períodos em que ambas as séries
contenham dados:

.. ipython:: python

   bcb.get_series(20786, 4189, join="inner")
