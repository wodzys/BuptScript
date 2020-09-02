import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import browsercookie
import threading

import smtplib
from email.mime.text import MIMEText
from email.header import Header

from functools import reduce

browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
UID = '2018111599'     # 学号
PASS = '**********'   # 教务系统密码
COOKIE = ''
pre_score_num = 0      #前一次出成绩课程的数目
post_score_num = 0     #后一次出成绩课程的数目
pre_scores = []        #前一次出的成绩
post_scores = []       #后一次出的成绩
new_content = []       #新出的成绩

# 定义成绩类
class score():
    def __init__(self, number, name, credit, final_exam, total):
        self.number = number
        self.name = name
        self.credit = credit
        self.final_exam = final_exam
        self.total = total

    def detail(self):
        return ('课程编号：%s  课程名称： %s  学分：%s  期末: %s  综合成绩：%s' % 
                (self.number, self.name, self.credit, self.final_exam, self.total))


# 定义邮件类
class Mail():
    def __init__(self, mail_host, mail_user, mail_pass, sender, receivers, 
        mail_content, send_from, send_to, subject):
        self.mail_host = mail_host
        self.mail_user = mail_user
        self.mail_pass = mail_pass
        self.sender = sender
        self.receivers = receivers
        self.mail_content = mail_content
        self.send_from = send_from
        self.send_to = send_to
        self.subject = subject

    def send_mail(self):
        message = MIMEText(self.mail_content, 'plain', 'utf-8')
        message['From'] = self.sender
        message['To'] = self.send_to
        message['Subject'] = Header(self.subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.mail_host, 25)
            smtpObj.login(self.mail_user, self.mail_pass)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            print('邮件发送成功')
        except smtplib.SMTPException:
            print('Error: 无法发送邮件')   


# 模拟浏览器登陆教务系统
def login():
    try:
        browser.get('http://yjxt.bupt.edu.cn')
        input1 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#username'))
        )
        input2 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#password'))
        )
        submit =wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#casLoginForm > input.btnsubmit.btn.btn-primary.btn-lg'))
        )
        input1.send_keys(UID)
        input2.send_keys(PASS)
        submit.click()
        
        cookie_list = browser.get_cookies()
        global COOKIE
        for cookie in cookie_list:
            if cookie['name'] == 'ASP.NET_SessionId':
                COOKIE = cookie['value']
    except TimeoutException:
        return None


# 爬取网页信息
def get_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' +
                'Chrome/71.0.3578.98 Safari/537.36',
            'Cookie': 'Hm_lvt_41e71a1bb3180ffdb5c83f253d23d0c0=1543313425; ASP.NET_SessionId=' + COOKIE
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


# 分析网页内容
def parse_page(html):
    pattern = re.compile('.*?<tr.*?<td align="center">(.*?)</td>.*?<td align="center">(.*?)</td>.*?<td align="center">(.*?)'
                        + '</td>.*?<td align="center">(.*?)</td>.*?'
                        + '<td align="center">(.*?)</td>.*?<td align="center">(.*?)</td>.*?<td align="center">(.*?)</td>'
                        + '.*?<td align="center">(.*?)</td>.*?<td align="center">(.*?)</td>.*?</tr>', re.S)
    items = re.findall(pattern, str(html))
    for item in items:
        score_temp = score(item[0], item[1], item[3], item[5].strip(), item[6].strip())
        yield score_temp


# 抓取数据的定时器 10分钟刷新一次 
# 太频繁没必要且未知教务系统是否有反爬措施
def fun_timer():
    score_analysis()
    post_processing()
    global timer
    timer = threading.Timer(600, fun_timer)
    timer.start()


# 抓取数据完毕的后续操作
def post_processing():
    global pre_score_num, pre_score_num, new_content, post_scores, pre_scores
    new_content.clear()
    post_score_num = len(post_scores)
    if post_score_num is not 0:
        if pre_score_num is not post_score_num:
            new_content = [item.detail() for item in post_scores if item not in pre_scores]
            pre_scores = post_scores.copy()
            pre_score_num = post_score_num
            post_scores.clear()
            post_score_num = 0 
            content = reduce(lambda x, y: x + y + '   ', new_content)
            email_address = '18653059888@163.com'
            mail_sender = Mail('smtp.163.com', email_address, '********', email_address, [email_address], 
                content, email_address, email_address, '期末考试成绩推送')
            mail_sender.send_mail()

        else:
            post_scores.clear()
            post_score_num = 0 


# 拿数据
def score_analysis():
    url = 'http://yjxt.bupt.edu.cn/Gstudent/Course/StudentScoreQuery.aspx?EID=l3PZkHTW3Su1WxpIyiJt7xg!oXf-MKDVwRsqQS-VmXP5EIN3VGspUCQlpP97holrwbsOABGJpxw=&UID=' + UID
    html = get_page(url)
    res = parse_page(html)
    try:
        while True:
            post_scores.append(res.__next__())
    except StopIteration:
        pass


# 启动定时器       
def main():
    timer=threading.Timer(1,fun_timer)
    timer.start()

if __name__ == '__main__':
    login()
    main()