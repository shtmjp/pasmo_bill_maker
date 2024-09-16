from pathlib import Path

import pandas as pd

from pasmo_bill_maker.aggregate_records import aggregate_same_route, aggregate_to_daily
from pasmo_bill_maker.preprocess import preprocess


def get_commute_route(all_station: set[str]) -> list[tuple]:
    commute_route = []
    while True:
        c = len(commute_route) + 1
        dep = input(f"{c}つ目の出発駅を入力してください: ")
        if dep == "":
            yn = input("入力を終了しますか？(y/n): ")
            if yn == "y":
                break
            else:
                c = c - 1
                continue
        if dep not in all_station:
            print(f"{dep}はデータに存在しない駅です。")
            continue
        arr = input(f"{c}つ目の到着駅を入力してください: ")
        if arr not in all_station:
            print(f"{arr}はデータに存在しない駅です。")
            continue
        commute_route.append((dep, arr))
    yn = input(f"通勤ルートは以下の通りでよろしいですか？(y/n): \n{commute_route}")
    if yn == "n":
        yn = input("入力をやり直しますか？(y/n): ")
        if yn == "y":
            return get_commute_route(all_station)
        else:
            raise ValueError("入力を終了します。")
    return commute_route


def main() -> None:
    data_path = Path(
        input("Excelファイルをドラッグ&ドロップし、Enterを押してください: ")
    )
    df = pd.read_excel(data_path)
    df = preprocess(df)  # ride history data
    all_station = set(df["発"].unique()) | set(df["着"].unique())

    print(
        "通勤ルートを入力します。入力が終了したら、何も入力せずにEnterを押してください。"
    )
    commute_route = get_commute_route(all_station)

    df = aggregate_to_daily(df, commute_route)
    df = aggregate_same_route(df)

    output_path = data_path.with_name("result.xlsx")
    df.to_excel(output_path, index=False)
    print(f"結果を{output_path}に出力しました。")
