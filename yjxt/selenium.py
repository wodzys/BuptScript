from selenium import webdriver
import time
import re
cc=webdriver.PhantomJS()
#身份认证，一次运行只需要运行一次
cc.get('http://auth.bupt.edu.cn/authserver/login?service=http%3a%2f%2fyjxt.bupt.edu.cn%2fULogin.aspx')
uname=cc.find_element_by_xpath('//*[@id="username"]')
uname.clear()
uname.send_keys('*********')
passwd=cc.find_element_by_xpath('//*[@id="password"]')
passwd.clear()
passwd.send_keys('*********')
cc.find_element_by_xpath('//*[@id="casLoginForm"]/input[4]').click()
xuankeurl='http://yjxt.bupt.edu.cn/Gstudent/Course/PlanCourseOnlineSel.aspx?EID=9kWb0OKGTBF2KzmBt5QNDZLXYu1Fldi6xwxV6Yb1wPA1TrsnKBRXgg==&UID=2016111552'
delaylist=[u'班级已全选满',u'选课未开放',u'选课已结束']
cc.get(xuankeurl)
wantedcourse=cc.find_element_by_xpath('//*[@id="contentParent_dgData_hykFull_42"]')
restr=wantedcourse.get_attribute('onclick')
jumpurl=(re.findall("classFull\('\?(.+)','classFull'\);",restr))[0]
while True:
    cc.get(xuankeurl)
    wantedcourse=cc.find_element_by_xpath('//*[@id="contentParent_dgData_hykFull_42"]')
    if wantedcourse.text in delaylist:
        print(wantedcourse.text)
        time.sleep(5)
        pass
    else :
        cc.get('http://yjxt.bupt.edu.cn/Gstudent/Course/PlanClassSelFull.aspx?'+jumpurl)
        print(cc.page_source)
        break;
