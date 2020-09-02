
import requests
from bs4 import BeautifulSoup

class YjxtLogin:
    def __init__(self, uname, pwd):
        self.uname = uname
        self.pwd = pwd

    def getAuthUrl(self):
        url = 'http://yjxt.bupt.edu.cn/'
        html = requests.get(url, allow_redirects=False)
        soup = BeautifulSoup(html.text,'lxml')
        url = soup.find_all('a')[0]['href']
        return url

    def getAuthParm(self, auth_url):
        post_parm = {}
        html = requests.get(auth_url)
        soup = BeautifulSoup(html.text,'lxml')
        parms = soup.findAll('input', {'type': 'hidden'})
        for parm in parms:
            post_parm[parm.attrs['name']] = parm.attrs['value']
        return html.cookies, post_parm
    
    def authLogin(self):
        auth_url = self.getAuthUrl()
        auth_cookies, auth_parms = self.getAuthParm(auth_url)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'Referer': auth_url,
            'Cookie': 'JSESSIONID=' + auth_cookies['JSESSIONID']
        }
        post_data = {
            'lt': auth_parms['lt'],
            'username': self.uname,
            'password': self.pwd,
            'execution': auth_parms['execution'],
            '_eventId': 'submit',
            'rmShown': '1'
        }
        res = requests.post(auth_url, data=post_data, headers=headers)
        return res.history[1].cookies