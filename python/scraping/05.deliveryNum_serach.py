import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

#情報定義
JSON_KEY="[JSONキー名]"
spread_id = "[スプレッドシート名]"
spread_sheet_name = "[シート名]"
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
# chromedriver.exeがある場所を指定
driver_path = "chromedriver.exe"

#認証開始
credentials=ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY,scope)
Client = gspread.authorize(credentials)

SpreadSheet = Client.open_by_key(spread_id)
ws = SpreadSheet.worksheet(spread_sheet_name)

# webdriverの作成
service = Service(executable_path=driver_path)

driver = webdriver.Chrome(service=service)
i = 2
while ws.cell(i,7).value is not None:
    ouput_text = ""
    #ヤマト運輸に遷移
    url = 'https://toi.kuronekoyamato.co.jp/cgi-bin/tneko'
    driver.get(url)
    sleep(1);
    elem_input = driver.find_element(By.XPATH,'/html/body/div[3]/div[3]/form/div[2]/div[2]/div/div[1]/div[1]/input')
    elem_input.send_keys(ws.cell(i,7).value)
    sleep(0.5);
    elem_input.send_keys(Keys.ENTER)
    elem_outbput = driver.find_element(By.XPATH,'/html/body/div[3]/div[3]/form/div[2]/div[2]/div/div[2]/div/a')
    sleep(0.5);
    if not elem_outbput.text=="伝票番号誤り":
       ouput_text="【ヤマト運輸】:"+elem_outbput.text

    #佐川に遷移
    url = 'https://k2k.sagawa-exp.co.jp/p/sagawa/web/okurijoinput.jsp'
    driver.get(url)
    sleep(1);
    elem_input = driver.find_element(By.XPATH,'//*[@id="main:no1"]')
    elem_input.send_keys(ws.cell(i,7).value)
    sleep(0.5);
    elem__button = driver.find_element(By.XPATH,'//*[@id="main:toiStart"]')
    elem__button.send_keys(Keys.ENTER)
    elem_outbput = driver.find_element(By.XPATH,'//*[@id="list1"]/div/table/tbody/tr[1]/th[3]/span')
    sleep(0.5);
    ouput_text=ouput_text+"\n【佐川】:"+elem_outbput.text

    #郵便に遷移
    url = 'https://trackings.post.japanpost.jp/services/srv/search/input'
    driver.get(url)
    sleep(1);
    elem_input = driver.find_element(By.XPATH,'//*[@id="content"]/form/div[1]/ul/li[1]/label/input')
    elem_input.send_keys(ws.cell(i,7).value)
    sleep(0.5);
    elem_input.send_keys(Keys.ENTER)
    elem_outbput = driver.find_element(By.XPATH,'//*[@id="content"]/form/div/table/tbody/tr[3]/td[2]')
    sleep(0.5);
    ouput_text=ouput_text+"\n【郵便】:"+elem_outbput.text
    ws.update_cell(i,8, ouput_text)
    
    i=i+1;
