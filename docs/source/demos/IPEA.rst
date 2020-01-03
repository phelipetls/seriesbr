Instituto de Pesquisa Econômica Aplicada
========================================

Searching
---------

You can :py:func:`search <seriesbr.ipea.search>` for a time series by name
with an arbitrary number of arguments:

.. ipython:: python

   import pandas as pd

   pd.set_option('display.expand_frame_repr', False, 'display.max_rows', 10)

   from seriesbr import ipea

   ipea.search("Taxa", "Selic", "recursos", "livres")


And it also accepts keyword arguments to filter by metadata.

For example, if you're looking for a macroeconomic, monthly time series
measured in percent points, you could try:

.. ipython:: python


   ipea.search(BASNOME="Macroeconômico", PERNOME="Mensal", UNINOME="(p.p.)")


Or, if you want american or german GDP that is still updated:

.. ipython:: python

   ipea.search("PIB", PAICODIGO=["DEU", "USA"], SERSTATUS="A")


Here's a list of the valid metadatas accepted by the ``ipea.search``
function:

============== =============================
Code           Description
============== =============================
SERNOME        Name
SERCODIGO      Code
PERNOME        Frequency
TEMCODIGO      Theme's code
UNINOME        Unit of measurement
PAICODIGO      Country's code
SERATUALIZACAO Last update
MULNOME        Multiplicative factor
SERCOMENTARIO  Notes/comments, in portuguese
FNTNOME        Source's name, in portuguese
FNTSIGLA       Source's initials
FNTURL         Source's url
BASNOME        Basis' name
SERSTATUS      Active ('A'), Inactive ('I')
SERNUMERICA    Numeric (1), Alphanumeric (0)
============== =============================

You can take a look at the available themes and countries with
:py:func:`list_themes <seriesbr.ipea.list_themes>` and :py:func:`list_countries <seriesbr.ipea.list_countries>`.

.. ipython:: python

   ipea.list_themes()


Supposing now we are interested in the theme of employment and
macroeconomics, we could search for these themes like this:

.. ipython:: python

   ipea.search(TEMCODIGO=[12, 17])


.. ipython:: python

   ipea.list_countries()


.. ipython:: python

   ipea.search(PAICODIGO="DEU")


Getting time series
-------------------

To get time series values, use :py:func:`seriesbr.ipea.get_series`.

.. ipython:: python

   ipea.get_series({"Taxa de juros - Over / Selic": "BM12_TJOVER12",
                    "Taxa de juros - CDB": "BM12_TJCDBN12"}, join="inner")

You could also filter by date:

.. ipython:: python

   ipea.get_series(
       {"Taxa de juros - Over / Selic": "BM12_TJOVER12"},
       "PAN12_IPCAG12",
       join="inner",
       start="072015",
       end="072016",
   )


Getting metadata
----------------

To get metadata, just call :py:func:`seriesbr.ipea.get_metadata`.

.. ipython:: python

   ipea.get_metadata("BM12_TJOVER12")
