import re


def parse_td1(td):
    wrap = td.find("span", "innerWrap")
    wrapTag = td.find("span", "innerWrapTag")
    regex = ".*openCorpInfoNew\('(?P<code>\d*)', '(?P<pop_id>[a-zA-Z]*)', '(?P<pop_link>[\/a-zA-Z0-9.]*)'\);.*"

    w = wrap if wrap else wrapTag

    if w:
        spans = w.select("span")
        ahref = w.find("a")["href"]
        m = re.match(regex, ahref)
        link_info = m.groupdict() if m else {}
        link_info["cls"] = spans[0]["title"]
        return link_info


def parse_td2(td):
    a = td.find("a")
    ahref = a["href"]
    aid = a["id"]
    aonclick = a["onclick"]

    regex = ".*openReportViewer\('(?P<rcp_no>\d*)','(?P<param2>.*)'\);.*"
    m = re.match(regex, aonclick)
    params = m.groupdict() if m else {}

    regex = ".*openReportViewer\('(?P<rcp_no>\d*)'\);.*"
    m = re.match(regex, aonclick)
    if not params:
        params = m.groupdict() if m else {}

    params["link"] = ahref
    params["id"] = aid
    params["title"] = a.text.strip().replace("\n", "").replace("\t", "")
    return params