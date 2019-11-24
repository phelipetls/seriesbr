import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seriesbr",
    version="0.0.1",
    author="Phelipe Teles",
    author_email="phelipe_teles@hotmail.com",
    description="Get requests for brazilian economic time series",
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
