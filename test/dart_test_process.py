import pandas as pd
import numpy as np


def dart_web_month_to_year_nb(year):
    file_dir = "/Users/nezah/ws/bylang/python/pypi_dart_api/test"

    months = [f"{year}{str(m).zfill(2)}" for m in range(1, 13)]

    dfx = pd.concat([pd.read_pickle(f"{file_dir}/dartweb_search_month_{month}.pkl") for month in months])

    dfx.to_pickle(f"{file_dir}/dartweb_search_year_{year}.pkl")


if __name__ == "__main__":
    dart_web_month_to_year_nb(2012)