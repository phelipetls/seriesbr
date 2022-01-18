Banco Central do Brasil
=======================

Obtendo séries
--------------

Para consultar as séries de código 20786 (spread bancário) e 4189 (Selic), use
a função :py:func:`seriesbr.bcb.get_series`:

.. ipython:: python

   from seriesbr import bcb

   bcb.get_series(20786)

É possível filtrar por período com os argumentos ``start_date`` e ``end_date``:

.. ipython:: python

   bcb.get_series(20786, start="2011", end="07-2012")

Ou obter as últimas 5 observações com o argumento ``last_n``:

.. ipython:: python

   bcb.get_series(20786, last_n=5)

Obtendo metadados
-----------------

Para obter os metadados de uma série:

.. ipython:: python

   bcb.get_metadata(20786)
