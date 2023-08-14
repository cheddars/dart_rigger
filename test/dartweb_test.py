import random
import os
import traceback
import time
import logging
import pandas as pd
import unittest
from cache.filecache import FileCache
from dartrig import DartWeb
from filters import filter_market

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)-10s [%(levelname)s] %(message)s")

BASE_DIR = "/Users/nezah/ws/projects/disclosure-squeezer/mgmt_data_archive/dart"


class TestDartWeb(unittest.TestCase):
    def test_list(self):
        dartweb = DartWeb()

        r = dartweb.search_report(1, "20200101", "20200131", "오뚜기")
        print(r)

    def test_viewer(self):
        file_cache = FileCache(base_dir=f"./html_cache")
        dartweb = DartWeb(file_cache=file_cache)

        r = dartweb.request_detail_with_dcm(rcp_no="20230526800078", dcm_no="9290146", dtd="html")
        # logging.info(r)

    def test_detail(self):
        file_cache = FileCache(base_dir=f"./html_cache")
        dartweb = DartWeb(file_cache=file_cache)

        r = dartweb.request_detail(rcp_no="20230526800078", dtd="html")
        logging.info(r)

    def test_dsaf_meta(self):
        file_cache = FileCache(base_dir=f"{BASE_DIR}/html_cache")
        dartweb = DartWeb(file_cache=file_cache)

        r = dartweb.get_dsaf_meta(company="리더스 기술투자", rcp_no="20220214001097")
        logging.info(r)
        r = dartweb.get_dsaf_meta(company="대동전자", rcp_no="20220214001035")
        logging.info(r)
        r = dartweb.get_dsaf_meta(company="동성화인텍", rcp_no="20220211000435")
        logging.info(r)

    def test_dsaf_meta_for_items(self):
        file_cache = FileCache(base_dir=f"{BASE_DIR}/html_cache")
        dartweb = DartWeb(file_cache=file_cache)
        year = 2020

        df = pd.read_pickle(f"{BASE_DIR}/list/dart_list_{year}.pkl")
        items = df.to_dict("records")

        filtered_items = list(filter(lambda x: "분기보고서" in x["title"].replace(" ", "") or
                                               "반기보고서" in x["title"].replace(" ", "") or
                                               "사업보고서" in x["title"].replace(" ", "")
                                     , items))
        filter_company = ["유한회사", "인수목적", "라닉스", "스펙"]
        filtered_items = list(filter(lambda x: not any([company in x["company"].replace(" ", "") for company in filter_company]), filtered_items))
        # filter_title = ["연장신고서", "기타경영사항", "기타주요경영사항"]
        # filtered_items = list(filter(lambda x: not any([title in x["title"].replace(" ", "") for title in filter_title]), filtered_items))
        filtered_items = list(filter(filter_market, filtered_items))
        total = len(filtered_items)
        logging.info(f"total : {total}")

        loop_break = min(1, total) + 1
        exception_list = []
        collected = []
        for item in filtered_items:
            use_cached = False
            try:
                if loop_break <= 0:
                    break
                loop_break -= 1
                title = item.get("title")
                rcp_no = item.get("rcp_no")
                company = item.get("company")
                # check file exists
                yyyy = rcp_no[:4]
                mm = rcp_no[4:6]
                dd = rcp_no[6:8]

                if os.path.exists(f"{BASE_DIR}/html_cache/dsaf/{yyyy}/{mm}/{dd}/{rcp_no}.html"):
                    use_cached = True

                r = dartweb.get_dsaf_meta(company=company, rcp_no=rcp_no)
                logging.info(f"{title} {company} : {r}")
                r.update(item)

            except Exception as e:
                logging.error(traceback.format_exc())
                exception_list.append(item)
                r = item

            collected.append(r)

            if not use_cached:
                num = random.randint(20, 40) / 10
                logging.info(f"sleep {num} seconds")
                time.sleep(num)

        df = pd.DataFrame(collected)
        df.to_pickle(f"{BASE_DIR}/list/dart_list_{year}_dsaf.pkl")
        for e in exception_list:
            logging.info(e)
