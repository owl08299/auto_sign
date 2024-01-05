from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import schedule

def perform_sign_in(username):
    # 打卡程式碼
    browser = webdriver.Chrome()

    url = "http://localhost:5000/"
    browser.get(url)

    username_input = browser.find_element("id", "UserName")
    password_input = browser.find_element("id", "Password")

    username_input.send_keys(username)
    password_input.send_keys("wilson")

    login_button = browser.find_element("id", "LoginButton")
    login_button.click()

    time.sleep(3)

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    target_text = soup.find('div', {'id': 'showloginmsg'}).find('div', {'class': 'form-group'}).text.strip()
    print(target_text)

    time.sleep(10)

    browser.quit()

def job():
    # 在此處指定要打卡的使用者和時間
    username = "M610111013"
    perform_sign_in(username)

# 每天早上 3:30 執行打卡任務
schedule.every().day.at("04:08").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
