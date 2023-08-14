import time
import random
import os
import logging
import pandas as pd
import unittest
from cache.filecache import FileCache
from dartrig import DartWeb
from filters import filter_market, filter_titles, filter_node_contains

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)-10s [%(levelname)s] %(message)s")

BASE_DIR = "/Users/nezah/ws/projects/disclosure-squeezer/mgmt_data_archive/dart"


class DartwebDsafParseTest(unittest.TestCase):

    def test_compare(self):
        file_cache = FileCache(base_dir=f"{BASE_DIR}/html_cache")
        dartweb = DartWeb(file_cache=file_cache)

        year = 2022
        df = pd.read_pickle(f"{BASE_DIR}/list/dart_list_{year}.pkl")
        items = df.to_dict("records")
        logging.info(f"loaded items : {len(items)}")
        filtered = list(filter(filter_market, items))
        logging.info(f"after market filtered : {len(filtered)}")
        filtered = list(filter(filter_titles, filtered))
        logging.info(f"after title filtered : {len(filtered)}")
        filtered = list(filter(lambda x: "분기보고서" in x.get('title'), filtered))

        break_point = 100

        not_matched = []
        meta1_3_not_match = []
        for item in filtered[:break_point]:
            company = item.get("company")
            rcp_no = item.get("rcp_no")

            yyyy = rcp_no[:4]
            mm = rcp_no[4:6]
            dd = rcp_no[6:8]
            need_sleep = True
            if os.path.exists(f"{BASE_DIR}/html_cache/dsaf/{yyyy}/{mm}/{dd}/{rcp_no}.html"):
                need_sleep = False

            dcm_no, nodes = dartweb.get_dsaf_nodes(rcp_no=rcp_no)

            if dcm_no != nodes[0].dcm_no:
                not_matched.append(item)
                logging.error(f"meta2 - meta3 not matched ")
                break

            gb_type = "gb"
            if filter_node_contains("2.연결재무", nodes):
                if not filter_node_contains("연결재무제표주석", nodes):
                    gb_type = "yg"
                else:
                    if filter_node_contains("1.요약재무", nodes):
                        if filter_node_contains("소규모", nodes):
                            gb_type = "gb2"

            logging.info(f"gb_type : {gb_type}")

            if need_sleep:
                timing = random.randint(10, 30) / 10
                logging.info(f"sleep for {timing}")
                time.sleep(timing)

        logging.info("start not matched")
        for nm in not_matched:
            logging.info(nm)

        logging.info("start meta 1 3 not matched")
        for m in meta1_3_not_match:
            logging.info(m)
            #r = dartweb.request_detail_with_dcm(rcp_no="20230526800078", dcm_no="9290146", dtd="html")