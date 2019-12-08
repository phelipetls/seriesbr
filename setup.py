import setuptools
import distutils

long_description = """
SeriesBR - A Python package to get brazilian economic time series

It has functions to get time series data from the Instituto de Pesquisa Econômica Aplicada (IPEA), Brazilian Central Bank (BCB) and Instituto Brasileiro de Geografia e Estatística (IBGE) databases into a pandas.DataFrame.

There are also functions to make queries and to get metadata information.

You can find more about at the GitHub [repository](https://github.com/phelipetls/seriesbr).
"""

setuptools.setup(
    name="seriesbr",
    version="0.0.5",
    author="Phelipe Teles",
    author_email="phelipe_teles@hotmail.com",
    description="Get requests for brazilian economic time series databases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phelipetls/brseries",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
