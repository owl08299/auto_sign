from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

# 啟動 Chrome 瀏覽器，你也可以選擇其他瀏覽器
browser = webdriver.Chrome()

# 打開打卡網址
url = "https://hr2sys.tmu.edu.tw/tmu_planhum_full/login_full_duty.aspx"
browser.get(url)

# 輸入帳號和密碼
username_input = browser.find_element("id", "UserName")  # 替換成實際的帳號欄位ID
password_input = browser.find_element("id", "Password")  # 替換成實際的密碼欄位ID

username_input.send_keys("F129675078")  # 替換成你的帳號
password_input.send_keys("F129675079")  # 替換成你的密碼
    

# 點擊登錄按鈕
login_button = browser.find_element("id", "LoginButton")  # 替換成實際的登錄按鈕ID
login_button.click()

# 等待一段時間，確保登錄成功（可以根據實際情況調整等待時間）
time.sleep(30)

# 確認使用者今天是否已簽到過
soup = BeautifulSoup(browser.page_source, 'html.parser')
target_text = soup.find('div', {'id': 'showloginmsg'}).find('div', {'class': 'form-group'}).text.strip()
print(target_text)


time.sleep(10)
# page_text = browser.find_element("tag name", "body").text
# print(page_text)

# time.sleep(60)
# if "今日已於" in page_text and "簽到" in page_text:
#     print("已簽到，進行相應的操作")
#     # 這裡可以進行後續的操作，例如簽退等
#     # ...

#     # 模擬按返回
#     browser.execute_script("window.history.go(-1)")
#     # 等待一段時間，確保返回成功（可以根據實際情況調整等待時間）
#     time.sleep(5)

# 關閉瀏覽器
#browser.quit()
