import configparser
import unittest

import logging
from cache import RedisCache, MemoryCache
from dartrig import DartAPI

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)-10s [%(levelname)s] %(message)s")

config = configparser.ConfigParser()
config.read("config.ini")

key = config["DART"]["API_KEY"]
class DartAPITest(unittest.TestCase):

    def test_list(self):
        #cache = RedisCache(host="localhost", port=6380, db=0, expire_mins=60*24, clear_cache=True)
        cache = MemoryCache()
        dartapi = DartAPI(keys=[key], cache=cache)

        r = dartapi.get_disclosure_list(end_de="20200102", max_page=10, use_cache=True)
        logging.debug(f"result A : {r}")

        r = dartapi.get_disclosure_list(end_de="20200102", max_page=10, use_cache=True)
        logging.debug(f"result B : {r}")

    def test_detail(self):
        #cache = RedisCache(host="localhost", port=6380, db=0, expire_mins=60*24, clear_cache=True)
        cache = MemoryCache()
        dartapi = DartAPI(keys=[key], cache=cache)

