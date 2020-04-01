Instituto Brasileiro de Geografia e Estatística
===============================================

IBGE has a complex database. It is composed of several researches
responsible for measuring a set of aggregates which has several
variables, locations and classifications associated with it.

An aggregate is also commonly referred to as a IBGE table.

Some aggregates may be filtered by locations such as cities, states,
mesoregions, microregions and macroregions, as well by classifications
and categories.

For example, IPCA, the inflation rate, is an aggregate of the research
"Índice Nacional de Preços ao Consumidor Amplo", with variables such as
monthly and cumulative variation. It has values for every Brazil's
location and for various kinds of products.

To show how to use the package, we will try to replicate `these
visualizations <https://sidra.ibge.gov.br/home/ipca/brasil>`__
on the most recent IPCA.

Searching
---------

Let's first :py:func:`search <seriesbr.ibge.search>` for IPCA's code:

.. ipython:: python

   import pandas as pd

   pd.set_option('display.expand_frame_repr', False, 'display.max_colwidth', None, 'display.max_rows', 10)

   from seriesbr import ibge

   ibge.search("Variação mensal, acumulada no ano, acumulada em 12 meses")


You could also search for a specific research (or any other column) in this way:

.. ipython:: python

   ibge.search(pesquisa_nome="Índice Nacional de Preços ao Consumidor Amplo$")


In fact, you can search in a similar way within any column. Also notice
that the string is a regex.

We want the aggregate that goes by the code 7060. So now let's take a
look at the available variables with :py:func:`seriesbr.ibge.list_variables`.

.. ipython:: python

   ibge.list_variables(7060)


We will use all of them eventually, but it is good to know them if you
want a specific one.

Now we need the codes of the same classifications used by IBGE in its
visualizations. We need :py:func:`seriesbr.ibge.list_classifications`
to search for that.

Because all ``list_*`` functions take an arbitrary number of regexes as
arguments to search in column ``nome``, by default, we will search for
those which have a single number followed by a dot, letters or spaces.
This means they're products' major groups, not subgroups etc.

.. ipython:: python

   categories = ibge.list_classifications(
       7060,
       "Índice geral",
       "^\d\.[A-z ]+",
   )

   categories

Apart from those, there are also :py:func:`list_periods <seriesbr.ibge.list_periods>`
and :py:func:`list_locations <seriesbr.ibge.list_locations>`.


Getting time series
-------------------

Now let's use all this information we've gathered and get the actual values
with :py:func:`seriesbr.ibge.get_series`.

The aggregate is 7060, we will use every variable so no need to filter
that.

Since we have the codes for classifications and categories, we can just
pass a dictionary like this: ``{ classification: [ categories ] }``.

But if you wanted data for all values of a classification, you don't
need to give a list of all categories' codes, just pass the
classification code alone as an int / str, or a list of them, and you'll
get all of its categories.

.. ipython:: python

   ipca = ibge.get_series(7060, last_n=1, classifications={315: categories.id.to_list()})

   ipca


Now let's visualize the inflation rate by product / service.

.. ipython:: python

   import matplotlib
   import matplotlib.pyplot as plt
   import matplotlib.ticker as ticker

   ipca.pivot_table(
       index="Geral, grupo, subgrupo, item e subitem", columns="Variável", values="Valor"
   ).drop("IPCA - Peso mensal", axis="columns").sort_values(
       "IPCA - Variação acumulada no ano"
   ).plot(
       kind="barh", title="IPCA por Produto / Serviço", figsize=(10, 8)
   ).legend(
       bbox_to_anchor=(1, 0.5), loc="center left", frameon=False
   )

   plt.ylabel("");
   plt.tight_layout()
   @savefig ipca_by_product.png
   plt.gca().xaxis.set_major_formatter(ticker.PercentFormatter())


To see the weight of each product in the inflation rate:

.. ipython:: python


   ipca.pivot_table(
       index="Geral, grupo, subgrupo, item e subitem", columns="Variável", values="Valor"
   ).loc[:, ["IPCA - Peso mensal"]].sort_values("IPCA - Peso mensal").plot(
       kind="barh", title="Weight of each product in IPCA"
   )

   plt.ylabel("");
   plt.tight_layout()
   @savefig ipca_weight_by_product.png
   plt.gca().xaxis.set_major_formatter(ticker.PercentFormatter())


It would be great if we could plot the inflation rate by metropolitan
area, a mesoregion, like they did.

But apart from mesoregions, there are also macroregions (Sul, Sudeste),
microregions (Baixadas, Norte Fluminense etc. in Rio de Janeiro), municipalities
and states, see the :py:func:`documentation <seriesbr.ibge.get_series>` for details.

.. note::

   Since v0.1.3 arguments for locations are in plural, i.e., macroregions,
   municipalities, microregions, mesoregions and states.

If a given location is available for an aggregate, you can assign "all" 
(actually anything that would be evaluated as ``True`` in Python) and it
will return data for every instance of that location, but you could also
pass a list or a single code to select specific locations.

By default, it will get data for the whole country. If you want data for
other regions and also for Brazil as a whole, you can do the following:

.. ipython:: python

   ipca_by_area = ibge.get_series(7060, mesoregions=True, brazil="yes", last_n=1)

   ipca_by_area


.. ipython:: python

   ipca_by_area.pivot_table(
       index="Região Metropolitana e Brasil", columns="Variável", values="Valor"
   ).drop("IPCA - Peso mensal", axis="columns").sort_values(
       "IPCA - Variação acumulada no ano"
   ).plot.barh(
       title="IPCA por Área Metropolitana", figsize=(10, 8)
   ).legend(
       bbox_to_anchor=(1, 0.5), loc="center left", frameon=False
   )

   plt.ylabel("");
   plt.tight_layout()
   @savefig ipca_by_area.png
   plt.gca().xaxis.set_major_formatter(ticker.PercentFormatter())


You could, of course, also filter by a specific date. For example, it
may be be interesting to know the inflation by product soon after the
Truck Drivers' strike in 2018.

.. ipython:: python

   ibge.get_series(
       1419,
       classifications={315: categories.id.to_list()},
       start="jun-2018",
       end="jun-2018",
   ).pivot_table(
       index="Geral, grupo, subgrupo, item e subitem", columns="Variável", values="Valor"
   ).drop(
       "IPCA - Peso mensal", axis="columns"
   ).sort_values(
       "IPCA - Variação acumulada em 12 meses"
   ).plot.barh(
       title="IPCA após greve dos caminhoneiros (junho/2018)", figsize=(10, 10)
   ).legend(
       bbox_to_anchor=(1, .5), loc="center left", frameon=False
   )

   plt.ylabel("");
   plt.tight_layout()
   @savefig ipca_truckers_strike.png
   plt.gca().xaxis.set_major_formatter(ticker.PercentFormatter())

.. note::

    Notice that the appropriate aggregate no longer is 7060, but 1419.
    This is because, for some reason, the aggregate 1419 ended in 2019.


Getting metadata
----------------

To :py:func:`get metadata<seriesbr.ibge.get_metadata>` of a time series:

.. ipython:: python

   ibge.get_metadata(7060).head()


.. ipython:: python
   :suppress:

   plt.close('all')
