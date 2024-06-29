from typing import List

import calendar
import time
import logging
import pandas as pd
import unittest
from cache import RedisCache
from dartrig import DartWeb
from dartrig.parser.parser_search import SearchNode

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)-10s [%(levelname)s] %(message)s")

BASE_DIR = "/Users/nezah/ws/projects/disclosure-squeezer/mgmt_data_archive/dart"


class TestDartWeb(unittest.TestCase):

    def test_search(self):
        dartweb = DartWeb()

        r = dartweb._search_recent_report(1, "2024.05.02")
        print(r.to_dict())
        print("###########\n\n")
        r = dartweb._search_recent_report(2, "2024.05.02")
        print(r.to_dict())

    def test_search_report(self):
        dartweb = DartWeb()
        r = dartweb.search_recent_report("2024.05.02")
        print(r)

    def test_search_report_redis(self):
        dartweb = DartWeb(cache=RedisCache(host="localhost", port=6379, db=6))

        r = dartweb.search_report("20240501", "20240503", srch_txt="")
        print(len(r))
        r = dartweb.search_report("20240501", "20240503", srch_txt="")
        print(len(r))

    def test_search_report_month(self):
        def _fetch_month(year, month):
            _, lastday = calendar.monthrange(year, month)

            dartweb = DartWeb()

            dft = pd.DataFrame()
            for d in range(1, lastday + 1):

                dt = f"{year}.{str(month).zfill(2)}.{str(d).zfill(2)}"
                print(f"dt : {dt}")
                r: List[SearchNode] = dartweb.search_recent_report(dt)
                df = pd.DataFrame([i.to_dict() for i in r])
                dft = pd.concat([dft, df])
                time.sleep(3)

            dft.to_pickle(f"dartweb_search_recent_month_{year}{str(month).zfill(2)}.pkl")

        year = 2008

        for m in range(1, 13):
            _fetch_month(year, m)
            time.sleep(5)


