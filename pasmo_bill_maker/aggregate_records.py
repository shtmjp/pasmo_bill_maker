import pandas as pd

from pasmo_bill_maker.utils import convert_dates_to_str, find_first_and_last_index


def get_commute_route() -> list[tuple]:
    # TODO: make some user interface
    return [("平沼橋", "相鉄横浜"), ("横浜", "東京"), ("地　東京", "地本郷三")]


def validate_dataframe(df: pd.DataFrame) -> None:
    assert set(df.columns) == set(["日付", "発", "着", "金額"])
    assert df["日付"].apply(type).eq(pd.Timestamp).all()
    assert df["発"].apply(type).eq(str).all()
    assert df["着"].apply(type).eq(str).all()
    assert df["金額"].apply(type).eq(int).all()
    assert df.isna().sum().sum() == 0


def calc_oneday_record(df: pd.DataFrame, commute_route: list[tuple]) -> list[dict]:
    validate_dataframe(df)
    assert df["日付"].unique().size == 1
    date = df["日付"].unique()[0]

    nobori_route = commute_route
    nobori_is_taken = {r: False for r in nobori_route}
    kudari_route = [(r[1], r[0]) for r in commute_route[::-1]]
    kudari_is_taken = {r: False for r in kudari_route}
    nobori_fee, kudari_fee = 0, 0

    for _, row in df.iterrows():
        dep, arr, fee = row[["発", "着", "金額"]]
        if (dep, arr) in nobori_is_taken:
            nobori_is_taken[(dep, arr)] = True
            nobori_fee += fee
        elif (dep, arr) in kudari_is_taken:
            kudari_is_taken[(dep, arr)] = True
            kudari_fee += fee

    nobori_is_taken_list = [nobori_is_taken[r] for r in nobori_route]
    kudari_is_taken_list = [kudari_is_taken[r] for r in kudari_route]

    out = []
    # 往復
    if nobori_is_taken_list == kudari_is_taken_list[::-1]:
        dep_idx, arr_idx = find_first_and_last_index(nobori_is_taken_list)
        out.append(
            {
                "date": date,
                "category": "往復",
                "departure": nobori_route[dep_idx][0],
                "arrival": nobori_route[arr_idx][1],
                "fee": nobori_fee + kudari_fee,
            }
        )
    # 片道
    else:
        if any(nobori_is_taken_list):
            dep_idx, arr_idx = find_first_and_last_index(nobori_is_taken_list)
            out.append(
                {
                    "date": date,
                    "category": "片道",
                    "departure": nobori_route[dep_idx][0],
                    "arrival": nobori_route[arr_idx][1],
                    "fee": nobori_fee,
                }
            )
        if any(kudari_is_taken_list):
            dep_idx, arr_idx = find_first_and_last_index(kudari_is_taken_list)
            out.append(
                {
                    "date": date,
                    "category": "片道",
                    "departure": kudari_route[dep_idx][0],
                    "arrival": kudari_route[arr_idx][1],
                    "fee": kudari_fee,
                }
            )
    return out


def aggregate_to_daily(df: pd.DataFrame, commute_route: list[tuple]) -> pd.DataFrame:
    aggregated_records = []
    for _, sub_df in df.groupby("日付"):
        aggregated_records.extend(calc_oneday_record(sub_df, commute_route))
    out_df = pd.DataFrame(aggregated_records)
    return out_df


def aggregate_same_route(df: pd.DataFrame) -> pd.DataFrame:
    all_years = df["date"].dt.year.unique()
    assert len(all_years) == 1

    results = []
    for _, g in df.groupby(["category", "departure", "arrival"]):
        dates = g["date"].tolist()
        category, dep, arr = (
            g["category"].iloc[0],
            g["departure"].iloc[0],
            g["arrival"].iloc[0],
        )
        date_str = convert_dates_to_str(dates)
        arrow = "->" if g["category"].iloc[0] == "往復" else "->"
        route_str = f"電車（{dep}{arrow}{arr}）{category}"

        fee = g["fee"].sum()
        results.append(
            {
                "date": date_str,
                "route": route_str,
                "fee": fee,
            }
        )
    return pd.DataFrame(results)
