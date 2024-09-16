import pandas as pd

from pasmo_bill_maker.utils import get_datetime


def validate_raw_data(df: pd.DataFrame) -> None:
    assert set(["月/日", "利用場所", "利用場所.1", "差額", "請求可否"]).issubset(
        set(df.columns)
    )


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    validate_raw_data(df)
    df["金額"] = -df["差額"]
    df = df[df["請求可否"] == 1].copy()
    df["月/日"] = df["月/日"].apply(get_datetime)
    df.rename(
        columns={
            "月/日": "日付",
            "利用場所": "発",
            "利用場所.1": "着",
        },
        inplace=True,
    )
    df["金額"] = -df["差額"]
    df["発"] = df["発"].str.strip()
    df["着"] = df["着"].str.strip()
    df = df[["日付", "発", "着", "金額"]]
    return df
