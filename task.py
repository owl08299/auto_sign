from celery import Celery
from celery.schedules import crontab
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import redis

app = Celery('tasks', broker='pyamqp://guest:guest@localhost//')

# 連接 Redis 資料庫
redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)

def perform_sign_in(username):
# 啟動 Chrome 瀏覽器，你也可以選擇其他瀏覽器
    browser = webdriver.Chrome()

    # 打開打卡網址
    url = "http://localhost:5000/"
    browser.get(url)

    # 輸入帳號和密碼
    username_input = browser.find_element("id", "UserName")  # 替換成實際的帳號欄位ID
    password_input = browser.find_element("id", "Password")  # 替換成實際的密碼欄位ID

    username_input.send_keys("M610111013")  # 替換成你的帳號
    password_input.send_keys("wilson")  # 替換成你的密碼
        

    # 點擊登錄按鈕
    login_button = browser.find_element("id", "LoginButton")  # 替換成實際的登錄按鈕ID
    login_button.click()

    # 等待一段時間，確保登錄成功（可以根據實際情況調整等待時間）
    time.sleep(3)

@app.task
def scheduled_sign_in(username):
    perform_sign_in(username)

def add_user_schedule(username, schedule_time):
    # 存儲使用者排程到 Redis
    redis_db.hset('user_schedules', username, schedule_time)
    # 創建 Celery 定時任務
    scheduled_sign_in.apply_async(args=[username], eta=crontab(hour=int(schedule_time.split(':')[0]), minute=int(schedule_time.split(':')[1])))

def remove_user_schedule(username):
    # 移除 Redis 中的使用者排程
    redis_db.hdel('user_schedules', username)

# 新增這行，定義每天早上3點30分的排程
app.conf.beat_schedule = {
    'scheduled-sign-in': {
        'task': 'tasks.scheduled_sign_in',
        'schedule': crontab(hour=3, minute=23),
    },
}
