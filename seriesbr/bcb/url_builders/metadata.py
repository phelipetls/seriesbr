def build_url(code):
    """Return a URL to search for a BCB time series metadata."""
    params = {"fq": f"codigo_sgs:{code}"}
    return "https://dadosabertos.bcb.gov.br/api/3/action/package_search", params
