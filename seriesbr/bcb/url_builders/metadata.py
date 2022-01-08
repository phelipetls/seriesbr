def build_url(code):
    params = {"fq": f"codigo_sgs:{code}"}
    return "https://dadosabertos.bcb.gov.br/api/3/action/package_search", params
