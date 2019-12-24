Banco Central do Brasil
=======================

Searching
---------

A simple :py:func:`search <seriesbr.bcb.search>`:

.. ipython:: python

   import pandas as pd
   pd.set_option('display.max_rows', 10)

   from seriesbr import bcb

   bcb.search("Selic")


It's also possible to search for multiple strings:

.. ipython:: python

   bcb.search("Atividade", "Econômica", "Índice")


You can also control how many results will be shown with the argument
``rows`` (defaults to 10), and from which row it'll start showing
them with ``start`` (defaults to 1).

.. ipython:: python

   bcb.search("Monetária", "mensal", "Milhares", rows=20, start=1)


Getting time series
-------------------

Now let's get the actual values with :py:func:`seriesbr.bcb.get_series`.

.. ipython:: python

   bcb.get_series(
       {"Spread": 20786, "Selic": 4189, "PIB_Mensal": 4380}, start="2011", end="07-2012"
   )


Or, if you don't mind the column names:

.. ipython:: python

   bcb.get_series(20786, 4189, 4380)


Keyword arguments will be passed to ``pandas.concat``. If you pass
"inner" to the ``join`` argument the returned ``DataFrame`` won't have
NAs.

.. ipython:: python

   bcb.get_series(20786, 4189, 4380, join="inner")


Getting metadata
----------------

And this is how you would get a time series :py:func:`metadata <seriesbr.bcb.get_metadata>`.

.. ipython:: python

   bcb.get_metadata(11)
