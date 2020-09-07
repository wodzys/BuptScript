# -*- coding: utf-8 -*-
import sys
import time
import win32api, win32con
import requests
import re


status_url = 'http://10.3.8.211/index'
login_url = 'http://10.3.8.211/login'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 UBrowser/5.5.10106.5 Safari/537.36',
                        'Referer': 'http://10.3.8.211/index',
                        'Connection': 'keep-alive',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate'}

post_data = {
    'user': '2020******',  # username
    'pass': '***********'  # password
}
if __name__ == "__main__":

    if len(sys.argv) < 3:
        print('Usage: python ./AutoLogin.py **** ****')
        exit()
    else:
        post_data['user'] = sys.argv[1]
        post_data['pass'] = sys.argv[2]

    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    session = requests.session()
    detectx = session.get(status_url)
    detectx.encoding = detectx.apparent_encoding
    result1 = detectx.text

    if re.findall('登录成功', result1):
        # win32api.MessageBox(0, "登陆成功", "提醒", win32con.MB_ICONASTERISK)
        with open("log.txt", "a", encoding=detectx.apparent_encoding) as file:
            file.write(now_time + ":: 登录成功\n")
    else:
        with open("log.txt", "a", encoding=detectx.apparent_encoding) as file:
            file.write(now_time + ":: 开始登录\n")
        startLogin = session.post(login_url, data=post_data)
        startLogin.encoding = startLogin.apparent_encoding
        result1 = startLogin.text
        if re.findall('登录成功', result1):
            # win32api.MessageBox(0, "登陆成功", "提醒", win32con.MB_ICONASTERISK)
            with open("log.txt", "a", encoding=detectx.apparent_encoding) as file:
                file.write(now_time + ":: 登录成功\n")
        else:
            win32api.MessageBox(0, "登陆失败，请检查", "提醒", win32con.MB_ICONASTERISK)
            with open("log.txt", "a", encoding=detectx.apparent_encoding) as file:
                file.write(now_time + ":: 登录失败\n")
            exit()
