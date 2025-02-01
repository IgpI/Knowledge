from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

# chromedriver.exeがある場所を指定
driver_path = "chromedriver.exe"

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
elem_input_pass = driver.find_element(By.ID,'password')
elem_input_pass.send_keys("[パスワード]")
elem_input_pass.send_keys(Keys.ENTER)
sleep(3);

#全体ビュー取得
elem_overview = driver.find_element(By.CLASS_NAME, "o-statsContent__overviewNum").text;
print(elem_overview)
