from seriesbr.utils import dates


def build_url(code, start=None, end=None, last_n=None):
    """Return the url for a BCB time series."""
    assert isinstance(code, (str, int)), "Not a valid code format."

    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"

    if last_n:
        url += f"/ultimos/{last_n}"
        url += "?format=json"
        return url

    start, end = dates.parse_dates(start, end, api="bcb")
    return f"{url}?format=json&dataInicial={start}&dataFinal={end}"
