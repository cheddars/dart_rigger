from dartrig import DartWeb


def test_list():
    dartweb = DartWeb()

    r = dartweb.search_report(1, "20200101", "20200131", "오뚜기")
    print(r)


if __name__ == "__main__":
    test_list()