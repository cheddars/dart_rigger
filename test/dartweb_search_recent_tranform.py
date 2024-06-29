import unittest

import pandas as pd

class TestDartWeb(unittest.TestCase):

    def _month_merge_to_year_nb(self, year):
        file_dir = "/Users/nezah/ws/bylang/python/pypi_dart_api/test"

        months = [f"{year}{str(m).zfill(2)}" for m in range(1, 13)]

        dfx = pd.concat([pd.read_pickle(f"{file_dir}/dartweb_search_recent_month_{month}.pkl") for month in months])

        dfx.to_pickle(f"{file_dir}/dartweb_search_recent_year_{year}.pkl")

    def test_dart_web_month_to_year_nb(self):
        self._month_merge_to_year_nb(2008)