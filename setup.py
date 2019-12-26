import setuptools
import distutils

long_description = """
SeriesBR - A Python package to interact with brazilian time series databases

It has functions to get time series data from Instituto de Pesquisa Econômica Aplicada (IPEA), Banco Central do Brasil (BCB) and Instituto Brasileiro de Geografia e Estatística (IBGE) databases into a DataFrame.

Learn more about it in our [repository](https://github.com/phelipetls/seriesbr) or [documentation](https://seriesbr.readthedocs.io).
"""

setuptools.setup(
    name="seriesbr",
    version="0.1.2",
    author="Phelipe Teles",
    author_email="phelipe_teles@hotmail.com",
    description="Get requests for brazilian economic time series databases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phelipetls/seriesbr",
    packages=setuptools.find_packages(),
    install_requires=["pandas", "requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    project_urls={
        "Documentation": "https://seriesbr.readthedocs.io/",
    },
)
