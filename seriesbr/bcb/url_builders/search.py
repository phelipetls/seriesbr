def build_url(*strings, rows=10, start=1):
    """Return a URL to search in the BCB database."""
    url = "https://dadosabertos.bcb.gov.br/api/3/action/package_search?"

    first, others = strings[0], strings[1:]
    params = f"q={first}&rows={rows}&start={start}&sort=score desc"

    other_params = ""
    if others:
        joined_params = "+".join([str(s) for s in others])
        other_params = f"&fq={joined_params}"

    return f"{url}{params}{other_params}"
