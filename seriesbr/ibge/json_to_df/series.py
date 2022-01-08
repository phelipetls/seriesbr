import pandas as pd


def build_df(json, freq="mensal"):
    # first element contains only metadata
    # let's ignore it
    df = pd.DataFrame(json[1:])

    # getting columns names
    df.columns = json[0].values()

    # handling dates
    date_fmt = "%Y" if freq == "anual" else "%Y%m"
    date_key = json[0]["D2C"]
    df[date_key] = pd.to_datetime(df[date_key], format=date_fmt)
    df = df.set_index(date_key)
    df = df.rename_axis("Date")

    # handling numerical values
    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")

    # getting the specific location column name
    location_key = json[0]["D1C"]

    # drop these columns
    to_drop = ["Mês", "Unidade de Medida", "Brasil", "Nível Territorial"]

    # also every columns that is a code
    is_code = lambda column: column.endswith("(Código)")  # noqa: E731

    # except for the location and variable code
    is_location_code = lambda column: column == location_key  # noqa: E731
    is_variable_code = lambda column: column == "Variável (Código)"  # noqa: E731

    to_drop.extend(
        [
            c
            for c in df.columns
            if is_code(c) and not (is_location_code(c) or is_variable_code(c))
        ]
    )

    df = df.drop(to_drop, axis="columns", errors="ignore")

    return df
