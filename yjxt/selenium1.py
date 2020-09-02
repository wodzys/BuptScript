import itchat
import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup


username = '20180000000'
password = '0000000'
lessonid = '3131100598'
itchat.auto_login()

def sendMsg(msg):
    itchat.send(u"[选课监视系统]"+msg+'\n'+time.strftime('%H:%M:%S',time.localtime(time.time())),toUserName='filehelper')
def countdown(t):
    for n in range(0,t):
        time.sleep(1)
        print("countdown:{0}".format(t-n))
def checkSource(source):
    soup = BeautifulSoup(source,'lxml')
    table = soup.table
    tr_arr = table.find_all('tr')
    for tr in tr_arr:
        tds = tr.find_all('td')
        if len(tds) == 0:
            continue
        strid = tds[0].get_text()
        strcon = tds[7].get_text()
        strid = strid.replace(' ','')
        strid = strid.replace('\n','')
        strid = strid.replace('\r','')
        strid = strid.replace('\t','')
        strcon = strcon.replace(' ','')
        strcon = strcon.replace('\n','')
        strcon = strcon.replace('\r','')
        strcon = strcon.replace('\t','')
        print(strid+strcon)
        if strid == lessonid:           
            if strcon == '选择上课班级':
                return True
    return False
    input[0].send_keys(username)

sendMsg('系统启动，监测课程'+lessonid+'中...')

def checkLessonAvailable():
    browser = webdriver.Chrome()
    browser.get('https://auth.bupt.edu.cn/authserver/login?service=http%3A%2F%2Fmy.bupt.edu.cn%2Flogin.portal')
    countdown(1)
    input = browser.find_elements_by_id('username')
    input = browser.find_elements_by_id('password')
    input[0].send_keys(password)
    input = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/form/input[4]')
    input.click()
    countdown(1)
    browser.get('http://yjxt.bupt.edu.cn')
    countdown(1)
    browser.switch_to.frame('MenuFrame')
    countdown(1)
    a = browser.find_element_by_id('tree1_2_a')
    url = a.get_attribute('href')
    while True:
        browser.get(url)
        table = browser.find_element_by_xpath('//*[@id="contentParent_UpdatePanel2"]/div')
        pagesource =table.get_attribute('innerHTML')
        #print(pagesource)
        if checkSource(pagesource) == True:
            sendMsg('老铁有课！手慢无\n'+'课程ID'+lessonid)
            print('有课')
            browser.close()
            break
        print('没有课/(ㄒoㄒ)/~~')
        countdown(30)
    sendMsg('系统关闭') 
checkLessonAvailable()