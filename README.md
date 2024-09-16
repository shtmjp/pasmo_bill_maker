# pasmo_bill_maker
入力した通勤/通学区間に基づいて、公式サイトで取得できるPASMO利用履歴を集計し、
請求書に記載しやすい形式にする。

## Get started
```
cd pasmo_bill_maker
poetry install
poetry run python3 exec.py
```

## How to prepare the excel sheet
1. PCから[モバイルPASMO公式サイト](https://www.mobile.pasmo.jp)にログインし、「SF(電子マネー)残額履歴」を開く
2. 該当するデータを表示し、表を適当なExcelファイルに直接コピペする
   - \[月/日, 種別, 利用場所, 種別, 利用場所, 残額, 差額\]というカラムがあればOK。
   - シート名は'Sheet1'にしておく
3. `poetry run python3 exec.py`を実行し、ファイルを投入する
