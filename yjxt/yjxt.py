# # -*- coding:utf-8 -*-

# import re
# import requests
# from bs4 import BeautifulSoup

# USERNAME = '***'
# PASSWD = '****'

# yjxt_url = 'http://yjxt.bupt.edu.cn/'

# def nameislt(tag):
#     if tag.has_attr('name') and tag['name'] == 'lt':
#         return True
#     else:
#         return False


# def nameisexecution(tag):
#     if tag.has_attr('name') and tag['name'] == 'execution':
#         return True
#     else:
#         return False


# if __name__ == '__main__':
#     yjxt_html = requests.get(yjxt_url, allow_redirects=False)
#     # print(yjxt_html.text)
#     # # <html><head><title>Object moved</title></head><body>
#     # # <h2>Object moved to <a href="http://auth.bupt.edu.cn/authserver/login?service=http%3a%2f%2fyjxt.bupt.edu.cn%2fULogin.aspx">here</a>.</h2>
#     # # </body></html>
#     yjxt_soup = BeautifulSoup(yjxt_html.text,'lxml')
#     auth_url = yjxt_soup.find_all('a')[0]['href']
#     # print(auth_url)
#     # # http://auth.bupt.edu.cn/authserver/login?service=http%3a%2f%2fyjxt.bupt.edu.cn%2fULogin.aspx

#     # try:
#     #     auth_html = requests.get(auth_url)
#     # except Exception as e:
#     #     print('连接超时：' + str(e))

#     auth_html = requests.get(auth_url)
#     # codestr = chardet.detect(auth_html.read())["encoding"]
#     auth_soup = BeautifulSoup(auth_html.text,'lxml')
#     lt_node = auth_soup.find(nameislt)
#     lt_str = lt_node['value']
#     exec_node = auth_soup.find(nameisexecution)
#     exec_str = exec_node['value']

#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
#         'Referer': auth_url,
#         'Cookie': 'JSESSIONID=' + auth_html.cookies['JSESSIONID']
#     }

#     post_data = {
#         'lt': lt_str,
#         'username': USERNAME,
#         'password': PASSWD,
#         'execution': exec_str,
#         '_eventId': 'submit',
#         'rmShown': '1'
#     }
#     yjxt_res = requests.post(auth_url, data=post_data, headers=headers)

#     leftmenu_url = 'http://yjxt.bupt.edu.cn/Gstudent/leftmenu.aspx?UID=' + USERNAME
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
#         'Referer': 'http://yjxt.bupt.edu.cn/Gstudent/Default.aspx?UID=' + USERNAME,
#         # 'Cookie': 'ASP.NET_SessionId=' + yjxt_res.history[1].cookies['ASP.NET_SessionId'] +'; OnlineSelXQ=32; DropDownListXqu='
#         'Cookie': 'ASP.NET_SessionId=' + yjxt_res.history[1].cookies['ASP.NET_SessionId']
#     }
#     leftmenu_res = requests.get(leftmenu_url, headers=headers)
#     # print(leftmenu_res.text)
#     patern = r'Course/PlanCourseOnlineSel.aspx\?EID=.*?=='
#     PlanCourseOnlineSel_url = 'http://yjxt.bupt.edu.cn/Gstudent/' + re.findall(re.compile(patern), leftmenu_res.text)[0] + '&UID=' + USERNAME
#     # print(url)
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
#         'Referer': leftmenu_url,
#         # 'Cookie': 'ASP.NET_SessionId=' + yjxt_res.history[1].cookies['ASP.NET_SessionId'] +'; OnlineSelXQ=32; DropDownListXqu='
#         'Cookie': 'ASP.NET_SessionId=' + yjxt_res.history[1].cookies['ASP.NET_SessionId']
#     }
#     PlanCourseOnlineSel_res = requests.get(PlanCourseOnlineSel_url, headers=headers)
#     PlanCourseTrs = BeautifulSoup(PlanCourseOnlineSel_res.text,"html5lib").find_all('tr', onmouseout="SetRowBgColor(this,false)")
#     l = {}
#     for tr in PlanCourseTrs:
#         tmp = str(tr).replace(' ', '').replace('\n', '')
#         if '正在选课' in tmp and '退选课程' not in tmp:
#             course = {}
#             pid = r'<tdalign="center"style="white-space:nowrap;">([0-9]*)</td>'
#             id = re.findall(re.compile(pid), tmp)[0]
#             purl = r'selClass\(\'([\s\S]*),\'selClass\'\)'
#             url = re.findall(re.compile(purl), tmp)[0]
#             course['url'] = 'http://yjxt.bupt.edu.cn/Gstudent/Course/PlanSelClass.aspx' + url.replace('&amp;', '&')
#             course['class'] = {}
#             l[id] = course
    
#     # for course in PlanCourseTrs:
#     #     course1 = course.find_all('td')
#     #     courseId = str(course1[0].text).replace(' ', '').replace('\n', '')
#     #     print(str(type(courseId)) + ':' + courseId)