from seriesbr.utils import dates


def build_url(code, start=None, end=None, last_n=None):
    assert isinstance(code, (str, int)), "Not a valid code format."

    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"
    params = {"format": "json"}

    if last_n:
        url += f"/ultimos/{last_n}"
        return url, params

    start, end = dates.parse_dates(start, end, api="bcb")
    params["dataInicial"] = start
    params["dataFinal"] = end
    return url, params
