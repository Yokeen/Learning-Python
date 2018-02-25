#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib, urllib2
import cookielib, time
from PIL import Image
from bs4 import BeautifulSoup
import os, re
# import MySQLdb, sqlite3
# from pymongo import MongoClient

# 登录url，验证码url，验证码存储路径
login_url = "教务系统登录页面"
captcha_url = "验证码地址"
captcha_path = '验证码存储路径'
# 通过cookielib来创建opener对象，保存cookie
cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
opener.addheaders=[('User-agent','Mozilla/5.0')]
urllib2.install_opener(opener)
#用建立好的opener对象访问验证码地址，opener对象保存访问验证码后的cookie以及图片
picture = opener.open(captcha_url).read()
local = open('D:\\Script demo\\python_demo\\school_admin_blast\\photo\\image.jpg','wb')
local.write(picture)
local.close()
#利用PIL库打开图片，进行手动登录
# im = Image.open('%simage.jpg'%path)
# im.show()
# checkcode = raw_input('please input captcha：')   #手动输入验证码

#利用验证码识别工具自动输出验证码
checkcode = os.popen('verifyCaptchaconfig\\VerifyTool.exe verifyCaptchaconfig\\school.ci.png -f photo\\image.jpg').read()
data = {
    "Account":"帐号",
    "PWD":"密码",
    "CheckCode":checkcode,
    "cmdok":""
    #其他post信息
}
post_data = urllib.urlencode(data)
result = opener.open(login_url,post_data).read()
# 这里边有两种情况
# 一、是否显示完全 有的浏览器可以显示所有页面，如IE，但是有的浏览器只能显示部分页面，这里使用“xskp/jwxs_xskp_like.aspx?usermain=”判断是否显示完全
# 二、是否登录成功  如果出现“other/CheckCode.aspx” 就说明没有登陆成功
login_success_whether = result.find('other/CheckCode.aspx')
display_success_whether = result.find('xskp/jwxs_xskp_like.aspx?usermain=')
# 判断是否登陆成功
if login_success_whether != -1:
    print 'Now check username & password or Captcha....'
else:
    print 'login in successful!!!'
# 判断页面是否显示完全
if display_success_whether != -1:
    print 'Display successful!!!'
else::
    print 'Your browser have some error....'
# 利用beautifulsoup抓取页面源代码，
Soup = BeautifulSoup(result,'lxml')
name = Soup.select('#users')[0].get_text()  # 获取用户新明
info_url_demo = Soup.select('个人信息url的css selector').get('src')  # 我们获取的是个人信息的url
# 这里要说明一下，原本以为所有人的个人信息页面都是同一个url，但是打开发现每个人是不一样的
# 有一个固定的值和你入学时间相关，这个就不算了，直接把url取出来就可以了
info_url = 'www.教务系统.edu.cn' + info_url_demo
info_text = opener.open('info_url').read()
# 获取信息
Soup_text = BeautifulSoup(info_text,'lxml')
college = Soup_text.select(学院信息css selector).get_text() 
Class = Soup_text.select(班级信息css selector).get_text()
ID = Soup_text.select(身份证号css selector).get_text()
# 其实信息还有很多，家庭地址，家庭电话，家庭成员情况，个人学习及工作简历，学籍变动以及奖励处分等等等等

# 获取之后再存储到数据库或者别的，看你想怎么存储，excel或者txt文本也可以

# SQLite
# import sqlite3 
# conn = sqlite3.connect("info.db")
# c = conn.cursor()
# c.execute("CREATE TABLE IF EXISTS student_info(id INT NOT NULL AUTO_INCREMENT,name VARCHAR(20) NOT NULL,.....,PRIMARY KEY(ID))DEFAULT CHARSET=utf8")
# c.execute("INSERT INTO student_info(id,name,...) values(1,xxx,xxx)")
# conn.commit()
# conn.close()

# MySQL或者其他的都成，其实想用MongoDB来着，以前爬数据的时候用过，好久没复习又忘了....,大概也就这样子把
