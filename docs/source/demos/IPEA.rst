Instituto de Pesquisa Econômica Aplicada
========================================

Obtendo séries
-------------------

Seguem alguns exemplos para ilustrar o uso da função
:py:func:`seriesbr.ipea.get_series`.

Obtendo as séries de identificador "BM12_TJOVER12" (Taxa de juros - Over /
Selic - acumulada no mês) e "BM12_PIB12" (PIB):

.. ipython:: python

   from seriesbr import ipea

   ipea.get_series("BM12_TJOVER12", "BM12_PIB12")

Dando nome às colunas:

.. ipython:: python

   ipea.get_series(
       {
           "Selic": "BM12_TJOVER12",
           "PIB": "BM12_PIB12",
       }
   )

Filtrando por data:

.. ipython:: python

   ipea.get_series(
       {
           "Selic": "BM12_TJOVER12",
           "PIB": "BM12_PIB12",
       },
       start="07-2015",
       end="07-2016",
   )
