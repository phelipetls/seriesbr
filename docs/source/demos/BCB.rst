Banco Central do Brasil
=======================

Searching
---------

A simple search:

.. code:: python

   import pandas as pd
   pd.set_option('display.max_rows', 10)

   from seriesbr import bcb

   bcb.search("Selic")

::

     codigo_sgs                                                                                                                title periodicidade                            unidade_medida
   0  1178       Taxa de juros - Selic anualizada base 252                                                                            diária        Percentual ao ano                       
   1  4390       Taxa de juros - Selic acumulada no mês                                                                               mensal        Percentual ao mês                       
   2  4189       Taxa de juros - Selic acumulada no mês anualizada base 252                                                           mensal        Percentual ao ano                       
   3  4177       Dívida mobiliária - Participação por indexador - Posição em carteira - Over/Selic                                    mensal        Percentual                              
   4  10634      Dívida mobiliária federal (saldos) - Posição em carteira - Título indexado a Selic - LFT                             mensal        Milhões de unidades monetárias correntes
   5             Estatísticas dos Sistemas de Liquidação de Títulos, Derivativos e Câmbio                                             Mensal                                                
   6             Negociação de Títulos Federais no Mercado Secundário                                                                                                                       
   7  10613      Dívida mobiliária federal - Títulos do Tesouro Nacional - Emitidos em oferta pública - Prazo e duração médios - LTN  mensal        Meses                                   
   8  10614      Dívida mobiliária federal - Títulos do Tesouro Nacional - Emitidos em oferta pública - Prazo médio - LFT             mensal        Meses                                   
   9  10618      Dívida mobiliária federal - Títulos do Tesouro Nacional - Emitidos - Prazo médio - Total                             mensal        Meses                                   

It's also possible to search for multiple strings:

.. code:: python

   bcb.search("Atividade", "Econômica", "Índice")

::

     codigo_sgs                                                                                                                    title periodicidade              unidade_medida
   0  24364      Índice de Atividade Econômica do Banco Central (IBC-Br) - com ajuste sazonal                                             mensal        Índice                    
   1  7414       Vendas do setor supermercadista (Jan/94=100)                                                                             mensal        Índice                    
   2  11426      Índice nacional de preços ao consumidor - Amplo (IPCA) - Núcleo médias aparadas sem suavização                           mensal        Variação percentual mensal
   3  11427      Índice nacional de preços ao consumidor - Amplo (IPCA) - Núcleo por exclusão - Sem monitorados e alimentos no domicílio  mensal        Variação percentual mensal
   4  10841      Índice de Preços ao Consumidor-Amplo (IPCA) - Bens não-duráveis                                                          mensal        Variação percentual mensal
   5  10842      Índice de Preços ao Consumidor-Amplo (IPCA) - Bens semi-duráveis                                                         mensal        Variação percentual mensal
   6  11428      Índice nacional de preços ao consumidor - Amplo (IPCA) - Itens livres                                                    mensal        Variação percentual mensal
   7  10843      Índice de Preços ao Consumidor-Amplo (IPCA) - Duráveis                                                                   mensal        Variação percentual mensal
   8  10844      Índice de Preços ao Consumidor-Amplo (IPCA) - Serviços                                                                   mensal        Variação percentual mensal
   9  16122      Índice nacional de preços ao consumidor - Amplo (IPCA) - Núcleo de dupla ponderação                                      mensal        Variação percentual mensal

You can control how many results will be shown with the argument
``rows`` (defaults to 10), and also from which row it'll start showing
with ``start`` (defaults to 1).

.. code:: python

   bcb.search("Monetária", "mensal", "Milhares", rows=20, start=1)

::

      codigo_sgs                                                                                                     title periodicidade                             unidade_medida
   0   1849       Recolhimentos obrigatórios de instituições financeiras - Recursos à vista em espécie (não remunerados)    mensal        Milhares de unidades monetárias correntes
   1   1848       Recolhimentos obrigatórios de instituições financeiras - Depósitos de poupança em espécie (remunerados)   mensal        Milhares de unidades monetárias correntes
   2   1850       Recolhimentos obrigatórios de instituições financeiras - Depósitos a prazo em espécie (remunerados)       mensal        Milhares de unidades monetárias correntes
   3   1797       Recolhimentos obrigatórios de instituições financeiras - Exigibilidade adicional em espécie (remunerado)  mensal        Milhares de unidades monetárias correntes
   4   17620      Insuficiência de direcionamento de crédito - Depósitos de poupança - Crédito imobiliário (em espécie)     mensal        Milhares de unidades monetárias correntes
   ..    ...                                                                                                        ...        ...                                              ...
   6   17623      Insuficiência de direcionamento de crédito - Depósitos à vista - Microcrédito (em espécie)                mensal        Milhares de unidades monetárias correntes
   7   17622      Insuficiência de direcionamento de crédito - Depósitos à vista - Crédito rural (em espécie)               mensal        Milhares de unidades monetárias correntes
   8   17624      Insuficiência de direcionamento de crédito - Total                                                        mensal        Milhares de unidades monetárias correntes
   9   17625      Outros recolhimentos - Total                                                                              mensal        Milhares de unidades monetárias correntes
   10  1847       Outros recolhimentos de instituições financeiras - Depósitos de poupança em títulos                       mensal        Milhares de unidades monetárias correntes

   [11 rows x 4 columns]

Getting time series
-------------------

.. code:: python

   bcb.get_series(
       {"Spread": 20786, "Selic": 4189, "PIB_Mensal": 4380}, start="2011", end="07-2012"
   )

::

               Spread  Selic  PIB_Mensal
   Date                                 
   2011-01-01 NaN      10.85  333330.6  
   2011-02-01 NaN      11.17  335117.6  
   2011-03-01  26.22   11.62  348082.9  
   2011-04-01  27.01   11.74  349255.0  
   2011-05-01  26.84   11.92  366411.2  
   ...           ...     ...       ...  
   2012-03-01  27.42   9.82   393868.0  
   2012-04-01  26.84   9.35   382581.2  
   2012-05-01  25.20   8.87   401072.6  
   2012-06-01  24.42   8.39   399470.4  
   2012-07-01  24.17   8.07   415385.3  

   [19 rows x 3 columns]

Or, if you don't mind the column names:

.. code:: python

   bcb.get_series(20786, 4189, 4380)

::

               20786   4189      4380
   Date                              
   1986-06-01 NaN     18.23 NaN      
   1986-07-01 NaN     23.51 NaN      
   1986-08-01 NaN     35.55 NaN      
   1986-09-01 NaN     39.39 NaN      
   1986-10-01 NaN     23.65 NaN      
   ...         ..       ...  ..      
   2019-08-01  31.57  5.90   615897.0
   2019-09-01  30.84  5.71   598360.6
   2019-10-01  30.35  5.38   619781.2
   2019-11-01 NaN     4.90   627545.9
   2019-12-01 NaN     4.67  NaN      

   [403 rows x 3 columns]

Keyword arguments will be passed to ``pandas.concat``. If you pass
"inner" to the ``join`` argument the returned ``DataFrame`` won't have
NAs.

.. code:: python

   bcb.get_series(20786, 4189, 4380, join="inner")

::

               20786   4189      4380
   Date                              
   2011-03-01  26.22  11.62  348082.9
   2011-04-01  27.01  11.74  349255.0
   2011-05-01  26.84  11.92  366411.2
   2011-06-01  26.72  12.10  371046.4
   2011-07-01  26.91  12.25  373333.7
   ...           ...    ...       ...
   2019-06-01  31.43  6.40   599143.0
   2019-07-01  31.63  6.40   627852.6
   2019-08-01  31.57  5.90   615897.0
   2019-09-01  30.84  5.71   598360.6
   2019-10-01  30.35  5.38   619781.2

   [104 rows x 3 columns]

Getting metadata
----------------

.. code:: python

   metadados = bcb.get_metadata(11)

   metadados

::

                                                                                                                                                                            values
   referencias                                                                                                                                                                    
   license_title            Licença Aberta para Bases de Dados (ODbL) do Open Data Commons                                                                                        
   maintainer               Banco Central do Brasil/Departamento de Operações do Mercado Aberto                                                                                   
   relationships_as_object  []                                                                                                                                                    
   vcge                     Sistema financeiro [http://vocab.e.gov.br/2011/03/vcge#sistema-financeiro], Economia e Finanças [http://vocab.e.gov.br/2011/03/vcge#economia-financas]
   ...                                                                                                                                                                         ...
   license_url              http://www.opendefinition.org/licenses/odc-odbl                                                                                                       
   frequencia                                                                                                                                                                     
   title                    Taxa de juros - Selic                                                                                                                                 
   revision_id              67db17b5-70d3-4f23-af39-afa50ee1b451                                                                                                                  
   fim_periodo                                                                                                                                                                    

   [43 rows x 1 columns]
