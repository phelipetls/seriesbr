import pytest
import pandas as pd

from seriesbr.helpers import utils


def test_cat():
    assert utils.cat(2, ",") == 2
    assert utils.cat("123", ",") == "123"
    assert utils.cat([1, 2, 3, 4], ",") == "1,2,3,4"
    assert utils.cat((4, 5), ",") == "4,5"


def test_is_isterable():
    assert utils.is_iterable([1])
    assert utils.is_iterable((1,))
    assert utils.is_iterable({1: 1})
    assert not utils.is_iterable(1)
    assert not utils.is_iterable("1")


def test_build_query():
    assert utils.build_query(1) == "nome.str.contains('(?iu)1')"
    assert utils.build_query("oi") == "nome.str.contains('(?iu)oi')"
    assert utils.build_query([1, 2, 3]) == "nome.str.contains('(?iu)1|2|3')"
    assert utils.build_query("nome", {"pesquisa_nome": "pesquisa"}) == (
        "nome.str.contains('(?iu)nome')"
        " and pesquisa_nome.str.contains('(?iu)pesquisa')"
    )
    assert utils.build_query(
        ["nome", "outro"], {"pesquisa_nome": ["pesquisa", "outra"]}
    ) == (
        "nome.str.contains('(?iu)nome|outro')"
        " and pesquisa_nome.str.contains('(?iu)pesquisa|outra')"
    )
    utils.build_query(
        ["oi", "tudo"], {"pesquisa_nome": ["DD", "DI"], "pesquisa_id": "AA"}
    ) == (
        "nome.str.contains('(?iu)oi|tudo')"
        " and pesquisa_nome.str.contains('(?iu)DD|DI')"
        " and pesquisa_id.str.contains('(?iu)AA')"
    )


df = pd.DataFrame([1, 2, 3], columns=["column"])


def test_searching_non_existent_column():
    with pytest.raises(ValueError):
        utils.search_df(df, "nome", {"non_existent_column": "string"})


def test_collect_codes_and_names_dict():
    assert utils.collect({"A": 1, "B": 2}, 100) == {"A": 1, "B": 2, 100: 100}


def test_collect_codes_and_names_no_dict():
    assert utils.collect(11) == {11: 11}
