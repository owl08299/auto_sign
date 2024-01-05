import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_notification_email(name, username, action, email, ip, timestamp):
    # 收件人的郵件地址
    to_email = email

    # 你的郵件帳戶資訊
    sender_email = 'wtns6991@gmail.com'
    sender_password = 'uvoa exqq erao gshv'

    # 郵件內容
    subject = f'{name} 自助打卡完成通知 - {username}'
    body = f'使用者{name} ({username}) 您好， 貓頭鷹自助打卡系統已於 {timestamp} 為您進行 {action}，IP 位置為 {ip}。'

    # 建立郵件物件
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject

    # 將郵件內容加入郵件物件
    message.attach(MIMEText(body, 'plain'))

    try:
        # 連接 SMTP 伺服器
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            # 登入郵件帳戶
            server.login(sender_email, sender_password)
            # 發送郵件
            server.sendmail(sender_email, to_email, message.as_string())
            print('郵件通知已發送成功！')
    except Exception as e:
        print(f'郵件通知發送失敗：{e}')


