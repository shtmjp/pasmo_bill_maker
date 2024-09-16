# pasmo_bill_maker
### Before
<img width="457" alt="スクリーンショット 2024-09-17 0 26 32" src="https://github.com/user-attachments/assets/4e1765d1-bd64-4a1c-8aad-010cb5204a38">

### After
<img width="341" alt="スクリーンショット 2024-09-17 0 22 43" src="https://github.com/user-attachments/assets/b0f52ecc-30bd-4a8b-9cfb-5f0d164cdc96">

## Get started
1. PCから[モバイルPASMO公式サイト](https://www.mobile.pasmo.jp)にログインし、「SF(電子マネー)残額履歴」を開く
2. Excelファイルを作成したのち、該当するデータを表示し、直接コピペする
   - \[月/日, 種別, 利用場所, 種別, 利用場所, 残額, 差額\]というカラムがあればOK。
   - シート名は'Sheet1'にしておく
3. 以下を実行し、コンソール上で指示に従う
   ```
   git clone git@github.com:shtmjp/pasmo_bill_maker.git
   cd pasmo_bill_maker
   poetry install
   poetry run python3 exec.py
   ```
