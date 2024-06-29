from typing import List

from datetime import datetime
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

        r = dartweb._search_report(1, "20240501", "20240503", srch_txt="")

    def test_search_report(self):
        dartweb = DartWeb()

        r = dartweb.search_report("20240501", "20240503", srch_txt="")
        r = dartweb.search_report("20240501", "20240503", srch_txt="")

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
            start = f"{year}{str(month).zfill(2)}01"
            end = f"{year}{str(month).zfill(2)}{lastday}"
            print(f"start : {start}, end : {end}")
            r: List[SearchNode] = dartweb.search_report(start, end, srch_txt="")
            df = pd.DataFrame([i.to_dict() for i in r])
            df.to_pickle(f"dartweb_search_month_{year}{str(month).zfill(2)}.pkl")

        year = 2012

        for m in range(1, 13):
            _fetch_month(year, m)
            time.sleep(5)

    def test_periodic_fetch(self):
        dartweb = DartWeb(cache=RedisCache(host="localhost", port=6379, db=6))

        dt = datetime.now().strftime("%Y%m%d")
        all_items = []
        i = 0
        while True:
            items: List[SearchNode] = dartweb.search_report(dt, dt, srch_txt="")
            all_items.extend(items)

            if i % 600 == 0:
                n = datetime.now()
                fn = n.strftime("%Y%m%d%H%M%S")
                print(f"Saving {len(all_items)} items to {fn} items : {len(all_items)}")
                item_dicts = [i.to_dict() for i in all_items]
                pd.DataFrame(item_dicts).to_pickle(f"dartweb_search_test_{fn}.pkl")

            i += 1
            time.sleep(0.3)

    def test_trasform_df(self):
        df = pd.read_pickle("dartweb_search_20240401_20240508.pkl")
        print(df.head(5))
        print(df.info())
        print(df.dtypes)

        # series = df[0]
        # x = [i.__dict__() for i in series]
        # dfx = pd.DataFrame(x)
        # dfx.to_pickle("dartweb_search_20240401_20240508_transformed.pkl")
        #
