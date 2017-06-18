# encoding=utf8
import urllib
import urllib2
import cookielib
import re
import string
from BeautifulSoup import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class SDJZU_Crawler:
    # 声明相关的属性
    def __init__(self):

        self.loginUrl = 'http://urpe.sdjzu.edu.cn/loginPortalUrlForIndexLogin.portal'  # 登录的url
        self.resultUrl = 'http://jwfw1.sdjzu.edu.cn/ssfw/jwnavmenu.do?menuItemWid=1E057E24ABAB4CAFE0540010E0235690'  # 查询成绩的url
        self.cookieJar = cookielib.CookieJar()  # 初始化一个CookieJar来处理Cookie的信息
        self.postdata = urllib.urlencode({'userName': '', 'password': ''})  # 登录需要POST的数据
        self.weights = []  # 存储权重，也就是学分
        self.points = []  # 存储分数，也就是成绩
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJar))

    def sdu_init(self):
        username = raw_input('请输入学号:')  # 这里不要用input，二者区别请自行查询
        password = raw_input('请输入密码:')
        self.postdata = urllib.urlencode({'userName': username, 'password': password})  # 将用户名密码加入到POST中
        # 初始化链接并且获取cookie
        myRequest = urllib2.Request(url=self.loginUrl, data=self.postdata)  # 自定义一个请求
        result = self.opener.open(myRequest)  # 访问登录页面，获取到必须的cookie的值
        result = self.opener.open(self.resultUrl)  # 访问成绩页面，获得成绩的数据
        self.deal_data(result.read())
        self.calculate_gpa()

    # 将内容从页面源码中提取出来
    def deal_data(self, myPage):

        soup = BeautifulSoup(myPage)

        # 从title属性为有效成绩的标签中获取所有class属性为t_con的TAG(tr标签)
        trs = soup.find(attrs={"title": "有效成绩"}).findAll(attrs={"class": "t_con"})

        # 从tr标签中的td标签中获取需要的信息。下标为3，7，8的分别为课程名，学分，成绩
        for tr in trs:
            for index, td in enumerate(tr.findAll('td')):  # enumerate能在for循环中使用下标

                if index == 3:
                    print td.text
                elif index == 7:
                    self.weights.append(td.text.encode('utf8'))
                    print td.text
                elif index == 8:
                    self.points.append(td.text.encode('utf8'))
                    print td.text

            print

    # 计算绩点，如果成绩还没出来，就不算该成绩，
    def calculate_gpa(self):
        point = 0.0  # 成绩
        weight = 0.0  # 学分
        for i in range(len(self.points)):
            if self.points[i].isdigit() and (self.weights[i] != 0):
                point += string.atof(self.points[i]) * string.atof(self.weights[i])  # 成绩*学分累加求和
                weight += string.atof(self.weights[i])  # 学分累加求和

        print "绩点为："
        print point / weight  # 输出绩点 值成绩*学分累加求和 / 学分累加求和


# 调用
mySpider = SDJZU_Crawler()
mySpider.sdu_init()
