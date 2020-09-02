import re
import requests
from bs4 import BeautifulSoup

class SelCourse():
    def __init__(self, uname, pwd, cookies):
        self.uname = uname
        self.pwd = pwd
        self.cookies = 'ASP.NET_SessionId=' + cookies['ASP.NET_SessionId']
        self.leftmenu_url = 'http://yjxt.bupt.edu.cn/Gstudent/leftmenu.aspx?UID=' + uname

    def getPlanCourseUrl(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'Referer': 'http://yjxt.bupt.edu.cn/Gstudent/Default.aspx?UID=' + self.uname,
            # 'Cookie': 'ASP.NET_SessionId=' + yjxt_res.history[1].cookies['ASP.NET_SessionId'] +'; OnlineSelXQ=32; DropDownListXqu='
            'Cookie': self.cookies
        }
        leftmenu_res = requests.get(self.leftmenu_url, headers=headers)
        patern = r'Course/PlanCourseOnlineSel.aspx\?EID=.*?==&UID=\d{10}'
        # url = 'http://yjxt.bupt.edu.cn/Gstudent/' + re.findall(re.compile(patern), leftmenu_res.text)[0] + '&UID=' + self.uname
        url = 'http://yjxt.bupt.edu.cn/Gstudent/' + re.findall(re.compile(patern), leftmenu_res.text)[0]
        return url
    
    def getPlanCourse(self):
        plan_course_url = self.getPlanCourseUrl()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'Referer': self.leftmenu_url,
            # 'Cookie': 'ASP.NET_SessionId=' + yjxt_res.history[1].cookies['ASP.NET_SessionId'] +'; OnlineSelXQ=32; DropDownListXqu='
            'Cookie': self.cookies
        }
        # 这里需要加一个刷新页面的if，选课未开放时刷新页面
        plan_course_res = requests.get(plan_course_url, headers=headers)
        plan_course_trs = BeautifulSoup(plan_course_res.text,"html5lib").find_all('tr', onmouseout="SetRowBgColor(this,false)")
        plan_course = {}
        for tr in plan_course_trs:
            tmp = str(tr).replace(' ', '').replace('\n', '')
            if '正在选课' in tmp and '退选课程' not in tmp:
                course = {}
                pid = r'<tdalign="center"style="white-space:nowrap;">([0-9]*)</td>'
                id = re.findall(re.compile(pid), tmp)[0]
                purl = r'selClass\(\'([\s\S]*),\'selClass\'\)'
                url = re.findall(re.compile(purl), tmp)[0]
                course['url'] = 'http://yjxt.bupt.edu.cn/Gstudent/Course/PlanSelClass.aspx' + url.replace('&amp;', '&')
                course['name'] = {}
                # course['name']用来保存课程名称
                plan_course[id] = course
        return plan_course
    
    def selCourse(self, course_list):
        plan_course = self.getPlanCourse()
        for course_id in course_list:
            class_info = plan_course[course_id]
            result = self.selClass(class_info)
        return result

    def selClass(self, class_info):
        payload = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'Referer': 'http://yjxt.bupt.edu.cn/Gstudent/Default.aspx?UID=' + self.uname,
            'Cookie': self.cookies
        }
        req = requests.get(class_info['url'], headers=headers)
        html = BeautifulSoup(req.text, features="html5lib")
        form = html.findAll('form')[0]
        payload['__VIEWSTATE'] = form.findAll('input', {'id': '__VIEWSTATE'})[0]['value']
        payload['__LASTFOCUS'] = form.findAll('input', {'id': '__LASTFOCUS'})[0]['value']
        payload['__EVENTTARGET'] = form.findAll('input', {'id': '__EVENTTARGET'})[0]['value']
        payload['__EVENTARGUMENT'] = form.findAll('input', {'id': '__EVENTARGUMENT'})[0]['value']
        payload['__VIEWSTATEGENERATOR'] = form.findAll('input', {'name': '__VIEWSTATEGENERATOR'})[0]['value']
        payload['__VIEWSTATEENCRYPTED'] = form.findAll('input', {'name': '__VIEWSTATEENCRYPTED'})[0]['value']
        payload['__EVENTVALIDATION'] = form.findAll('input', {'name': '__EVENTVALIDATION'})[0]['value']
        payload['_ASYNCPOST'] = True

        self.url = 'http://yjxt.bupt.edu.cn/Gstudent/Course/' + form['action']
        payload['ctl00$contentParent$dgData$ctl02$ImageButton1.x'] = 13
        payload['ctl00$contentParent$dgData$ctl02$ImageButton1.y'] = 8
        trs = html.findAll('tr')
        for tr in trs[3:]:
            tmp = str(tr).replace(' ', '').replace('\n', '')
            pname = r'<aclass=\"none\"href=\"javascript:void\(0\)\"id=\"contentParent_dgData_hykClass_[0-9]+[\s\S]*\">([\s\S]*)<\/a>'
            classname = re.findall(re.compile(pname), tmp)[0]
            # print(classname)
            if class_info['name'] != classname:
                continue
            else:
                btn = tr.findAll('input', {'type': 'image'})[0]['name']
                payload['ctl100$ScriptManager1'] = btn
        req = requests.post(self.url, headers=headers, data=payload)
        if 'frameElement.api.close()' in req.text:
            print("选课完成")
            return True
        else:
            print(req.text)
            return False



