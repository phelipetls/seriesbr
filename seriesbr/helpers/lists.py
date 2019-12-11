from pandas import DataFrame
from .request import get_json
from .utils import clean_json, do_search


# IBGE


def list_regions(kind_of_region, search, where):
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/{kind_of_region}"
    json = get_json(url)
    df = clean_json(json)
    if search:
        return do_search(df, search, where)
    return df


# IPEA


def list_metadata(resource_path):
    baseurl = "http://www.ipeadata.gov.br/api/odata4/"
    url = f"{baseurl}{resource_path}"
    json = get_json(url)["value"]
    return DataFrame(json)
