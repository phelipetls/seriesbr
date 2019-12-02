# SeriesBR: A Python package to get brazilian economic time series into a DataFrame

[![Build Status](<https://travis-ci.org/phelipetls/seriesbr.svg?branch=master>)](<https://travis-ci.org/phelipetls/seriesbr>)

<nav id="TOC" role="doc-toc">
<ul>
<li><a href="#seriesbr-a-python-package-to-get-brazilian-economic-time-series-into-a-dataframe">SeriesBR: A Python package to get brazilian economic time series into a DataFrame</a>
<ul>
<li><a href="#introduction">Introduction</a></li>
<li><a href="#installation">Installation</a></li>
<li><a href="#dependencies">Dependencies</a></li>
<li><a href="#main-features">Main Features</a></li>
<li><a href="#banco-central-do-brasil">Banco Central do Brasil</a></li>
<li><a href="#instituto-de-pesquisa-econômica-aplicada">Instituto de Pesquisa Econômica Aplicada</a></li>
<li><a href="#bcb-ipea">BCB + IPEA</a></li>
<li><a href="#instituto-brasileiro-de-geografia-e-estatística">Instituto Brasileiro de Geografia e Estatística</a></li>
<li><a href="#conclusion">Conclusion</a></li>
<li><a href="#license">License</a></li>
<li><a href="#support">Support</a></li>
</ul></li>
</ul>
</nav>


## Introduction

This package eases the task of getting data from Banco Central do Brasil
(BCB), Instituto de Pesquisa Econômica Aplicada (Ipea) and Instituto 
Brasileiro de Geografia e Estatística (IBGE) databases.

It has several functions to interact with these databases,
such as searching for a series by name or another criteria,
retrieving metadata and, most importantly,
getting the series values into a \`pandas.DataFrame\`.

It is heavily inspired by the R packages [rbcb](https://github.com/wilsonfreitas/rbcb), [ipeaData](https://github.com/ipea/ipeaData) and [sidrar](https://github.com/cran/sidrar).

## Installation

`pip3 install seriesbr`

## Dependencies

-   requests
-   pandas

## Main Features

-   Get multiple time series with `get_series`.
-   Search in a given database with `search`.
-   Get metadata with `get_metadata`.

## Banco Central do Brasil

Let's imagine you need to get the brazilian interest rate. You
will need a code for that but you have no idea what it is.

Not a problem, you can search for it like this:


```python
import pandas as pd
pd.set_option('display.max_rows', 10)

from seriesbr import bcb

bcb.search("Selic")
```




<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>codigo_sgs</th>
      <th>title</th>
      <th>periodicidade</th>
      <th>unidade_medida</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1178</td>
      <td>Taxa de juros - Selic anualizada base 252</td>
      <td>diária</td>
      <td>Percentual ao ano</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4390</td>
      <td>Taxa de juros - Selic acumulada no mês</td>
      <td>mensal</td>
      <td>Percentual ao mês</td>
    </tr>
    <tr>
      <th>2</th>
      <td>4189</td>
      <td>Taxa de juros - Selic acumulada no mês anualiz...</td>
      <td>mensal</td>
      <td>Percentual ao ano</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4177</td>
      <td>Dívida mobiliária - Participação por indexador...</td>
      <td>mensal</td>
      <td>Percentual</td>
    </tr>
    <tr>
      <th>4</th>
      <td>10634</td>
      <td>Dívida mobiliária federal (saldos) - Posição e...</td>
      <td>mensal</td>
      <td>Milhões de unidades monetárias correntes</td>
    </tr>
    <tr>
      <th>5</th>
      <td></td>
      <td>Estatísticas dos Sistemas de Liquidação de Tít...</td>
      <td>Mensal</td>
      <td></td>
    </tr>
    <tr>
      <th>6</th>
      <td></td>
      <td>Negociação de Títulos Federais no Mercado Secu...</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>7</th>
      <td>10613</td>
      <td>Dívida mobiliária federal - Títulos do Tesouro...</td>
      <td>mensal</td>
      <td>Meses</td>
    </tr>
    <tr>
      <th>8</th>
      <td>10614</td>
      <td>Dívida mobiliária federal - Títulos do Tesouro...</td>
      <td>mensal</td>
      <td>Meses</td>
    </tr>
    <tr>
      <th>9</th>
      <td>10618</td>
      <td>Dívida mobiliária federal - Títulos do Tesouro...</td>
      <td>mensal</td>
      <td>Meses</td>
    </tr>
  </tbody>
</table>
</div>



The `bcb.search` function takes an arbitrary number of optional arguments.

The API then do its best to give the results accordingly.


```python
bcb.search("Atividade", "Econômica", "Índice")
```




<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>codigo_sgs</th>
      <th>title</th>
      <th>periodicidade</th>
      <th>unidade_medida</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>24364</td>
      <td>Índice de Atividade Econômica do Banco Central...</td>
      <td>mensal</td>
      <td>Índice</td>
    </tr>
    <tr>
      <th>1</th>
      <td>7414</td>
      <td>Vendas do setor supermercadista (Jan/94=100)</td>
      <td>mensal</td>
      <td>Índice</td>
    </tr>
    <tr>
      <th>2</th>
      <td>11426</td>
      <td>Índice nacional de preços ao consumidor - Ampl...</td>
      <td>mensal</td>
      <td>Variação percentual mensal</td>
    </tr>
    <tr>
      <th>3</th>
      <td>11427</td>
      <td>Índice nacional de preços ao consumidor - Ampl...</td>
      <td>mensal</td>
      <td>Variação percentual mensal</td>
    </tr>
    <tr>
      <th>4</th>
      <td>10841</td>
      <td>Índice de Preços ao Consumidor-Amplo (IPCA) - ...</td>
      <td>mensal</td>
      <td>Variação percentual mensal</td>
    </tr>
    <tr>
      <th>5</th>
      <td>10842</td>
      <td>Índice de Preços ao Consumidor-Amplo (IPCA) - ...</td>
      <td>mensal</td>
      <td>Variação percentual mensal</td>
    </tr>
    <tr>
      <th>6</th>
      <td>11428</td>
      <td>Índice nacional de preços ao consumidor - Ampl...</td>
      <td>mensal</td>
      <td>Variação percentual mensal</td>
    </tr>
    <tr>
      <th>7</th>
      <td>10843</td>
      <td>Índice de Preços ao Consumidor-Amplo (IPCA) - ...</td>
      <td>mensal</td>
      <td>Variação percentual mensal</td>
    </tr>
    <tr>
      <th>8</th>
      <td>10844</td>
      <td>Índice de Preços ao Consumidor-Amplo (IPCA) - ...</td>
      <td>mensal</td>
      <td>Variação percentual mensal</td>
    </tr>
    <tr>
      <th>9</th>
      <td>16122</td>
      <td>Índice nacional de preços ao consumidor - Ampl...</td>
      <td>mensal</td>
      <td>Variação percentual mensal</td>
    </tr>
  </tbody>
</table>
</div>



By default, it only returns the first 10 results.
If you didn't find what you're looking for,
you can specify the number of returned results with `rows`
and how many results to skip with `skip`.


```python
bcb.search("Monetária", rows=20, skip=1)
```




<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>codigo_sgs</th>
      <th>title</th>
      <th>periodicidade</th>
      <th>unidade_medida</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>17633</td>
      <td>Recolhimentos obrigatórios de instituições fin...</td>
      <td>mensal</td>
      <td>Milhares de unidades monetárias correntes</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1849</td>
      <td>Recolhimentos obrigatórios de instituições fin...</td>
      <td>mensal</td>
      <td>Milhares de unidades monetárias correntes</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1848</td>
      <td>Recolhimentos obrigatórios de instituições fin...</td>
      <td>mensal</td>
      <td>Milhares de unidades monetárias correntes</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1850</td>
      <td>Recolhimentos obrigatórios de instituições fin...</td>
      <td>mensal</td>
      <td>Milhares de unidades monetárias correntes</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1797</td>
      <td>Recolhimentos obrigatórios de instituições fin...</td>
      <td>mensal</td>
      <td>Milhares de unidades monetárias correntes</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>15</th>
      <td>10813</td>
      <td>Taxa de câmbio - Livre - Dólar americano (compra)</td>
      <td>diária</td>
      <td>Taxa unidade monetária corrente/dólar americano</td>
    </tr>
    <tr>
      <th>16</th>
      <td>1</td>
      <td>Taxa de câmbio - Livre - Dólar americano (vend...</td>
      <td>diária</td>
      <td>Taxa unidade monetária corrente/dólar americano</td>
    </tr>
    <tr>
      <th>17</th>
      <td>12150</td>
      <td>Saldos das operações de crédito das instituiçõ...</td>
      <td>mensal</td>
      <td>Milhões de unidades monetárias correntes</td>
    </tr>
    <tr>
      <th>18</th>
      <td>12106</td>
      <td>Saldos das operações de crédito das instituiçõ...</td>
      <td>mensal</td>
      <td>Milhões de unidades monetárias correntes</td>
    </tr>
    <tr>
      <th>19</th>
      <td>17620</td>
      <td>Insuficiência de direcionamento de crédito - D...</td>
      <td>mensal</td>
      <td>Milhares de unidades monetárias correntes</td>
    </tr>
  </tbody>
</table>
<p>20 rows × 4 columns</p>
</div>



Ok, so now you know how to find out the desired code.
Let's get the actual values.

To get just one series, you would simply do:


```python
bcb.get_series({"Spread": 20786}) # or just 20786
```




<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Spread</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2011-03-01</th>
      <td>26.22</td>
    </tr>
    <tr>
      <th>2011-04-01</th>
      <td>27.01</td>
    </tr>
    <tr>
      <th>2011-05-01</th>
      <td>26.84</td>
    </tr>
    <tr>
      <th>2011-06-01</th>
      <td>26.72</td>
    </tr>
    <tr>
      <th>2011-07-01</th>
      <td>26.91</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
    </tr>
    <tr>
      <th>2019-06-01</th>
      <td>31.43</td>
    </tr>
    <tr>
      <th>2019-07-01</th>
      <td>31.63</td>
    </tr>
    <tr>
      <th>2019-08-01</th>
      <td>31.57</td>
    </tr>
    <tr>
      <th>2019-09-01</th>
      <td>30.84</td>
    </tr>
    <tr>
      <th>2019-10-01</th>
      <td>30.35</td>
    </tr>
  </tbody>
</table>
<p>104 rows × 1 columns</p>
</div>



But, in general, you will want to get multiple series.

The most convenient way to do that is to pass a dictionary
with keys being names and values being codes.

You can optionally specify the arguments `start` and `end` for the
initial and final date,  or `last_n` to get
just the last n observations.


```python
bcb.get_series({"Spread": 20786, "Selic": 4189, "PIB_Mensal": 4380}, start="2011", end="07-2012")
```




<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Spread</th>
      <th>Selic</th>
      <th>PIB_Mensal</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2011-01-01</th>
      <td>NaN</td>
      <td>10.85</td>
      <td>333330.5</td>
    </tr>
    <tr>
      <th>2011-02-01</th>
      <td>NaN</td>
      <td>11.17</td>
      <td>335117.5</td>
    </tr>
    <tr>
      <th>2011-03-01</th>
      <td>26.22</td>
      <td>11.62</td>
      <td>348082.9</td>
    </tr>
    <tr>
      <th>2011-04-01</th>
      <td>27.01</td>
      <td>11.74</td>
      <td>349255.0</td>
    </tr>
    <tr>
      <th>2011-05-01</th>
      <td>26.84</td>
      <td>11.92</td>
      <td>366411.2</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2012-03-01</th>
      <td>27.42</td>
      <td>9.82</td>
      <td>393868.0</td>
    </tr>
    <tr>
      <th>2012-04-01</th>
      <td>26.84</td>
      <td>9.35</td>
      <td>382581.2</td>
    </tr>
    <tr>
      <th>2012-05-01</th>
      <td>25.20</td>
      <td>8.87</td>
      <td>401072.7</td>
    </tr>
    <tr>
      <th>2012-06-01</th>
      <td>24.42</td>
      <td>8.39</td>
      <td>399470.5</td>
    </tr>
    <tr>
      <th>2012-07-01</th>
      <td>24.17</td>
      <td>8.07</td>
      <td>415385.2</td>
    </tr>
  </tbody>
</table>
<p>19 rows × 3 columns</p>
</div>



If you don't mind the columns names, you can just feed it with the numbers.


```python
bcb.get_series(20786, 4189, 4380)
```




<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>20786</th>
      <th>4189</th>
      <th>4380</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1986-06-01</th>
      <td>NaN</td>
      <td>18.23</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1986-07-01</th>
      <td>NaN</td>
      <td>23.51</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1986-08-01</th>
      <td>NaN</td>
      <td>35.55</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1986-09-01</th>
      <td>NaN</td>
      <td>39.39</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1986-10-01</th>
      <td>NaN</td>
      <td>23.65</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2019-07-01</th>
      <td>31.63</td>
      <td>6.40</td>
      <td>619395.2</td>
    </tr>
    <tr>
      <th>2019-08-01</th>
      <td>31.57</td>
      <td>5.90</td>
      <td>603944.8</td>
    </tr>
    <tr>
      <th>2019-09-01</th>
      <td>30.84</td>
      <td>5.71</td>
      <td>566361.6</td>
    </tr>
    <tr>
      <th>2019-10-01</th>
      <td>30.35</td>
      <td>5.38</td>
      <td>613627.6</td>
    </tr>
    <tr>
      <th>2019-11-01</th>
      <td>NaN</td>
      <td>4.90</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>402 rows × 3 columns</p>
</div>



You can get rid of the NaN's with the argument `join`,
which is passed to the [`pandas.concat`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.concat.html) function,
as well as any other keyword argument.

The default value for `join` is "outer". So, if you pass "inner":


```python
bcb.get_series(20786, 4189, 4380, join="inner")
```




<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>20786</th>
      <th>4189</th>
      <th>4380</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2011-03-01</th>
      <td>26.22</td>
      <td>11.62</td>
      <td>348082.9</td>
    </tr>
    <tr>
      <th>2011-04-01</th>
      <td>27.01</td>
      <td>11.74</td>
      <td>349255.0</td>
    </tr>
    <tr>
      <th>2011-05-01</th>
      <td>26.84</td>
      <td>11.92</td>
      <td>366411.2</td>
    </tr>
    <tr>
      <th>2011-06-01</th>
      <td>26.72</td>
      <td>12.10</td>
      <td>371046.4</td>
    </tr>
    <tr>
      <th>2011-07-01</th>
      <td>26.91</td>
      <td>12.25</td>
      <td>373333.7</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2019-06-01</th>
      <td>31.43</td>
      <td>6.40</td>
      <td>594163.0</td>
    </tr>
    <tr>
      <th>2019-07-01</th>
      <td>31.63</td>
      <td>6.40</td>
      <td>619395.2</td>
    </tr>
    <tr>
      <th>2019-08-01</th>
      <td>31.57</td>
      <td>5.90</td>
      <td>603944.8</td>
    </tr>
    <tr>
      <th>2019-09-01</th>
      <td>30.84</td>
      <td>5.71</td>
      <td>566361.6</td>
    </tr>
    <tr>
      <th>2019-10-01</th>
      <td>30.35</td>
      <td>5.38</td>
      <td>613627.6</td>
    </tr>
  </tbody>
</table>
<p>104 rows × 3 columns</p>
</div>



Or, of course, you can just call `dropna()` afterwards.

If you want more information about a given series, you can call `get_metadata`
and you will get a dictionary with the results.


```python
metadados = bcb.get_metadata(11)

metadados["notes"]
```




    'Taxa de juros que representa a taxa média ajustada das operações compromissadas com prazo de um dia útil lastreadas com títulos públicos federais custodiados no Sistema Especial de Liquidação e de Custódia (Selic). Divulgação em % a.d.\r\n\r\n__Para mais informações sobre a série, clique no link abaixo:__\r\n\r\nhttps://www3.bcb.gov.br/sgspub/consultarmetadados/consultarMetadadosSeries.do?method=consultarMetadadosSeriesInternet&hdOidSerieSelecionada=11'



## Instituto de Pesquisa Econômica Aplicada

Now let's check what we can do with the IPEA's database.

The `search` function here is more powerful because there are way more filters to play with.

For example, let's filter for a monthly macroeconomic time series with units in percent points.
Here, we have to specify which parameter we are referring to.

Under the hood, this functions asks the API to return any result
containing a given string in the specified field.


```python
from seriesbr import ipea

ipea.search(BASNOME="Macroeconômico", PERNOME="Mensal", UNINOME="(p.p.)")
```




<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>SERCODIGO</th>
      <th>SERNOME</th>
      <th>PERNOME</th>
      <th>UNINOME</th>
      <th>BASNOME</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BM12_CRDSD12</td>
      <td>Operações de crédito - recursos direcionados -...</td>
      <td>Mensal</td>
      <td>(p.p.)</td>
      <td>Macroeconômico</td>
    </tr>
    <tr>
      <th>1</th>
      <td>BM12_CRDSDPF12</td>
      <td>Operações de crédito - recursos direcionados -...</td>
      <td>Mensal</td>
      <td>(p.p.)</td>
      <td>Macroeconômico</td>
    </tr>
    <tr>
      <th>2</th>
      <td>BM12_CRDSDPJ12</td>
      <td>Operações de crédito - recursos direcionados -...</td>
      <td>Mensal</td>
      <td>(p.p.)</td>
      <td>Macroeconômico</td>
    </tr>
    <tr>
      <th>3</th>
      <td>BM12_CRLSD12</td>
      <td>Operações de crédito - recursos livres - spread</td>
      <td>Mensal</td>
      <td>(p.p.)</td>
      <td>Macroeconômico</td>
    </tr>
    <tr>
      <th>4</th>
      <td>BM12_CRLSDPF12</td>
      <td>Operações de crédito - recursos livres - sprea...</td>
      <td>Mensal</td>
      <td>(p.p.)</td>
      <td>Macroeconômico</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>10</th>
      <td>VALOR12_GLOBAL2412</td>
      <td>Bônus global República (24) - spread</td>
      <td>Mensal</td>
      <td>(p.p.)</td>
      <td>Macroeconômico</td>
    </tr>
    <tr>
      <th>11</th>
      <td>VALOR12_GLOBAL2712</td>
      <td>Bônus global República (27) - spread</td>
      <td>Mensal</td>
      <td>(p.p.)</td>
      <td>Macroeconômico</td>
    </tr>
    <tr>
      <th>12</th>
      <td>VALOR12_GLOBAL4012</td>
      <td>Bônus global República (40) - spread</td>
      <td>Mensal</td>
      <td>(p.p.)</td>
      <td>Macroeconômico</td>
    </tr>
    <tr>
      <th>13</th>
      <td>VALOR12_GLOBAL912</td>
      <td>Bônus global República (9) - spread</td>
      <td>Mensal</td>
      <td>(p.p.)</td>
      <td>Macroeconômico</td>
    </tr>
    <tr>
      <th>14</th>
      <td>VALOR12_TJCBOND12</td>
      <td>C-Bond - spread</td>
      <td>Mensal</td>
      <td>(p.p.)</td>
      <td>Macroeconômico</td>
    </tr>
  </tbody>
</table>
<p>15 rows × 5 columns</p>
</div>



Another example:


```python
ipea.search("Juros", PERNOME="Mensal", UNINOME="(% a.m.)")
```




<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>SERCODIGO</th>
      <th>SERNOME</th>
      <th>PERNOME</th>
      <th>UNINOME</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ANBIMA12_TJCDBP12</td>
      <td>Taxa de juros - CDB pré-fixado</td>
      <td>Mensal</td>
      <td>(% a.m.)</td>
    </tr>
    <tr>
      <th>1</th>
      <td>BM12_TJCDBN12</td>
      <td>Taxa de juros - CDB</td>
      <td>Mensal</td>
      <td>(% a.m.)</td>
    </tr>
    <tr>
      <th>2</th>
      <td>BM12_TJCDI12</td>
      <td>Taxa de juros - CDI / Over</td>
      <td>Mensal</td>
      <td>(% a.m.)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>BM12_TJLCMN12</td>
      <td>Taxa de juros - letras de câmbio ao mutuário</td>
      <td>Mensal</td>
      <td>(% a.m.)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>BM12_TJLCTN12</td>
      <td>Taxa de juros - letras de câmbio ao tomador</td>
      <td>Mensal</td>
      <td>(% a.m.)</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>12</th>
      <td>GM12_TJLFT12</td>
      <td>Taxa de juros - Letras do Tesouro Nacional - f...</td>
      <td>Mensal</td>
      <td>(% a.m.)</td>
    </tr>
    <tr>
      <th>13</th>
      <td>IBMEC12_OTNRTJ12</td>
      <td>Taxa de juros - obrigações reajustáveis do Tes...</td>
      <td>Mensal</td>
      <td>(% a.m.)</td>
    </tr>
    <tr>
      <th>14</th>
      <td>IBMEC12_TJEMP12</td>
      <td>Taxa de juros paga pelo tomador do empréstimo ...</td>
      <td>Mensal</td>
      <td>(% a.m.)</td>
    </tr>
    <tr>
      <th>15</th>
      <td>IBMEC12_TJLM12</td>
      <td>Taxa de juros - letras imobiliárias</td>
      <td>Mensal</td>
      <td>(% a.m.)</td>
    </tr>
    <tr>
      <th>16</th>
      <td>IBMEC12_TJTIT12</td>
      <td>Taxa de juros - letras de câmbio</td>
      <td>Mensal</td>
      <td>(% a.m.)</td>
    </tr>
  </tbody>
</table>
<p>17 rows × 4 columns</p>
</div>



If you want to filter by theme ("TEMNOME") or by country ("PAINOME"), take a look at what is in
the database with `list_theme` and `list_countries`.

You could then get the series in the very same way:


```python
ipea.get_series({"Taxa de juros - Over / Selic": "BM12_TJOVER12", "Taxa de juros - CDB": "BM12_TJCDBN12"}, join="inner")
```




<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Taxa de juros - Over / Selic</th>
      <th>Taxa de juros - CDB</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1974-01-01</th>
      <td>1.46</td>
      <td>1.800000</td>
    </tr>
    <tr>
      <th>1974-02-01</th>
      <td>1.15</td>
      <td>1.800000</td>
    </tr>
    <tr>
      <th>1974-03-01</th>
      <td>1.16</td>
      <td>1.800000</td>
    </tr>
    <tr>
      <th>1974-04-01</th>
      <td>1.21</td>
      <td>1.800000</td>
    </tr>
    <tr>
      <th>1974-05-01</th>
      <td>1.24</td>
      <td>1.800000</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2009-06-01</th>
      <td>0.76</td>
      <td>0.711593</td>
    </tr>
    <tr>
      <th>2009-07-01</th>
      <td>0.79</td>
      <td>0.776809</td>
    </tr>
    <tr>
      <th>2009-08-01</th>
      <td>0.69</td>
      <td>0.692135</td>
    </tr>
    <tr>
      <th>2009-09-01</th>
      <td>0.69</td>
      <td>0.718573</td>
    </tr>
    <tr>
      <th>2009-10-01</th>
      <td>0.69</td>
      <td>0.693355</td>
    </tr>
  </tbody>
</table>
<p>430 rows × 2 columns</p>
</div>



To get metadata you would do the same as in `bcb` module.


```python
metadados = ipea.get_metadata("BM12_TJOVER12")

metadados["SERCOMENTARIO"]
```




    'Quadro: Taxas de juros efetivas.  Para 1974-1979: fonte Andima.  Dados mais recentes atualizados pela Sinopse da Andima.  Obs.: A taxa Overnight / Selic é a média dos juros que o Governo paga aos bancos que lhe emprestaram dinheiro. Refere-se à média do mês. Serve de referência para outras taxas de juros do país. A taxa Selic é a taxa básica de juros da economia.'



## BCB + IPEA

For your convenience there is also a module to get
series from both databases in a single call.

You will always get a `pandas.DataFrame` when calling
`get_series` in every module.

You don't have to worry about converting dates because the index
is already of type `datetime64[ns]` sou you can immediately enjoy
pandas functionalities regarding dates, such as slicing and plotting.


```python
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
```


```python
%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib

matplotlib.style.use('seaborn-deep')

dados.plot(subplots=True, layout=(2, 2), figsize=(10, 5))
plt.gcf().tight_layout()
plt.suptitle("Séries do IPEADATA e do BCB")
plt.subplots_adjust(top=.9)
```


![png](README_files/README_29_0.png)


## Instituto Brasileiro de Geografia e Estatística

IBGE has a very complex database, which allows you to get values for
very specific things. For example, some variables may have different
values for specific locations or categories.

Regarding locations, it could be a city, a state, a macroregion (Sul,
Sudeste), a microregion (for example, Lagos in Rio de Janeiro) or even a
mesoregion (e.g., Baixadas or Região Metropolitana in Rio).

The variables may also have different categories. For example, the IPCA
(Índice de Preços ao Consumidor Amplo) has values for very specific
products or kinds of products.

If you want such a detailed information, this package may be of help. It
has functions to help you get the codes for all of those things so you
can just pass them to the `get_series` later on.

To get a list of the locations, you can try `list_macroregions`, `list_states`,
 `list_cities`, `list_mesoregion` and `list_microregion`.

To search for an aggregated variable code, you would use `list_aggregates`.
To see which variables are associated with an aggregate, you'd use `list_variables`.

All list functions accepts two optional arguments `search` and
`where`, which is just a convenient way to search for a regex in a
given column ("nome" by default).

Also, you can get the metadata of a given aggregate with `get_metadata` function, which
will print a lot of text to the screen depending on the complexity of the aggregate.

To demonstrate how these come together in a typical workflow, let's recreate the first
chart in this [page](https://sidra.ibge.gov.br/home/ipca), a bar plot of the IPCA in October 2019 by products' category.

The aggregate used was "IPCA - Variação mensal, acumulada no ano e acumulada em 12 meses (%)",
let's search for its code.


```python
pd.set_option('max_colwidth', 200)

from seriesbr import ibge

ibge.list_aggregates("IPCA - Variação mensal, acumulada")
```

<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>nome</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2243</th>
      <td>2938</td>
      <td>IPCA - Variação mensal, acumulada no ano e peso mensal, para o índice geral, grupos, subgrupos, itens e subitens de produtos e serviços (de julho/2006 até dezembro/2011)</td>
    </tr>
    <tr>
      <th>2244</th>
      <td>1419</td>
      <td>IPCA - Variação mensal, acumulada no ano, acumulada em 12 meses e peso mensal, para o índice geral, grupos, subgrupos, itens e subitens de produtos e serviços (a partir de janeiro/2012)</td>
    </tr>
  </tbody>
</table>
</div>



After some reading, we will conclude that the code we need is 1419.

Let's see the variables of this aggregate.


```python
ibge.list_variables(1419)
```


<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>variavel</th>
      <th>unidade</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>63</td>
      <td>IPCA - Variação mensal</td>
      <td>%</td>
    </tr>
    <tr>
      <th>1</th>
      <td>69</td>
      <td>IPCA - Variação acumulada no ano</td>
      <td>%</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2265</td>
      <td>IPCA - Variação acumulada em 12 meses</td>
      <td>%</td>
    </tr>
    <tr>
      <th>3</th>
      <td>66</td>
      <td>IPCA - Peso mensal</td>
      <td>%</td>
    </tr>
  </tbody>
</table>
</div>

In the IBGE's chart, they used all of them except for IPCA - Peso mensal.
So, we will need to remember the codes 63, 69 and 66.

Now we need the code for the products categories,
which is a specific classification of this variable.
Let's use `list_classifications`.

I'll use a regex to get the exact categories used in the chart.
This isn't pretty, really, but does work.


```python

regex = "^\d\.(.ndice geral|Alimenta..o e bebidas|Habita.ao|Artigos de resid.ncia|Vestu.rio|Transportes|Sa.de e cuidados pessoais|Despesas pessoais|Educa..o|Comunica..o)$"

df = ibge.list_classifications(1419, regex)

df
```

    /home/linuxbrew/.linuxbrew/opt/python/lib/python3.7/site-packages/pandas/core/strings.py:1843: UserWarning: This pattern has match groups. To actually get the groups, use str.extract.
      return func(self, *args, **kwargs)





<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>nome</th>
      <th>unidade</th>
      <th>nivel</th>
      <th>classificacao_id</th>
      <th>classificacao_nome</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>7170</td>
      <td>1.Alimentação e bebidas</td>
      <td>None</td>
      <td>-1</td>
      <td>315</td>
      <td>Geral, grupo, subgrupo, item e subitem</td>
    </tr>
    <tr>
      <th>227</th>
      <td>7486</td>
      <td>3.Artigos de residência</td>
      <td>None</td>
      <td>-1</td>
      <td>315</td>
      <td>Geral, grupo, subgrupo, item e subitem</td>
    </tr>
    <tr>
      <th>270</th>
      <td>7558</td>
      <td>4.Vestuário</td>
      <td>None</td>
      <td>-1</td>
      <td>315</td>
      <td>Geral, grupo, subgrupo, item e subitem</td>
    </tr>
    <tr>
      <th>315</th>
      <td>7625</td>
      <td>5.Transportes</td>
      <td>None</td>
      <td>-1</td>
      <td>315</td>
      <td>Geral, grupo, subgrupo, item e subitem</td>
    </tr>
    <tr>
      <th>348</th>
      <td>7660</td>
      <td>6.Saúde e cuidados pessoais</td>
      <td>None</td>
      <td>-1</td>
      <td>315</td>
      <td>Geral, grupo, subgrupo, item e subitem</td>
    </tr>
    <tr>
      <th>395</th>
      <td>7712</td>
      <td>7.Despesas pessoais</td>
      <td>None</td>
      <td>-1</td>
      <td>315</td>
      <td>Geral, grupo, subgrupo, item e subitem</td>
    </tr>
    <tr>
      <th>428</th>
      <td>7766</td>
      <td>8.Educação</td>
      <td>None</td>
      <td>-1</td>
      <td>315</td>
      <td>Geral, grupo, subgrupo, item e subitem</td>
    </tr>
    <tr>
      <th>453</th>
      <td>7786</td>
      <td>9.Comunicação</td>
      <td>None</td>
      <td>-1</td>
      <td>315</td>
      <td>Geral, grupo, subgrupo, item e subitem</td>
    </tr>
  </tbody>
</table>
</div>



So, now  we have all that we need. Let's get the data first, we will `get_series` as usual.


```python
ids = df.id.to_list()

ipca = ibge.get_series(1419, variables=[63, 69, 2265], classifications={315: ids})

ipca
```




<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Nível Territorial</th>
      <th>Brasil</th>
      <th>Mês</th>
      <th>Variável</th>
      <th>Geral, grupo, subgrupo, item e subitem</th>
      <th>Unidade de Medida</th>
      <th>Valor</th>
    </tr>
    <tr>
      <th>Data</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2012-01-01</th>
      <td>Brasil</td>
      <td>Brasil</td>
      <td>janeiro 2012</td>
      <td>IPCA - Variação mensal</td>
      <td>1.Alimentação e bebidas</td>
      <td>%</td>
      <td>0.86</td>
    </tr>
    <tr>
      <th>2012-01-01</th>
      <td>Brasil</td>
      <td>Brasil</td>
      <td>janeiro 2012</td>
      <td>IPCA - Variação mensal</td>
      <td>3.Artigos de residência</td>
      <td>%</td>
      <td>0.16</td>
    </tr>
    <tr>
      <th>2012-01-01</th>
      <td>Brasil</td>
      <td>Brasil</td>
      <td>janeiro 2012</td>
      <td>IPCA - Variação mensal</td>
      <td>4.Vestuário</td>
      <td>%</td>
      <td>0.07</td>
    </tr>
    <tr>
      <th>2012-01-01</th>
      <td>Brasil</td>
      <td>Brasil</td>
      <td>janeiro 2012</td>
      <td>IPCA - Variação mensal</td>
      <td>5.Transportes</td>
      <td>%</td>
      <td>0.69</td>
    </tr>
    <tr>
      <th>2012-01-01</th>
      <td>Brasil</td>
      <td>Brasil</td>
      <td>janeiro 2012</td>
      <td>IPCA - Variação mensal</td>
      <td>6.Saúde e cuidados pessoais</td>
      <td>%</td>
      <td>0.30</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2019-10-01</th>
      <td>Brasil</td>
      <td>Brasil</td>
      <td>outubro 2019</td>
      <td>IPCA - Variação acumulada em 12 meses</td>
      <td>5.Transportes</td>
      <td>%</td>
      <td>0.40</td>
    </tr>
    <tr>
      <th>2019-10-01</th>
      <td>Brasil</td>
      <td>Brasil</td>
      <td>outubro 2019</td>
      <td>IPCA - Variação acumulada em 12 meses</td>
      <td>6.Saúde e cuidados pessoais</td>
      <td>%</td>
      <td>4.34</td>
    </tr>
    <tr>
      <th>2019-10-01</th>
      <td>Brasil</td>
      <td>Brasil</td>
      <td>outubro 2019</td>
      <td>IPCA - Variação acumulada em 12 meses</td>
      <td>7.Despesas pessoais</td>
      <td>%</td>
      <td>3.13</td>
    </tr>
    <tr>
      <th>2019-10-01</th>
      <td>Brasil</td>
      <td>Brasil</td>
      <td>outubro 2019</td>
      <td>IPCA - Variação acumulada em 12 meses</td>
      <td>8.Educação</td>
      <td>%</td>
      <td>4.72</td>
    </tr>
    <tr>
      <th>2019-10-01</th>
      <td>Brasil</td>
      <td>Brasil</td>
      <td>outubro 2019</td>
      <td>IPCA - Variação acumulada em 12 meses</td>
      <td>9.Comunicação</td>
      <td>%</td>
      <td>0.35</td>
    </tr>
  </tbody>
</table>
<p>2256 rows × 7 columns</p>
</div>



This is what will look like before any manipulation. It also
has parameters for dates (`start`, `end` and `last_n`.
But also for the locations (`city`, `state`, `macroregion`,
`microregion`, `mesoregion`). You will need to get the code for
a given location and pass them as a list if there is more than one,
or you can pass "all" and you'll get data for all of possible values
of that location.


Let's now do the manipulation needed to the plot.


```python
ipca["2019-10"].pivot_table(
    index="Geral, grupo, subgrupo, item e subitem", columns="Variável", values="Valor"
).plot(kind="barh", figsize=(7, 7)).legend(
    loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.08)
)
```




    <matplotlib.legend.Legend at 0x7ff8b3c80690>




![png](README_files/README_39_1.png)


## Conclusion

Hope you enjoy the package!!

If you find any bugs or if you think something could be better, 
feel free to open an issue / contribute by opening a pull request!

## License

[MIT](https://github.com/phelipetls/seriesbr/blob/master/LICENSE)

## Support

If you find it useful, give this repo a start :)
