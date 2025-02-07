!pip install gspread
!pip install  oauth2client
!pip install pyautogui pyperclip

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import pyautogui
import pyperclip

#情報定義
JSON_KEY="[GCPで取得したjsonのキーファイル名]"
spread_id = "[スプレッドシートのID]"
spread_sheet_name = "[シート名]"
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
# chromedriver.exeがある場所を指定
driver_path = "chromedriver.exe"

credentials=ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY,scope)
Client = gspread.authorize(credentials)

SpreadSheet = Client.open_by_key(spread_id)
ws = SpreadSheet.worksheet(spread_sheet_name)

# webdriverの作成
service = Service(executable_path=driver_path)

#noteに遷移
driver = webdriver.Chrome(service=service)
url = 'https://note.com/sitesettings/stats'
driver.get(url)
sleep(3);

#入力
elem_input_mail = driver.find_element(By.ID,'email')
elem_input_mail.send_keys("[メールアドレス]")
elem_input_pass = driver.find_element(By.ID,'[パスワード]')
elem_input_pass.send_keys("01Brain10_note")
elem_input_pass.send_keys(Keys.ENTER)
sleep(2);

#記事を開く
driver.get("https://note.com/notes/new")
sleep(2);

#件名
elem_input_subject = driver.find_element(By.XPATH,'//*[@id="__next"]/div[3]/div[1]/div[2]/div[1]/main/textarea')
sleep(1);
elem_input_subject.send_keys(ws.acell("B3").value)
sleep(1);

#はじめに
elem_input_content = driver.find_element(By.CLASS_NAME,'paragraph')
sleep(1);
elem_input_content.send_keys(ws.acell("C3").value)
sleep(1);

#見出し
pyautogui.press('Enter')
pyautogui.press('Enter')
pyperclip.copy(ws.acell("D3").value)
pyautogui.hotkey('ctrl','v')
sleep(1);
pyautogui.hotkey('shift','home')
sleep(1);
pyautogui.press(['tab','tab','down','Enter'])

#本文
pyautogui.press('Enter')
pyautogui.press('Enter')
sleep(1);
elem_input_content.send_keys(ws.acell("E3").value)
sleep(1);

#目次
pyautogui.hotkey('ctrlleft','home')
elem_input_index = driver.find_element(By.XPATH,'//*[@id="__next"]/div[3]/div[1]/div[2]/div[4]/button')
sleep(1);
elem_input_index.send_keys(Keys.ENTER)
sleep(1);
elem_input_index = driver.find_element(By.XPATH,'//*[@id="toc-setting"]')
sleep(1);
elem_input_index.send_keys(Keys.ENTER)
sleep(1);

#投稿ボタン
elem_input_post = driver.find_element(By.XPATH,'//*[@id=":r6:"]')
sleep(1);
elem_input_post.send_keys(Keys.ENTER)
sleep(1);
elem_input_pass = driver.find_element(By.XPATH,'//*[@id=":rv:"]')
sleep(1);
elem_input_pass.send_keys(Keys.ENTER)
sleep(1);


#driver.quit()
