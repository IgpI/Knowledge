!pip install gspread
!pip install  oauth2client

import gspread
from oauth2client.service_account import ServiceAccountCredentials

#情報定義
JSON_KEY="JSONキーファイル名"
spread_id = "[スプレッドシートのID]"
spread_sheet_name = "[シート名]"
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#認証
credentials=ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY,scope)
Client = gspread.authorize(credentials)

#スプレッドシートのシート連携
SpreadSheet = Client.open_by_key(spread_id)
ws = SpreadSheet.worksheet(spread_sheet_name)

#出力
print(ws.acell("B3").value)
print(ws.acell("C3").value)
