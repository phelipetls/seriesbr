.. seriesbr documentation master file, created by
   sphinx-quickstart on Sun Dec 15 17:06:03 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SeriesBR
========

|pypi|
|codecov|

**seriesbr** ajuda a consultar, de forma programática, séries temporais dos
bancos de dados do Banco Central do Brasil (BCB), Instituto de Pesquisa
Econômica Aplicada (IPEA) e Instituto Brasileiro de Geografia e Estatística
(IBGE).

Installation
------------

.. code:: bash

   pip3 install seriesbr

Demonstração
------------

.. ipython:: python

   import matplotlib
   import matplotlib.pyplot as plt

   from seriesbr import bcb

   df = bcb.get_series(20786, start="2015", end="2018-06-01")
   df.plot(kind="line", title="Spread bancário no Brasil de 2016 até 01/06/2018")
   df.columns = ["Spread bancário"]
   @savefig spread_bcb.png
   plt.tight_layout()

.. toctree::
   :hidden:
   :maxdepth: 2

   BCB <demos/BCB>
   IPEA <demos/IPEA>
   IBGE <demos/IBGE>

.. toctree::
   :hidden:
   :maxdepth: 1

   Documentation <api/modules>


.. |pypi| image:: https://img.shields.io/pypi/v/seriesbr.svg
   :target: https://pypi.org/project/seriesbr/
.. |codecov| image:: https://codecov.io/gh/phelipetls/seriesbr/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/phelipetls/seriesbr

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
