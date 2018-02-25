#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib, urllib2
import cookielib, time
from PIL import Image
from bs4 import BeautifulSoup
import chardet

# 登录url，验证码url，验证码存储路径
url = "教务系统登录页面url"
captcha_url = "验证码地址"
path = '验证码图片保存地址'
# 通过cookielib来创建opener对象，保存cookie
cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
#默认是[('User-agent', 'Python-urllib/2.7')]，稍微做一点反爬虫机制
opener.addheaders=[('User-agent','Mozilla/5.0')]
urllib2.install_opener(opener)
#用建立好的opener对象访问验证码地址，opener对象保存访问验证码后的cookie以及图片
picture = opener.open(captcha_url).read()
local = open('D:\\Script demo\\python_demo\\urllib_cookielib\\photo\\image.jpg','wb')
local.write(picture)
local.close()
#利用PIL库打开图片，进行手动登录
im = Image.open('%simage.jpg'%path)
im.show()
checkcode = raw_input('please input captcha：')   #手动输入验证码
data = {
	#其他post的相关数据
    "Account":"",
    "PWD":"",
    "CheckCode":checkcode,
    "cmdok":""
}
post_data = urllib.urlencode(data)
result = opener.open(url,post_data).read()
soup = BeautifulSoup(result,'lxml')
name = soup.select('#users')[0].get_text()   #这里只是抓取了登陆之后页面的用户名，还并没有深入抓取
print name