import logging

import unittest

from cache.filecache import FileCache
from dartrig import DartWeb

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)-10s [%(levelname)s] %(message)s")

class TestDartWeb(unittest.TestCase):
    def test_list(self):
        dartweb = DartWeb()

        r = dartweb.search_report(1, "20200101", "20200131", "오뚜기")
        print(r)

    def test_detail(self):
        file_cache = FileCache(base_dir=f"./html_cache")
        dartweb = DartWeb(file_cache=file_cache)

        r = dartweb.request_detail("20200214000073", dtd="dart3.xsd")
        logging.info(r)

