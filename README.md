<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#seriesbr-a-python-:session-package-to-get-brazilian-economic-time-series">1. SeriesBR: A Python package to get brazilian economic time series</a>
<ul>
<li><a href="#sec-1-1">1.1. Introduction</a></li>
<li><a href="#banco-central-do-brasil">1.2. Banco Central do Brasil</a></li>
<li><a href="#instituto-de-pesquisa-econ-mica-aplicada">1.3. Instituto de Pesquisa Econômica Aplicada</a></li>
<li><a href="#sec-1-4">1.4. Metadata information</a></li>
<li><a href="#sec-1-5">1.5. Conclusion</a></li>
</ul>
</li>
</ul>
</div>
</div>

# SeriesBR: A Python package to get brazilian economic time series<a id="seriesbr-a-python :session-package-to-get-brazilian-economic-time-series" name="seriesbr-a-python :session-package-to-get-brazilian-economic-time-series"></a>



## Introduction<a id="sec-1-1" name="sec-1-1"></a>

This package eases the task of getting data from Banco Central do Brasil
(BCB) and Instituto de Pesquisa Econômica Aplicada (Ipea) databases API.

It comes packed with a bunch of functions to interact with these databases API,
such as searching for a series, getting metadata and, most importantly, getting the values
into a `pandas.DataFrame`.

It takes heavy inspiration from the R packages [rbcb](https://github.com/wilsonfreitas/rbcb) and [ipeaData](https://github.com/ipea/ipeaData).

Here I'll demonstrate how it would be used.

## Banco Central do Brasil<a id="banco-central-do-brasil" name="banco-central-do-brasil"></a>


Let's imagine you need to get the brazilian interest rate. You
will need a code for that but you have no idea what it is.

Not a problem, you can search for it like this:

    import pandas as pd
    pd.set_option('display.max_rows', 10)

    from seriesbr import bcb
    
    bcb.search("Selic")

      codigo_sgs periodicidade                            unidade_medida                                              title
    0       1178        diária                         Percentual ao ano          Taxa de juros - Selic anualizada base 252
    1       4390        mensal                         Percentual ao mês             Taxa de juros - Selic acumulada no mês
    2       4189        mensal                         Percentual ao ano  Taxa de juros - Selic acumulada no mês anualiz...
    3       4177        mensal                                Percentual  Dívida mobiliária - Participação por indexador...
    4      10634        mensal  Milhões de unidades monetárias correntes  Dívida mobiliária federal (saldos) - Posição e...
    5                   Mensal                                            Estatísticas dos Sistemas de Liquidação de Tít...
    6                                                                     Negociação de Títulos Federais no Mercado Secu...
    7      10613        mensal                                     Meses  Dívida mobiliária federal - Títulos do Tesouro...
    8      10614        mensal                                     Meses  Dívida mobiliária federal - Títulos do Tesouro...
    9      10618        mensal                                     Meses  Dívida mobiliária federal - Títulos do Tesouro...

The `bcb.search` function takes an arbitrary number of optional arguments.

The API then do its best to give the results accordingly.

    bcb.search("Atividade", "Econômica", "Índice")

      codigo_sgs periodicidade              unidade_medida                                              title
    0      24364        mensal                      Índice  Índice de Atividade Econômica do Banco Central...
    1       7414        mensal                      Índice       Vendas do setor supermercadista (Jan/94=100)
    2      11426        mensal  Variação percentual mensal  Índice nacional de preços ao consumidor - Ampl...
    3      11427        mensal  Variação percentual mensal  Índice nacional de preços ao consumidor - Ampl...
    4      10841        mensal  Variação percentual mensal  Índice de Preços ao Consumidor-Amplo (IPCA) - ...
    5      10842        mensal  Variação percentual mensal  Índice de Preços ao Consumidor-Amplo (IPCA) - ...
    6      11428        mensal  Variação percentual mensal  Índice nacional de preços ao consumidor - Ampl...
    7      10843        mensal  Variação percentual mensal  Índice de Preços ao Consumidor-Amplo (IPCA) - ...
    8      10844        mensal  Variação percentual mensal  Índice de Preços ao Consumidor-Amplo (IPCA) - ...
    9      16122        mensal  Variação percentual mensal  Índice nacional de preços ao consumidor - Ampl...

By default, it only returns the first 10 results. If what you're looking
for isn't there, you can get more results by specifying the `rows`
argument and it will be returned that many results,
starting at line `start` (whose default is value 1).

You can also declare the `start` argument to specify

    bcb.search("Monetária", rows = 20, start = 1)

       codigo_sgs periodicidade                                   unidade_medida                                              title
    0       17633        mensal        Milhares de unidades monetárias correntes  Recolhimentos obrigatórios de instituições fin...
    1        1849        mensal        Milhares de unidades monetárias correntes  Recolhimentos obrigatórios de instituições fin...
    2        1848        mensal        Milhares de unidades monetárias correntes  Recolhimentos obrigatórios de instituições fin...
    3        1850        mensal        Milhares de unidades monetárias correntes  Recolhimentos obrigatórios de instituições fin...
    4        1797        mensal        Milhares de unidades monetárias correntes  Recolhimentos obrigatórios de instituições fin...
    ..        ...           ...                                              ...                                                ...
    15      10813        diária  Taxa unidade monetária corrente/dólar americano  Taxa de câmbio - Livre - Dólar americano (compra)
    16          1        diária  Taxa unidade monetária corrente/dólar americano  Taxa de câmbio - Livre - Dólar americano (vend...
    17      12150        mensal         Milhões de unidades monetárias correntes  Saldos das operações de crédito das instituiçõ...
    18      12106        mensal         Milhões de unidades monetárias correntes  Saldos das operações de crédito das instituiçõ...
    19      17620        mensal        Milhares de unidades monetárias correntes  Insuficiência de direcionamento de crédito - D...
    
    [20 rows x 4 columns]

Ok, so now you know how to find out the desired code.
Let's get the actual values next.

To get just one series, you would simply do:

    bcb.get_series({"Spread": 20786})

                Spread
    date              
    2011-03-01   26.22
    2011-04-01   27.01
    2011-05-01   26.84
    2011-06-01   26.72
    2011-07-01   26.91
    ...            ...
    2019-06-01   31.43
    2019-07-01   31.63
    2019-08-01   31.57
    2019-09-01   30.84
    2019-10-01   30.35
    
    [104 rows x 1 columns]

But, in general, you will want to get multiple series.

The most most convenient way to do that is to pass a dictionary
with keys being names and values being codes.

You can also specify the arguments `start` and `end`, that
corresponds to the initial and final date.

    bcb.get_series({"Spread": 20786, "Selic": 4189, "PIB_Mensal": 4380}, start="2011", end="07-2012")

                Spread  Selic  PIB_Mensal
    date                                 
    2011-01-01     NaN  10.85    333330.5
    2011-02-01     NaN  11.17    335117.5
    2011-03-01   26.22  11.62    348082.9
    2011-04-01   27.01  11.74    349255.0
    2011-05-01   26.84  11.92    366411.2
    ...            ...    ...         ...
    2012-03-01   27.42   9.82    393868.0
    2012-04-01   26.84   9.35    382581.2
    2012-05-01   25.20   8.87    401072.7
    2012-06-01   24.42   8.39    399470.5
    2012-07-01   24.17   8.07    415385.2
    
    [19 rows x 3 columns]

And if you don't mind the columns names:

    bcb.get_series(20786, 4189, 4380)

                20786  4189      4380 
    date                              
    1986-06-01    NaN  18.23       NaN
    1986-07-01    NaN  23.51       NaN
    1986-08-01    NaN  35.55       NaN
    1986-09-01    NaN  39.39       NaN
    1986-10-01    NaN  23.65       NaN
    ...           ...    ...       ...
    2019-07-01  31.63   6.40  619395.2
    2019-08-01  31.57   5.90  603944.8
    2019-09-01  30.84   5.71  566361.6
    2019-10-01  30.35   5.38  613627.6
    2019-11-01    NaN   4.90       NaN
    
    [402 rows x 3 columns]

See this bunch of NaN? You can get rid of them by specifying the join argument, which is passed to the `pandas.concat` function,
as well as any other keyword argument.

    bcb.get_series(20786, 4189, 4380, join="inner")

                20786  4189      4380 
    date                              
    2011-03-01  26.22  11.62  348082.9
    2011-04-01  27.01  11.74  349255.0
    2011-05-01  26.84  11.92  366411.2
    2011-06-01  26.72  12.10  371046.4
    2011-07-01  26.91  12.25  373333.7
    ...           ...    ...       ...
    2019-06-01  31.43   6.40  594163.0
    2019-07-01  31.63   6.40  619395.2
    2019-08-01  31.57   5.90  603944.8
    2019-09-01  30.84   5.71  566361.6
    2019-10-01  30.35   5.38  613627.6
    
    [104 rows x 3 columns]

## Instituto de Pesquisa Econômica Aplicada<a id="instituto-de-pesquisa-econômica-aplicada" name="instituto-de-pesquisa-econômica-aplicada"></a>


Now let's check what we got to interact with IPEA's database.

The `search` function here is more powerful because there are way more filters to play with.

For example, let's filter for series in the macroeconomics database, of monthly
period and percent unit measure. Here, we have to specify which parameter we are referring to.

Under the hood, this functions asks the API to return any result containing a given string in the specified field.

    from seriesbr import ipea
    
    ipea.search(BASNOME="Macroeconômico", PERNOME="Mensal", UNINOME="(p.p.)")

                 SERCODIGO PERNOME UNINOME                                            SERNOME         BASNOME
    0         BM12_CRDSD12  Mensal  (p.p.)  Operações de crédito - recursos direcionados -...  Macroeconômico
    1       BM12_CRDSDPF12  Mensal  (p.p.)  Operações de crédito - recursos direcionados -...  Macroeconômico
    2       BM12_CRDSDPJ12  Mensal  (p.p.)  Operações de crédito - recursos direcionados -...  Macroeconômico
    3         BM12_CRLSD12  Mensal  (p.p.)    Operações de crédito - recursos livres - spread  Macroeconômico
    4       BM12_CRLSDPF12  Mensal  (p.p.)  Operações de crédito - recursos livres - sprea...  Macroeconômico
    ..                 ...     ...     ...                                                ...             ...
    10  VALOR12_GLOBAL2412  Mensal  (p.p.)               Bônus global República (24) - spread  Macroeconômico
    11  VALOR12_GLOBAL2712  Mensal  (p.p.)               Bônus global República (27) - spread  Macroeconômico
    12  VALOR12_GLOBAL4012  Mensal  (p.p.)               Bônus global República (40) - spread  Macroeconômico
    13   VALOR12_GLOBAL912  Mensal  (p.p.)                Bônus global República (9) - spread  Macroeconômico
    14   VALOR12_TJCBOND12  Mensal  (p.p.)                                    C-Bond - spread  Macroeconômico
    
    [15 rows x 5 columns]

Another example:

    ipea.search("Juros", PERNOME="Mensal", UNINOME="(% a.m.)")

                SERCODIGO PERNOME   UNINOME                                            SERNOME
    0   ANBIMA12_TJCDBP12  Mensal  (% a.m.)                     Taxa de juros - CDB pré-fixado
    1       BM12_TJCDBN12  Mensal  (% a.m.)                                Taxa de juros - CDB
    2        BM12_TJCDI12  Mensal  (% a.m.)                         Taxa de juros - CDI / Over
    3       BM12_TJLCMN12  Mensal  (% a.m.)       Taxa de juros - letras de câmbio ao mutuário
    4       BM12_TJLCTN12  Mensal  (% a.m.)        Taxa de juros - letras de câmbio ao tomador
    ..                ...     ...       ...                                                ...
    12       GM12_TJLFT12  Mensal  (% a.m.)  Taxa de juros - Letras do Tesouro Nacional - f...
    13   IBMEC12_OTNRTJ12  Mensal  (% a.m.)  Taxa de juros - obrigações reajustáveis do Tes...
    14    IBMEC12_TJEMP12  Mensal  (% a.m.)  Taxa de juros paga pelo tomador do empréstimo ...
    15     IBMEC12_TJLM12  Mensal  (% a.m.)                Taxa de juros - letras imobiliárias
    16    IBMEC12_TJTIT12  Mensal  (% a.m.)                   Taxa de juros - letras de câmbio
    
    [17 rows x 4 columns]

You would get the series in a similar fashion as with the bcb module:

    ipea.get_series({"Taxa de juros - Over / Selic": "BM12_TJOVER12", "Taxa de juros - CDB": "BM12_TJCDBN12"}, join="inner")

                Taxa de juros - Over / Selic  Taxa de juros - CDB
    date                                                         
    1974-01-01                          1.46             1.800000
    1974-02-01                          1.15             1.800000
    1974-03-01                          1.16             1.800000
    1974-04-01                          1.21             1.800000
    1974-05-01                          1.24             1.800000
    ...                                  ...                  ...
    2009-06-01                          0.76             0.711593
    2009-07-01                          0.79             0.776809
    2009-08-01                          0.69             0.692135
    2009-09-01                          0.69             0.718573
    2009-10-01                          0.69             0.693355
    
    [430 rows x 2 columns]

## Metadata information<a id="sec-1-4" name="sec-1-4"></a>

If you want to get metadata information about a series,
you can do it like in the snippets below, which will give you a dictionary.

    metadados = ipea.get_metadata("BM12_TJOVER12")
    
    metadados["SERCOMENTARIO"]

    'Quadro: Taxas de juros efetivas.  Para 1974-1979: fonte Andima.  Dados mais recentes atualizados pela Sinopse da Andima.  Obs.: A taxa Overnight / Selic é a média dos juros que o Governo paga aos bancos que lhe emprestaram dinheiro. Refere-se à média do mês. Serve de referência para outras taxas de juros do país. A taxa Selic é a taxa básica de juros da economia.'

You'll get a dictionary back.

Similarly for BCB module:

    metadados = bcb.get_metadata(11)
    
    metadados["notes"]

    Taxa de juros que representa a taxa média ajustada das operações compromissadas com prazo de um dia útil lastreadas com títulos públicos federais custodiados no Sistema Especial de Liquidação e de Custódia (Selic). Divulgação em % a.d.
    
    __Para mais informações sobre a série, clique no link abaixo:__
    
    https://www3.bcb.gov.br/sgspub/consultarmetadados/consultarMetadadosSeries.do?method=consultarMetadadosSeriesInternet&hdOidSerieSelecionada=11

## Conclusion<a id="sec-1-5" name="sec-1-5"></a>

For your convenience there is also a module to get
series from both databases in a single call.

You will always get a `pandas.DataFrame` when calling
`get_series`.

This is done so you can do nice things such as plotting
the series immediately after getting them.

    from seriesbr import seriesbr
    
    dados = seriesbr.get_series(
        {
            "spread": 20786,
            "pib_mensal": 4380,
            "igp": "PAN12_IGPDIG12",
            "inadimplência": "BM12_CRLIN12"
        },
        join="inner",
    )

    import matplotlib.pyplot as plt
    
    dados.plot(subplots=True, layout=(2, 2))
    plt.gcf().tight_layout()
    plt.suptitle("Séries do IPEADATA e do BCB")
    plt.subplots_adjust(top=.9)
    plt.savefig('example.png', figsize=(7, 7))
    'example.png'

![img](example.png)

Hope you enjoy the package.

If you find any bugs or if you think something could be better, 
feel free to open an issue / contribute by opening a pull request!