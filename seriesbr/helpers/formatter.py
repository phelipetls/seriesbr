def format_response_bcb(response):
    results = response.json()["result"]["results"]
    codigos, nomes = [], []
    for result in results:
        codigos.append(result["codigo_sgs"])
        nomes.append(result["title"])
    to_table(codigos, nomes)


def format_search_ipea(results):
    codigos = [item["SERCODIGO"] for item in results]
    nomes = [item["SERNOME"] for item in results]
    to_table(codigos, nomes)


def to_table(codigos, nomes):
    for codigo, nome in zip(codigos, nomes):
        print(f"{format(codigo, codigos)} | {nome}")


def format(string, iterable):
    return f"{string:<{len(max(iterable, key=len))}}"
