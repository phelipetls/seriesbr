Instituto de Pesquisa Econômica Aplicada
========================================

Obtendo séries
-------------------

Seguem alguns exemplos para ilustrar o uso da função
:py:func:`seriesbr.ipea.get_series`.

Obtendo as séries de identificador "*BM12_TJOVER12*" (Taxa de juros - Over /
Selic - acumulada no mês):

.. ipython:: python

   from seriesbr import ipea

   ipea.get_series("BM12_TJOVER12")

Filtrando por data:

.. ipython:: python

   ipea.get_series("BM12_TJOVER12", start="07-2015", end="07-2016")

Obtendo as últimas 12 observações:

.. ipython:: python

   ipea.get_series("BM12_TJOVER12", last_n=12)


Obtendo metadados
-----------------

Para obter os metadados de uma série:

.. ipython:: python

  ipea.get_metadata("BM12_TJOVER12")

Para entender o que significa cada campo exatamente, consulte a `documentação
do Ipeadata <http://www.ipeadata.gov.br/api/>`_.
