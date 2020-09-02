from YjxtLogin import YjxtLogin
from SelCourse import SelCourse


if __name__ == '__main__':
    USERNAME = '2019***'
    PASSWD = '*****'
    course_list = []

    login = YjxtLogin(USERNAME, PASSWD)
    login_cookies = login.authLogin()
    print(login_cookies)
    sel_course = SelCourse(USERNAME, PASSWD, login_cookies)
    sel_course.selCourse(course_list)