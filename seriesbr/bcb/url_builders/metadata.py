def build_url(code):
    """Return a URL to search for a BCB time series metadata."""
    baseurl = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?"
    params = f"fq=codigo_sgs:{code}"
    return f"{baseurl}{params}"
