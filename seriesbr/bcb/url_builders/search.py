def build_url(*strings, rows=10, start=1):
    """Return a URL to search in the BCB database."""
    url = "https://dadosabertos.bcb.gov.br/api/3/action/package_search"

    first, others = strings[0], strings[1:]
    params = {"q": first, "rows": rows, "start": start, "sort": "score desc"}

    if others:
        joined_params = "+".join([str(s) for s in others])
        params["fq"] = joined_params

    return url, params
