import pandas as pd

from pasmo_bill_maker.aggregate_records import calc_oneday_record


def test_calc_oneday_record_1():
    # 例1: 寄り道せずちゃんと通勤した場合
    commute_route = [("東京", "渋谷"), ("渋谷", "駒場東大前")]
    df = pd.DataFrame(
        {
            "日付": [pd.Timestamp("2021-01-01")] * 4,
            "発": ["東京", "渋谷", "駒場東大前", "渋谷"],
            "着": ["渋谷", "駒場東大前", "渋谷", "東京"],
            "金額": [210, 140, 140, 210],
        },
    )
    out = calc_oneday_record(df, commute_route)
    assert len(out) == 1
    assert out[0] == {
        "date": pd.Timestamp("2021-01-01"),
        "category": "往復",
        "departure": "東京",
        "arrival": "駒場東大前",
        "fee": 210 + 140 + 140 + 210,
    }


def test_calc_oneday_record_2():
    # 例2: 帰りに渋谷でオールした場合
    commute_route = [("東京", "渋谷"), ("渋谷", "駒場東大前")]
    df = pd.DataFrame(
        {
            "日付": [pd.Timestamp("2021-01-01")] * 3,
            "発": ["東京", "渋谷", "駒場東大前"],
            "着": ["渋谷", "駒場東大前", "渋谷"],
            "金額": [210, 140, 140],
        },
    )
    out = calc_oneday_record(df, commute_route)
    assert len(out) == 2
    assert out[0] == {
        "date": pd.Timestamp("2021-01-01"),
        "category": "片道",
        "departure": "東京",
        "arrival": "駒場東大前",
        "fee": 210 + 140,
    }
    assert out[1] == {
        "date": pd.Timestamp("2021-01-01"),
        "category": "片道",
        "departure": "駒場東大前",
        "arrival": "渋谷",
        "fee": 140,
    }


def test_calc_oneday_record_3():
    # 例3: 研究室に泊まった場合
    commute_route = [("東京", "渋谷"), ("渋谷", "駒場東大前")]
    df = pd.DataFrame(
        {
            "日付": [pd.Timestamp("2021-01-01")] * 2,
            "発": ["東京", "渋谷"],
            "着": ["渋谷", "駒場東大前"],
            "金額": [210, 140],
        },
    )
    out = calc_oneday_record(df, commute_route)
    assert len(out) == 1
    assert out[0] == {
        "date": pd.Timestamp("2021-01-01"),
        "category": "片道",
        "departure": "東京",
        "arrival": "駒場東大前",
        "fee": 210 + 140,
    }


def test_calc_oneday_record_4():
    # 例4: 前日恵比寿に泊まって翌日通勤した場合
    commute_route = [("東京", "渋谷"), ("渋谷", "駒場東大前")]
    df = pd.DataFrame(
        {
            "日付": [pd.Timestamp("2021-01-01")] * 4,
            "発": ["恵比寿", "渋谷", "駒場東大前", "渋谷"],
            "着": ["渋谷", "駒場東大前", "渋谷", "東京"],
            "金額": [146, 140, 140, 210],
        },
    )
    out = calc_oneday_record(df, commute_route)
    assert len(out) == 2
    assert out[0] == {
        "date": pd.Timestamp("2021-01-01"),
        "category": "片道",
        "departure": "渋谷",
        "arrival": "駒場東大前",
        "fee": 140,
    }  # 恵比寿〜渋谷間は通勤経路に含まれないので請求しない
    assert out[1] == {
        "date": pd.Timestamp("2021-01-01"),
        "category": "片道",
        "departure": "駒場東大前",
        "arrival": "東京",
        "fee": 140 + 210,
    }
