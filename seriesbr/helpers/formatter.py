import re
from bs4 import BeautifulSoup as bs


def format_results_bcb(results, page):
    soup = bs(results.text, 'html.parser')
    last_page = get_last_page(soup)
    datasets = soup.find_all({"h3": {"class": "dataset-heading"}})
    codigos, nomes = [], []
    for dataset in datasets:
        if dataset.a is not None:
            codigos.append(extract_code(dataset.a["href"]))
            nomes.append(dataset.text.replace("\n", ""))
    print(f"Page {page} of {last_page}")
    to_table(codigos, nomes)


def format_results_ipea(results):
    codigos = [item["SERCODIGO"] for item in results]
    nomes = [item["SERNOME"] for item in results]
    to_table(codigos, nomes)


def to_table(codigos, nomes):
    for codigo, nome in zip(codigos, nomes):
        print(f"{format(codigo, codigos)} | {format(nome, nomes)} |")


def format(string, iterable):
    return f"{string:<{len(max(iterable, key=len))}}"


def extract_code(codigo):
    try:
        return re.search("/dataset/(\d+)-.*", codigo).group(1)
    except AttributeError:
        return ""


def get_last_page(soup):
    try:
        return soup.find_all("div", "pagination")[0].find_all("li")[-2].text
    except IndexError:
        raise
        print("Nothing was found.")
