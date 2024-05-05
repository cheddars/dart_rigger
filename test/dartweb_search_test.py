import random
import os
import traceback
import time
import logging
import pandas as pd
import unittest

from cache import RedisCache
from cache.filecache import FileCache
from dartrig import DartWeb
from filters import filter_market

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
