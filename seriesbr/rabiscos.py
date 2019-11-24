import requests
cod = "SGS12_IBCBR12"
baseurl = "http://www.ipeadata.gov.br/api/odata4/"
resource_path = f"Metadados(SERCODIGO='{cod}')"
query = "?$select=SERNOME"
url = f"{baseurl}{resource_path}{query}"
# baseurl = "http://ipeadata2-homologa.ipea.gov.br/api/v1/"
# resource_path = f"Metadados(SERCODIGO='{cod}')?$select=PAICODIGO"
# url = f"{baseurl}{resource_path}"
print(requests.get(url).json())
