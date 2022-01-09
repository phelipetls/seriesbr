Instituto Brasileiro de Geografia e Estatística
===============================================

Obtendo séries
-------------------

O uso do módulo do IBGE não é tão simples quanto às do BCB e IPEA.

Isso porque uma série temporal para a `API de agregados do IBGE
<https://servicodados.ibge.gov.br/api/docs/agregados?versao=3>`_ é uma variável
que pertence a um agregado (ou tabela), que por sua vez pertence a uma
pesquisa.

Além disso, é possível obter dados por localidade (municípios, estados etc.),
classificações (grupo, por exemplo tipo de produto) e categorias (tipo
específico, por exemplo alimentação), além de filtrar por período.

Por isso, a função :py:func:`seriesbr.ibge.get_series` aceita muito mais
argumentos.

É recomendado usar `a seção de Acervo do site do Sidra
<https://sidra.ibge.gov.br/acervo>`_ para obter os identificadores das tabelas,
localidades, classificações, categorias etc.

Para ilustrar o uso do módulo, vamos reproduzir uma `visualização do IPCA no
site do Sidra <https://sidra.ibge.gov.br/home/ipca/brasil>`_.

O identificador da tabela do IPCA é 7060 e nós vamos querer as variáveis de
variação mensal e acumulada no ano.

.. ipython:: python

   import matplotlib
   import matplotlib.pyplot as plt
   import matplotlib.ticker as ticker

   from seriesbr import ibge

   ipca_by_product = ibge.get_series(
       7060,
       last_n=1,
       classifications={315: [7170, 7445, 7486, 7558, 7625, 7660, 7712, 7766, 7786]},
   )

   ipca_by_product

   date = ipca_by_product.index.unique().strftime("%b/%Y").values[0].title()

   ipca_by_product.pivot_table(
       index="Geral, grupo, subgrupo, item e subitem", columns="Variável", values="Valor"
   ).drop("IPCA - Peso mensal", axis="columns").sort_values(
       "IPCA - Variação acumulada no ano"
   ).plot(
       kind="barh", title="IPCA por Produto / Serviço - " + date, figsize=(10, 8)
   )

   plt.ylabel("");
   plt.tight_layout()
   @savefig ipca_by_product.png
   plt.gca().xaxis.set_major_formatter(ticker.PercentFormatter())

Obtendo metadados
-----------------

Pode ser útil obter metadados sobre uma série específica:

.. ipython:: python

   metadata = ibge.get_metadata(7060)

   metadata.keys()

Por exemplo, pode ser útil para obter os identificadores dos grupos
da classificação "Geral, grupo, subgrupo, item e subitem" do IPCA, que foi a
lista usada no exemplo anterior:

.. ipython:: python

   classification = metadata["classificacoes"][0]

   classification["id"]

   [categoria["id"] for categoria in classification["categorias"] if categoria["nivel"] == 1]
