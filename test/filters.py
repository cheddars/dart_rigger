from typing import List

from dartrig.parser import DsafNode

TITLE_WHITELIST = [
    "최대주주",
    "투자판단",
    "조회공시",
    "단일판매ㆍ공급계약체결",
    "특허권취득",
    "영업실적 등에 대한 전망",
    "수시공시",
    "신규시설투자등",
    "소송",
    "거래정지",
    "영업정지",
    "관리종목",
    "매출액",
    "상장폐지",
    "중단",
    "타법인주식및출자증권처분결정",
    "연결재무제표 기준 영업(잠정)실적",
    "타법인주식및출자증권취득결정",
    "타법인주식및출자증권양수결정",
    "우선주의 보통주",
    "전환청구권",
    "영업(잠정)실적(공정공시)",
    "영업양수결정",
    "연결재무제표기준영업(잠정)실적",
    "주요사항보고서",
    "최대주주변경을수반하는주식양수도계약체결",
    "타법인주식 및 출자증권 양수결정",
    "기타경영사항",
    "주식소각결정",
    "기술도입ㆍ이전ㆍ제휴 계약체결",
    "감자",
    "전환가",
    "신주인수권행사",
    "유상증자결정", "유무상증자결정", "무상증자결정",
    "전환사채권발행결정",
    "최대주주등",
    "전환가액의조정",
    "분기보고서",
    "반기보고서",
    "사업보고서",
    "장래사업",
    "주요주주특정증권",
    "자기주식취득결정",
    "수시공시의무관련사항",
    "유형자산양수결정",
    "자기주식취득신탁계약체결결정",
    "주식등의대량보유상황보고서",
    "회사분할결정",
    "기업설명회",
    "주요사항보고서(감자결정)"
]


def filter_market(info):
    market = info.get("market")
    return market == "K" or market == "Y"

def filter_titles(info):
    title = info.get("title")
    for keyword in TITLE_WHITELIST:
        if keyword.replace(" ", "") in title.replace(" ", ""):
            return True

    return False


def find_node_contains(find_str, nodes: List[DsafNode]):
    for node in nodes:
        text = node.text
        if text is None:
            continue
        if find_str.replace(" ", "") in text.replace(" ", ""):
            return node
    return None


def filter_node_contains(find_str, nodes: List[DsafNode]):
    return find_node_contains(find_str, nodes) is not None