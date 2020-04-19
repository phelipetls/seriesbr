Instituto Brasileiro de Geografia e Estatística
===============================================

This module will help you explore IBGE tables.

You will be able to find out which research, variables, locations,
classifications and categories are associated with it, so you can drill it down
to exactly what you need.

For instance, table #7060 is the IPCA table, the brazilian inflation rate, is a
table from the research "Índice Nacional de Preços ao Consumidor Amplo", with
variables such as the monthly variation and cumulative variation over the year
(see :py:func:`seriesbr.ibge.list_variables`). It also has values for specific
municipalities and mesoregions (see :py:func:`seriesbr.ibge.list_locations`).

To learn more about this module, we will now try to replicate `these
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

To get the most recent IPCA, we want table 7060. Table 1419 goes from jan/2012
to dec/2019.

Let's take a look at the available variables with
:py:func:`seriesbr.ibge.list_variables`.

.. ipython:: python

   ibge.list_variables(7060)


We will use all of them eventually.

We will also need the codes of the classifications used by IBGE in its
visualizations. We can use :py:func:`seriesbr.ibge.list_classifications` for
that.

.. ipython:: python

    categories = ibge.list_classifications(7060)

    categories


This let us see the classification id (315) and 457 different categories for
all kinds of products.

We're not interested in much detailed products, so we
will filter for only those whose "level" is 1 or lower.

.. ipython:: python

    products = categories.loc[categories.nivel <= 1]

    products


Apart from those, there are also :py:func:`list_periods
<seriesbr.ibge.list_periods>` and :py:func:`list_locations
<seriesbr.ibge.list_locations>`.


Getting time series
-------------------

Now let's use the information we've gathered to get the actual values with the
function :py:func:`seriesbr.ibge.get_series`.

The table is 7060, we will use every variable so no need to filter those.

Since we have the codes for classifications and categories, we can just pass a
dictionary like this: ``{ classification: [ categories ] }``.

But if you wanted data for a classification with all of its categories, you
could just pass the classification code alone as an int / str, or a list of
them.

.. ipython:: python

   ipca = ibge.get_series(7060, last_n=1, classifications={315: products.id.to_list()})

   ipca


Now let's visualize the inflation rate by product / service.

.. ipython:: python

   # get which month is it
   date = ipca.index.unique().strftime("%b/%Y").values[0].title()

   import matplotlib
   import matplotlib.pyplot as plt
   import matplotlib.ticker as ticker

   ipca.pivot_table(
       index="Geral, grupo, subgrupo, item e subitem", columns="Variável", values="Valor"
   ).drop("IPCA - Peso mensal", axis="columns").sort_values(
       "IPCA - Variação acumulada no ano"
   ).plot(
       kind="barh", title="IPCA por Produto / Serviço - " + date, figsize=(10, 8)
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
       kind="barh", title="Weight of each product in IPCA - " + date
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

If a given location is available for a table, you can assign "all" 
(actually anything that would be evaluated as ``True`` in Python) and it
will return data for every instance of that location, but you could also
pass a list or a single code to select specific locations.

To discover a location code, call the appropriate ``list_*`` function, e.g., to
see which is the code for the state of Rio de Janeiro:

.. ipython:: python

    ibge.list_states(nome="Rio de Janeiro")


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
       title="IPCA por Área Metropolitana - " + date, figsize=(10, 8)
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
       classifications={315: products.id.to_list()},
       start="jun-2018",
       end="jun-2018",
   ).pivot_table(
       index="Geral, grupo, subgrupo, item e subitem", columns="Variável", values="Valor"
   ).drop(
       "IPCA - Peso mensal", axis="columns"
   ).sort_values(
       "IPCA - Variação acumulada em 12 meses"
   ).plot.barh(
       title="IPCA após greve dos caminhoneiros - Jun/2018", figsize=(10, 10)
   ).legend(
       bbox_to_anchor=(1, .5), loc="center left", frameon=False
   )

   plt.ylabel("");
   plt.tight_layout()
   @savefig ipca_truckers_strike.png
   plt.gca().xaxis.set_major_formatter(ticker.PercentFormatter())


Getting metadata
----------------

To :py:func:`get metadata<seriesbr.ibge.get_metadata>` of a time series:

.. ipython:: python

   ibge.get_metadata(7060).head()


.. ipython:: python
   :suppress:

   plt.close('all')
