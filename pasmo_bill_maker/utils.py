import datetime

import pandas as pd


def get_datetime(val: object) -> datetime.datetime:
    """
    Excelで読み込んだdataframeの日付はシリアル値になっていることがあるので, datetime.datetimeに変換する
    cf. https://qiita.com/ponsuke0531/items/4ddbc6438a817790dfa3
    """
    val_type = type(val)
    # datetime.datetimeだったらそのまま返却
    if val_type is datetime.datetime:
        return val
    # pandas.Timestampはdatetime.datetimeを継承していてdatetime.datetimeとして処理できそうなのでそのまま返却
    if issubclass(val_type, datetime.datetime):
        return val
    # intだったらシリアル値としてdatetime.datetimeに変換して返却
    if val_type is int:
        if val < 60:
            # 1900-03-01より前の場合
            days = val - 1
        else:
            # 1900-03-01以降の場合
            days = val - 2
        return pd.to_datetime("1900/01/01") + datetime.timedelta(days=days)
    return None


def find_first_and_last_index(lst: list[bool]) -> tuple:
    try:
        first_index = lst.index(True)
    except ValueError:
        return None, None

    last_index = len(lst) - 1 - lst[::-1].index(True)
    return first_index, last_index


def convert_dates_to_str(dates) -> str:
    if not dates:
        return ""

    dates.sort()  # Ensure dates are sorted in case they aren't
    result = []
    start = dates[0]
    end = dates[0]

    for i in range(1, len(dates)):
        if (dates[i] - dates[i - 1]).days == 1:  # Check if consecutive
            end = dates[i]
        else:
            if start == end:
                result.append(f"{start.month}/{start.day}")
            else:
                result.append(f"{start.month}/{start.day}-{end.month}/{end.day}")
            start = end = dates[i]

    # Append the last range or single date
    if start == end:
        result.append(f"{start.month}/{start.day}")
    else:
        result.append(f"{start.month}/{start.day}-{end.month}/{end.day}")

    return ", ".join(result)
