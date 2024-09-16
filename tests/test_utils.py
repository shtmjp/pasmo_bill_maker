import datetime

from pasmo_bill_maker.utils import convert_dates_to_str, find_first_and_last_index


def test_find_first_and_last_index():
    lst = [0, 0, 1, 0, 1, 0, 1]
    lst = [bool(i) for i in lst]
    first_index, last_index = find_first_and_last_index(lst)
    assert first_index == 2
    assert last_index == 6


def test_convert_dates_to_str_with_date():
    # Test case 1: Consecutive and non-consecutive dates
    dates1 = [
        datetime.date(2021, 8, 29),
        datetime.date(2021, 8, 30),
        datetime.date(2021, 9, 2),
        datetime.date(2021, 9, 3),
        datetime.date(2021, 9, 4),
    ]
    result1 = convert_dates_to_str(dates1)
    expected1 = "8/29-8/30, 9/2-9/4"
    assert result1 == expected1

    # Test case 2: Single date only
    dates2 = [datetime.date(2021, 10, 1)]
    result2 = convert_dates_to_str(dates2)
    expected2 = "10/1"
    assert result2 == expected2

    # Test case 3: Multiple non-consecutive single dates
    dates3 = [
        datetime.date(2021, 11, 1),
        datetime.date(2021, 11, 3),
        datetime.date(2021, 11, 5),
    ]
    result3 = convert_dates_to_str(dates3)
    expected3 = "11/1, 11/3, 11/5"
    assert result3 == expected3

    # Test case 4: Multiple consecutive dates
    dates4 = [
        datetime.date(2021, 12, 1),
        datetime.date(2021, 12, 2),
        datetime.date(2021, 12, 3),
        datetime.date(2021, 12, 4),
    ]
    result4 = convert_dates_to_str(dates4)
    expected4 = "12/1-12/4"
    assert result4 == expected4
