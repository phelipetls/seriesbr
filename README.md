# SeriesBR: A Python package to get brazilian economic time series into a DataFrame


[\\![Build Status](<https://travis-ci.org/phelipetls/seriesbr.svg?branch=master>)](<https://travis-ci.org/phelipetls/seriesbr>)

<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#seriesbr-a-python-:session-package-to-get-brazilian-economic-time-series">1. SeriesBR: A Python package to get brazilian economic time series into a DataFrame</a>
<ul>
<li><a href="#sec-1-1">1.1. Introduction</a></li>
<li><a href="#sec-1-2">1.2. Installation</a></li>
<li><a href="#sec-1-3">1.3. Dependencies</a></li>
<li><a href="#sec-1-4">1.4. Main Features</a></li>
<li><a href="#sec-1-5">1.5. Demonstrations</a></li>
<li><a href="#sec-1-6">1.6. Conclusion</a></li>
<li><a href="#sec-1-7">1.7. License</a></li>
<li><a href="#sec-1-8">1.8. Support</a></li>
</ul>
</li>
</ul>
</div>
</div>

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

## Demonstrations

There are demonstration on you would use the package to get data from [BCB and IPEA](https://github.com/phelipetls/seriesbr/blob/master/BCB_E_IPEA_DEMO.org) or [IBGE](https://github.com/phelipetls/seriesbr/blob/master/IBGE_DEMO.org).

## Conclusion

Hope you enjoy the package!!

If you find any bugs or if you think something could be better, 
feel free to open an issue / contribute by opening a pull request!

## License

[MIT](https://github.com/phelipetls/seriesbr/blob/master/LICENSE)

## Support

If you find it useful, give this repo a start :)