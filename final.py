import os
from flask import Flask, render_template, request, redirect, send_from_directory, url_for
from flask_migrate import Migrate
from database import DBHelper
from crontab import CronTab
from celery import Celery
from celery.schedules import crontab
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from datetime import datetime

import time
import threading
import schedule
import csv
import socket

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# app.app_context().push()  # 重新推送上下文
    

# 存放使用者設定的排程
user_schedules = {}

# 假設這是您的有效憑據
valid_credentials = {
    'M610111013': {'password': 'wilson', 'name': '江韋辰'},
    '123456': {'password': '123456', 'name': '互評人'},
}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/images/<path:filename>')
def get_image(filename):
    return send_from_directory('static/images', filename)

@app.route('/login', methods=['POST'])
def login():
    entered_username = request.form.get('UserName')
    entered_password = request.form.get('Password')
    action = request.form.get('submit_btn')

    #if entered_username == valid_credentials['username'] and entered_password == valid_credentials['password']:
    if entered_username in valid_credentials and entered_password == valid_credentials[entered_username]['password']:
        if action == '簽到':
            record_schedule_success(entered_username, action)
            return redirect(url_for('success', success_message='簽到成功'))
            
        elif action == '簽退':
            record_schedule_success(entered_username, action)
            return redirect(url_for('success', success_message='簽退成功'))
    else:
        return redirect(url_for('error', error_message='帳號或密碼不正確'))
    

@app.route('/success')
def success():
    success_message = request.args.get('success_message', '')
    return render_template('success.html', success_message=success_message)

@app.route('/error')
def error():
    error_message = request.args.get('error_message', '')
    return render_template('success.html', success_message=error_message)

def perform_sign_in(username,password,action):
    # 打卡程式碼
    browser = webdriver.Chrome()

    try:
        url = "http://localhost:5000/"
        browser.get(url)

        username_input = browser.find_element("id", "UserName")
        password_input = browser.find_element("id", "Password")

        username_input.send_keys(username)
        password_input.send_keys(password)

        if action == 'signin':
            login_button = browser.find_element("id", "LoginButton")
            login_button.click()
        elif action == 'signout':
            logout_button = browser.find_element("id", "logoutbtn")
            logout_button.click()

        time.sleep(3)
        
        # if "成功" in browser.page_source:
        #     record = Record(username=username)
        #     db.session.add(record)
        #     db.session.commit()        

        # soup = BeautifulSoup(browser.page_source, 'html.parser')
        # target_text = soup.find('div', {'id': 'showloginmsg'}).find('div', {'class': 'form-group'}).text.strip()
        # print(target_text)

        # time.sleep(10)
    finally:
        browser.quit()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def record_schedule_success(username, action):
    # 在這裡添加紀錄排程成功的程式碼
    file_path = 'schedule_success_records.csv'
    
    # 檢查檔案是否存在，如果不存在就寫入標題列
    if not os.path.exists(file_path):
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["帳號", "打卡別", "IP", "時間"])
            
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([username, action, get_ip(), current_time])

def job(username, password, action):
    # 打卡任務
    perform_sign_in(username, password, action)
    # 儲存打卡紀錄
    record_schedule_success(username, action)


def schedule_job(username, password, time, action):
    # 設定排程
    schedule.every().day.at(time).do(job, username, password, action)

# 設定排程的頁面
@app.route('/set_schedule_page')
def set_schedule_page():
    return render_template('set_schedule.html')

# 處理設定排程的請求
@app.route('/set_schedule', methods=['POST'])
def set_schedule():
    username = request.form.get('username')
    password = request.form.get('password')
    time = request.form.get('time')
    action = request.form.get('action')

    # 將使用者的設定儲存到排程中
    user_schedules[username] = {'password': password,'time': time, 'action': action}

    # 設定打卡任務  
    schedule_job(username, password, time, action)

    return redirect(url_for('index'))

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    # db = SQLAlchemy(app)
    # migrate = Migrate(app, db)

    # with app.app_context():
     
    #     # 創建資料庫表格
    #     db.create_all()

    # 啟動排程執行緒
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()

    # 啟動 Flask 應用程式
    app.run(debug=True)
