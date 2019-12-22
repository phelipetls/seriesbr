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

To show how to use the package, we will try to replicate the
visualizations as it was done
`here <https://sidra.ibge.gov.br/home/ipca/brasil>`__, concerning the
most recent IPCA.

Searching
---------

Let's first search for IPCA's code.

.. ipython:: python
   import pandas as pd
   from seriesbr import ibge

   pd.set_option(
       "display.expand_frame_repr", False,
       "display.max_colwidth", -1,
       "display.max_rows", 10,
   )

   ibge.search("Variação mensal, acumulada no ano, acumulada em 12 meses")


You could also search for a specific research in this way:

.. ipython:: python

   ibge.search(pesquisa_nome="Índice Nacional de Preços ao Consumidor Amplo$")


In fact, you can search in a similar way within any column. Also notice
that the string is a regex.

We want the aggregate that goes by the code of 1419. So now let's take a
look at the available variables:

.. ipython:: python

   ibge.list_variables(1419)


We will use all of them eventually, but it is good to know them if you
want a specific one.

Now we need the codes of the same classifications used by in IBGE in its
visualizations. Let's use ``list_classifications``.

Because all ``list_*`` functions takes an arbitrary number of regexes as
arguments to search in column ``nome``, we will search for those which
have a single number followed by a dot, letters and spaces. This means
they're products' groups, not subgroups etc.

.. ipython:: python

   categories = ibge.list_classifications(
       1419,
       "Índice geral",
       "^\d\.[A-z ]+",
   )

   categories

Getting time series
-------------------

Now let's use all this information we've gathered.

The aggregate is 1419, we will use every variable so no need to filter
that.

Since we have the codes for classifications and categories, we can just
pass a dictionary like this: ``{ classification: [ categories ] }``.

But if you wanted data for all values of a classification, you don't
need to give a list of all categories' codes, just pass the
classification code alone as an int / str, or a list of them, and you'll
get all of its categories.

.. ipython:: python

   ipca = ibge.get_series(1419, last_n=1, classifications={315: categories.id.to_list()})

   ipca


Now let's visualize the inflation rate by product / service.

.. ipython:: python


   ipca.pivot_table(
       index="Geral, grupo, subgrupo, item e subitem", columns="Variável", values="Valor"
   )


.. ipython:: python

   import matplotlib
   import matplotlib.pyplot as plt

   matplotlib.style.use('seaborn-muted')

   ipca.pivot_table(
       index="Geral, grupo, subgrupo, item e subitem", columns="Variável", values="Valor"
   ).drop("IPCA - Peso mensal", axis="columns").plot(
       kind="barh", title="IPCA by Procuct", figsize=(10, 8)
   )

   @savefig ipca_by_product.png
   plt.tight_layout()

To see the weight of each product in the inflation rate:

.. ipython:: python


   ipca.pivot_table(
       index="Geral, grupo, subgrupo, item e subitem", columns="Variável", values="Valor"
   ).loc[:, ["IPCA - Peso mensal"]].sort_values("IPCA - Peso mensal").plot(
       kind="barh", title="Weight of each product in IPCA"
   )

   @savefig ipca_weight_by_product.png
   plt.tight_layout()


It would be great if we could plot the inflation rate by metropolitan
area, a mesoregion.

Apart from mesoregions, there are also macroregions (Sul, Sudeste),
microregions (Baixadas, Norte Fluminense etc. in Rio de Janeiro), cities
and states.

If this location is available for an aggregate, you can assign "all" and
it will do return data for every location, but you can pass a list of
codes or a single code to select specific locations.

By default, it will get data for the whole country. If you want data for
other regions and also for Brazil as a whole, you can do the following:

.. ipython:: python

   ipca_by_area = ibge.get_series(1419, mesoregion=True, brazil="yes", last_n=1)

   ipca_by_area


In fact, if you want data for all vales of a given location, just pass
anything that would be evaluated as ``True`` in Python.

.. ipython:: python

   ipca_by_area.pivot_table(
       index="Região Metropolitana e Brasil", columns="Variável", values="Valor"
   ).drop("IPCA - Peso mensal", axis="columns").plot.barh(
       title="IPCA by Mesoregion", figsize=(10, 8)
   )

   @savefig ipca_by_area.png
   plt.tight_layout()

You could, of course, also filter by a specific date. For example, it
would be interested to know the inflation by product soon after the
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
   ).plot.barh(
       title="IPCA after Truckers' strike (June 2018)", figsize=(10, 10)
   )

   @savefig ipca_truckers_strike.png
   plt.tight_layout()

Getting metadata
----------------

.. ipython:: python

   ibge.get_metadata(1419).head()

.. ipython:: python
   :suppress:

   plt.close('all')
