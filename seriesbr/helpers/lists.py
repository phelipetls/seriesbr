from pandas import DataFrame
from .request import get_json
from .utils import clean_json, search_list


def list_region(region, search, searches):
    """Help list IBGE metadata about a geographic region."""

    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/{region}"

    json = get_json(url)
    df = clean_json(json)

    return search_list(df, search, searches)


def list_metadata(resource_path):
    """Helper function to list IPEA database information."""

    url = "http://www.ipeadata.gov.br/api/odata4/"
    url += f"{resource_path}"
    json = get_json(url)["value"]

    return DataFrame(json)
