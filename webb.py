# web.py
from flask import Flask, send_from_directory, render_template, request, redirect, url_for
from database import DBHelper
from crontab import CronTab


app = Flask(__name__)
# 存放使用者設定的排程
user_schedules = {}

db_helper = DBHelper()

# 假設這是您的有效憑據
valid_credentials = {'username': 'M610111013', 'password': 'wilson'}

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

    if entered_username == valid_credentials['username'] and entered_password == valid_credentials['password']:
        if action == '簽到':
            # 在這裡設定使用者排程
            return redirect(url_for('success', success_message='簽到成功'))
        elif action == '簽退':
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

if __name__ == '__main__':
    app.run(debug=True)

