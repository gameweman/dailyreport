#!/usr/bin/env python3
"""
每天获取笑话并通过邮件发送
"""

import os
import smtplib
import requests
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 中文冷笑话库
COLD_JOKES = [
    {"setup": "为什么小明从不写错别字？", "punchline": "因为他用的是橡皮。"},
    {"setup": "一只青蛙掉进了井里，怎么办？", "punchline": "等它跳出来啊，要不怎么叫井底之蛙。"},
    {"setup": "什么东西越洗越脏？", "punchline": "水。"},
    {"setup": "有一个人走在沙漠里，没有水，没有食物，最后死了，为什么？", "punchline": "因为他没有翅膀。"},
    {"setup": "今天天气真好，你看天上有几朵云？", "punchline": "我看不见，我闭眼睛了。"},
    {"setup": "什么时候1+1不等于2？", "punchline": "一加一等于二，不在什么时候。"},
    {"setup": "怎样让一只大象从冰箱里出来？", "punchline": "打开冰箱门就行了。"},
    {"setup": "怎样让一只长颈鹿进入冰箱？", "punchline": "先把大象赶出来。"},
    {"setup": "为什么小红从不去动物园？", "punchline": "因为所有的动物都已经死在她的作文里了。"},
    {"setup": "什么是黑色的，白色的，红色的？", "punchline": "一只斑马掉进了番茄酱里。"},
]

def fetch_jokes(count=20):
    """从API获取英文笑话"""
    jokes = []
    try:
        for i in range(count):
            response = requests.get('https://official-joke-api.appspot.com/random_joke', timeout=5)
            if response.status_code == 200:
                joke_data = response.json()
                jokes.append({
                    'type': joke_data.get('type', 'general'),
                    'setup': joke_data.get('setup', ''),
                    'punchline': joke_data.get('punchline', '')
                })
    except Exception as e:
        print(f"获取笑话出错: {e}")
    
    return jokes

def format_report(english_jokes, cold_jokes):
    """将笑话格式化为邮件报告"""
    date_str = datetime.now().strftime('%Y年%m月%d日')
    
    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; line-height: 1.8; color: #333; }}
            .container {{ max-width: 700px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #FF6B6B; color: white; padding: 25px; text-align: center; border-radius: 8px; margin-bottom: 20px; }}
            .header h1 {{ margin: 0; font-size: 28px; }}
            .section-title {{ background-color: #FFE66D; color: #333; padding: 12px 15px; margin-top: 25px; margin-bottom: 10px; border-radius: 5px; font-weight: bold; font-size: 16px; }}
            .joke {{ background-color: #f9f9f9; padding: 15px; margin: 8px 0; border-left: 5px solid #4CAF50; border-radius: 3px; }}
            .joke-number {{ color: #FF6B6B; font-weight: bold; font-size: 14px; }}
            .setup {{ font-weight: bold; color: #2196F3; margin: 8px 0; }}
            .punchline {{ margin-top: 8px; color: #555; font-style: italic; padding-left: 15px; border-left: 2px dashed #ccc; }}
            .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 30px; padding-top: 15px; border-top: 1px solid #eee; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>😄 每日笑话报告 😄</h1>
                <p>{date_str}</p>
                <p style="font-size: 14px; margin: 5px 0;">共30条笑话，让你笑得没烦恼！</p>
            </div>
            
            <div class="section-title">🌍 国际笑话（20条）</div>
    """
    
    for i, joke in enumerate(english_jokes, 1):
        html_content += f"""
            <div class="joke">
                <span class="joke-number">第 {i} 条</span>
                <div class="setup">{joke['setup']}</div>
                <div class="punchline">{joke['punchline']}</div>
            </div>
        """
    
    html_content += f"""
            <div class="section-title">🇨🇳 中文冷笑话（10条）</div>
    """
    
    for i, joke in enumerate(cold_jokes, 1):
        html_content += f"""
            <div class="joke">
                <span class="joke-number">第 {20 + i} 条</span>
                <div class="setup">{joke['setup']}</div>
                <div class="punchline">{joke['punchline']}</div>
            </div>
        """
    
    html_content += """
            <div class="footer">
                <p>✨ 这是由自动化机器人生成的每日笑话报告 ✨</p>
                <p>希望这些笑话能给你带来快乐！😊</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

def send_email(recipient, subject, html_content):
    """使用SMTP发送邮件"""
    sender = "noreply@github.com"
    password = os.getenv('SMTP_PASSWORD')
    
    if not password:
        print("错误：EMAIL_PASSWORD未在secrets中设置")
        return False
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient
        
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        # Outlook SMTP
        with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        
        print(f"邮件已成功发送到 {recipient}")
        return True
        
    except Exception as e:
        print(f"发送邮件出错: {e}")
        return False

def main():
    email = os.getenv('EMAIL_ADDRESS')
    
    print("正在获取20条国际笑话...")
    english_jokes = fetch_jokes(20)
    
    if not english_jokes:
        print("无法获取笑话，将使用默认笑话")
        english_jokes = []
    
    print(f"成功获取 {len(english_jokes)} 条笑话")
    print(f"已准备 {len(COLD_JOKES)} 条中文冷笑话")
    
    date_str = datetime.now().strftime('%Y年%m月%d日')
    subject = f"每日笑话报告 - {date_str}"
    
    html_content = format_report(english_jokes, COLD_JOKES)
    
    if email:
        print(f"正在发送报告到 {email}...")
        send_email(email, subject, html_content)
    else:
        print("EMAIL_ADDRESS未设置")
        print(html_content)

if __name__ == '__main__':
    main()
