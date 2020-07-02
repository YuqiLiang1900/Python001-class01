# Learning Notes for Week 02

## Objective for Week 02
Further understanding of the web-scraping framework Scrapy

## Knowledge Tree
* Handling Exception Errors
* PyMySQL: Saving Data to a Database
* Avoid being detected by the web server
    * HTTP Header Info: User-agent, Referer
    * Selenium and Webdriver
    * Captcha
* Middleware
   * 下载中间件 & 系统代理IP
   * 自定义中间件 & 随机代理IP

## Handling Exception Errors

One of the big issues with Selenium is that if something doesn’t exist on the page, it freaks out and throws an error. For example, if I try to find #dinosaur-park and it isn’t there, I get a NoSuchElementException and my code stops working.

```python
driver.find_element_by_id('dinosaur-park')
>>> NoSuchElementException: Message: no such element: Unable to locate element: {"metho d":"id","selector":"dinosaur-park"}
(Session info: chrome=67.0.3396.79)
(Driver info: chromedriver=2.38.552518 (183d19265345f54ce39cbb94cf81ba5f15905011),p latform=Mac OS X 10.12.6 x86_64)
```

To get around that, we need to tell Python “hey, try to do this, but if it doesn’t work, that’s ok!” We can accomplish this by using try and except.

```python
try: 
  driver.find_element_by_id('dinosaur-park')
except:
  print("Couldn't find it.")
```

The part under try is run, and if it throws an error... we just ignore it and skip down to except ! This is very useful for clicking “next” buttons. When you get to the last page, there’s no ‘next’
button, and you get an error.


## PyMySQL: Saving Data to a Database

Note: in later courses, we will introduce an easier way ORM.

Sqlite 和 mysql 是同一个级别，都叫数据库软件。图形界面的软件是管理工具，是用来管理数据库的，mysql 和 sqlite 都有各自的管理软件，有些管理软件也可以同时管理 mysql 和 sqlite。

用命令行和管理软件都行，想练 sql 语句的功底可以直接终端操作，管理软件最好安装一个，在数据库中数据量大的时候方便你查看，能够提高调试效率。再说安装图形管理工具也不影响你使用命令操作数据库。

本周最大的坑之一在于 mysql 在安装之后的初始化。按照老师的 mysql -u root -p 以及 mysql.server start 均报错： ERROR! The server quit without updating PID file (/usr/local/mysql/data/liangleis-MacBook-Pro.local.pid).

解决方案：https://medium.com/@jainakansha/installing-and-running-mysql-on-macos-with-errors-resolved-70ef53e3b5b9 本篇博文拯救了我，虽然中途也出现了未曾预料的问题，但是解决方法是，点击initialize mysql，点击进入设置密码。

![mysql interface](https://miro.medium.com/max/1330/1*7mHa3fkUyNeAQtTX8xP7ig.png)

The general process of connecting Python to MySQL via Pymysql:
* Connect to the database (by initializing a pymysql.connect object)
* Get access to a cursor 
  * with connection.cursor() as cursor:
  * execute the CRUD operation
  * connection is not autocommit by default. So you must commit to save your changes (by connection.commit())
  * close the cursor
* connection.close()

A typical example of using Pymysql:

```python
import pymysql

# /usr/local/mysql/suport-files/mysql.server

# 数据库连接信息
df_info = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'rootroot',
    'db': 'test',
    'charset': 'utf8mb4' # 考虑字符乱码问题，mb4指也支持emoji表情
}

# 需要使用的SQL CRUD语句
# select 1 返回的肯定是1
# version（）值得是mysql的当前版本
sqls = ['select 1', 'select VERSION()']

result = []

class ConnDB(object):
    def __init__(self, db_info, sqls):
        super().__init__()
        self.host = db_info['host']
        self.port = db_info['port']
        self.user = db_info['user']
        self.password = db_info['password']
        self.db = db_info['db']
        self.sqls = sqls

    def run(self):
        conn = pymysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password,
            db = self.db
        )

        # 游标建立的时候就开启了一个隐形的事务 => 后面出现的所有的异常，都可以进行回滚（rollback）
        cur = conn.cursor()
        
        try:
            for command in self.sqls:
                cur.execute(command)
                result.append(cur.fetchone()) # 把游标执行的第一条结果输进去
            # 关闭游标
            cur.close()
            conn.commit()
        except:
            # 在try的语句块中，若是Mysql的语句操作出现异常，则同步进行回滚操作
            conn.rollback()
            
        # 执行批量插入操作
        # values = [(id, 'testuser'+str(id)) for id in range(4, 21)]
        # cur.executemany['INSERT INTO' + TABLE_NAME +' values(%s,%s)', values]
            
        # 关闭数据库连接
        conn.close()
        
if __name__ == '__main__':
    db = ConnDB(df_info, sqls)
    db.run()
    print(result)
```

Tips regarding the connections of databasse:
* Reuse the existing connection if possible. Do not create a new connection for every simple CRUD operation.
* The resource of database connections is previous. Close the connection whenever we have finished the queries. 

Some helpful resources
* 爬虫数据存储实例: https://github.com/yanceyblog/scrapy-mysql
* Pymysql 增删查改实例：https://www.cnblogs.com/woider/p/5926744.html
* A few tips and tricks about mysql in Navicate: https://www.navicat.com/en/company/aboutus/blog/1051-a-few-mysql-tips-and-tricks
* Python 3 进阶 —— 使用 PyMySQL 操作 MySQL: https://shockerli.net/post/python3-pymysql/
* Python+MySQL数据库操作（PyMySQL）: https://www.yiibai.com/python/python_database_access.html
* Python中操作mysql的pymysql模块详解: https://www.cnblogs.com/wt11/p/6141225.html
* Crawl Jingdong's mobile phone product data | selenium | Crawler Detailed: https://www.programmersought.com/article/75503988047/
* Mysql| 命令行模式访问操作mysql数据库.: https://blog.csdn.net/u011479200/article/details/78511073
* Python3 MySQL 数据库连接 - PyMySQL 驱动: https://www.runoob.com/python3/python3-mysql.html
* scrapy爬虫系列：利用pymysql操作mysql数据库： https://newsn.net/say/scrapy-pymysql.html


## Avoid being detected by the web server

反爬虫文献：https://segmentfault.com/a/1190000005840672

### HTTP Header Info: User-agent, Referer

We can use a random browser header to simulate the requests from a broswer. 

A more strict way to constrain from the perspective of the website: asking to log in. The cookies in the request to a web server contains such a information.

#### Random user-agent

```python
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False) 
# 在网络当中请求一些目前常用的浏览器
# 不去进行ssl验证，否则会经常下载失败，导致请求的IP被封掉。这也让浏览器去请求信息返回更快。

# Simulate different broswers
print('Chrome broswer: '.format(ua.chrome))
print(ua.safari)
print(ua.ie)

# return headers
print('Random broswer: '.format(ua.random))
```

#### Referer

指是从哪个链接里跳转过来的。有些网站会验证你的 user-agent, host, and referer.

有些网站也会增加自己的一些参数：e.g. douban.com - headers: x-client-data


### Cookie 模拟登录，解决反爬虫

对于大部分网站而言，直接复制cookie没有问题。但是对于大规模爬虫来说，每次手动复制的话会稍显繁琐。因为cookie有有效期，几小时/24小时。若是爬虫7/24h运行，则还
需要凌晨爬起来再改cookie。

因此，需要模拟登录 =》 涉及到另一个http另外一个基础的概念。
* get：在浏览器页面正常发起请求。直接将网页地址直接粘贴在浏览器的方式是get方式。
* post：

```python
# http get method
import requests
r = requests.get('https://github.com')
r.status_code
r.headers['content-type']
# r.text
r.encoding
# r.json()

# http post method
r = requests.post('http://httpbin.org/post', data={'key': 'value'})
r.json() # 若是post成功，请求完之后会有返回值，并且将其进行json化处理。
```

Post和cookie之间的关系：产生cookie是需要用户名和密码登录的，但是一般用户名和密码都是需要保密的，所以希望不要在浏览器上明文显示密码。客户端也会通过加密的机制，返回进行加密的用户名和密码，也是客户端一部分的cookie保留了下来。

```python
import requests

# 在同一个 session 实例发出的所有请求之间保持 cookie
# 更显式的指定，要用一个会话来去让上下两次连接都由同一个会话发起。这样的话，会在所有的请求之间来去保存好我们的cookie。
s = requests.Session()

# key（用户名）: sessioncookie, value（密码）: 123456789 从而模拟post的方式
s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
r = s.get('http://httpbin.org/cookies')

print(r.text)
# '{'cookies': {'sessioncookie': '123456789'}}'
# 实际上会加密保存，cookie保存用户名、密码、cookie保存的有效期。到期之后，用户需要再次登录。

# 会话可以使用上下文管理器
with requests.Session() as s:
   s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
```

注意：Requests 默认使用了 Session 功能。

Calling requests.request in turn creates a Session. If you are making multiple requests to the same endpoint you are better to use a session since it will hold open the TCP session between connections, keep a cookie jar and also remember any preferences for each request.

把post模拟登录都放在Scrapy的start_requests. 因为start_requests只会先发送一次请求，正好在此处登录用户名和密码，获得cookie。

```python

import time
import requests
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)
headers = {
    'User-Agent': ua.random,
    'Referer': 'https://accounts.douban.com/passport/login_popup?login_source=annoy' # 从浏览器中复制过来的。
}

s = requests.Session()

# 会话对象：在同一个 Session 实例发出的所有请求之间保持 cookie。
# 期间，使用 urllib3 的 connection pooling 功能。
# 连接池：当你去发起连接的时候，就从池子当中选择一个较为空闲的连接进行发起。
# 向同一主机发送多个请求，底层的TCP连接将会被重用，从而带来显著的性能提升。

login_url = 'https://accounts.douban.com/j/mobile/login/basic'

form_data = {
    'ck': '',
    'name': '15055495@qq.com',
    'password': 'test123test456',
    'remember': 'false',
    'ticket': ''
}

response = s.post(login_url, data=form_data, headers=headers)

# 注意：因为我们没有任何输出，所以也不知道登录成功之后会是怎么样。于是，可以：
# print(response.text()) # TypeError: 'str' object is not callable
print(response) # <Response [200]>
print(reponse.text) # {"status":"failed","message":"parameter_missing","description":"参数缺失","payload":{}}


# 或是：登录后可以进行后续的请求，因为拿到cookies了：
# url2 = 'https://accounts.douban.com/passport/setting'

# response2 = s.get(url2, headers=headers)
# 可以用新的session再去做请求：
# response3 = newsession.get(url3, headers=headers, cookies=s.cookies)

# 将请求的登录信息进行保存
# with open('profile.html', 'w+') as f:
#     f.write(response2.text)

```

注意：post的请求可能返回的结果有
* 405: 没有指定user-agent
* 参数非法：返回浏览器去查看 - header - form data，发现 ck 和 remember ticket 没提交。因此，request要提交完整。

### Some helpful tutorials about cookie 模拟登录：
* cookie模拟登陆 https://www.jianshu.com/p/6db4f48390d5
* 超星刷课：https://github.com/sxwxs/chaoxing_shuake/blob/master/main.py
* python网课自动刷课程序-------selenium+chromedriver: https://www.lagou.com/lgeduarticle/36714.html
* python+selenium实现自动抢票: https://www.imooc.com/article/263824
* 通过selenium+pymysql抓取民政部区号并存入数据库中: https://www.jianshu.com/p/09495554fd46
* Python+Selenium(+pymysql)实现自动听取慕课课程: https://blog.csdn.net/ZZPHOENIX/article/details/83245692

## Selenium and Webdriver

使用 requests 可以去模拟浏览器行为，并获取cookie信息，并且进行正常登录。但有些时候，页面是经过 JavaScript 做了一些加密处理，或者有时页面中获取不到我们想要去请求的 URL。因此，Selenium and Webdriver 可以让 Python 模拟浏览器的点击行为，如填了用户名和密码，并点击登录；登录之后也能拿到cookie，并且将其复制出来。Python 去模拟这个行为的时候，用到的是 webdriver 功能。

对于简单的登录，可以直接向登录接口 POST 数据；复杂些的登录，直接用带 Cookie 的请求也可以破解。但是 Cookie 那么长一串，还要将其转变为字典格式，非常麻烦。因此，有一种办法应运而生，可以和平时一样只输入账号和密码就能登录：

Selenium 是一个 web 自动化测试工具，必须和浏览器配合使用。由于它可以模仿用户的真实操作，所以它可以用来解决 JavaScript 渲染问题，也可以解决登录问题。

老师在05讲的三个代码文件：

1. 豆瓣网模拟登录

```python
from selenium import webdriver
import time

try:
    browser = webdriver.Chrome()
    # 需要安装 Chrome driver，和本机浏览器版本保持一致
    # http://chromedriver.storage.googleapis.com/index.html

    browser.get('https://www.douban.com')
    time.sleep(1)

    browser.switch_to_frame(browser.find_elements_by_tag_name('iframe')[0])
    # 以下三种方法都可以：
    # btm1 = browser.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]')
    btm1 = browser.find_element_by_xpath("//li[@class='account-tab-account']")
    # btm1 = browser.find_element_by_xpath("//div[@class='account-body-tabs']//li[@class='account-tab-account']")
    print(btm1) # []
    print(type(btm1)) # <class 'list'>
    btm1.click()

    browser.find_element_by_xpath("//*[@id='username']").send_keys('15055495@qq.com')
    browser.find_element_by_id("password").send_keys('test123test456')
    time.sleep(1)
    browser.find_element_by_xpath("//a[contains(@class, 'btn-account')]").click()

    cookies = browser.get_cookies()
    print(cookies)
    time.sleep(3)
    
except Exception as e:
    print(e)

finally:
    browser.close()
    
>>> DeprecationWarning: use driver.switch_to.frame instead
  browser.switch_to_frame(browser.find_elements_by_tag_name('iframe')[0])
<selenium.webdriver.remote.webelement.WebElement (session="9c4a4c7c05f61aa471cfcf2e10df1181", element="2f14ca37-3adf-4c73-b54c-89c04e564ddb")>
<class 'selenium.webdriver.remote.webelement.WebElement'>
[{'domain': '.douban.com', 'expiry': 1593609928, 'httpOnly': False, 'name': '__utmt', 'path': '/', 'secure': False, 'value': '1'}, {'domain': '.douban.com', 'expiry': 1609377328, 'httpOnly': False, 'name': '__utmz', 'path': '/', 'secure': False, 'value': '30149280.1593609328.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'}, {'domain': '.douban.com', 'httpOnly': False, 'name': '__utmc', 'path': '/', 'secure': False, 'value': '30149280'}, {'domain': '.douban.com', 'expiry': 1593611128, 'httpOnly': False, 'name': '__utmb', 'path': '/', 'secure': False, 'value': '30149280.1.10.1593609328'}, {'domain': '.douban.com', 'expiry': 1656681328, 'httpOnly': False, 'name': '__utma', 'path': '/', 'secure': False, 'value': '30149280.880660377.1593609328.1593609328.1593609328.1'}, {'domain': '.douban.com', 'expiry': 1625145325, 'httpOnly': False, 'name': 'll', 'path': '/', 'secure': False, 'value': '"108165"'}, {'domain': 'accounts.douban.com', 'httpOnly': False, 'name': 'login_start_time', 'path': '/', 'secure': False, 'value': '1593609328126'}, {'domain': 'accounts.douban.com', 'httpOnly': False, 'name': 'apiKey', 'path': '/', 'secure': False, 'value': ''}, {'domain': '.douban.com', 'expiry': 1625145325, 'httpOnly': False, 'name': 'bid', 'path': '/', 'secure': False, 'value': 'LXrYkmpVegg'}]
```

1.2 类似的作业：使用 requests 或 Selenium 模拟登录石墨文档 https://shimo.im

```python
from selenium import webdriver
import time

try:
    browser = webdriver.Chrome()
    time.sleep(1)

    browser.get('https://shimo.im')
    login_btn = browser.find_element_by_xpath("//button[@class='login-button btn_hover_style_8']")
    login_btn.click()

    browser.find_element_by_xpath("//input[@name='mobileOrEmail']").send_keys("356545057@qq.com")
    browser.find_element_by_xpath("//input[@type='password']").send_keys("test123test456")
    time.sleep(1)
    browser.find_element_by_xpath("//button[@class='sm-button submit sc-1n784rm-0 bcuuIb']")

    cookies = browser.get_cookies()
    print(cookies)
    time.sleep(3)

except Exception as e:
    print(e)

finally:
    browser.close()
    
>>>[{'domain': 'shimo.im', 'expiry': 1609163116, 'httpOnly': False, 'name': '_bl_uid', 'path': '/', 'secure': False, 'value': 'g2kptcth399eswwpsvp9iv9m78gz'}, {'domain': '.shimo.im', 'httpOnly': False, 'name': 'sensorsdata2015session', 'path': '/', 'secure': False, 'value': '%7B%7D'}, {'domain': '.shimo.im', 'expiry': 7900811154, 'httpOnly': False, 'name': 'sensorsdata2015jssdkcross', 'path': '/', 'secure': False, 'value': '%7B%22distinct_id%22%3A%221730a9fd4381d1-0f747438a3bf28-31617402-1128960-1730a9fd439b42%22%2C%22%24device_id%22%3A%221730a9fd4381d1-0f747438a3bf28-31617402-1128960-1730a9fd439b42%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D'}, {'domain': '.shimo.im', 'expiry': 1909045336, 'httpOnly': False, 'name': 'shimo_svc_edit', 'path': '/', 'secure': False, 'value': '8943'}, {'domain': '.shimo.im', 'expiry': 1909143917, 'httpOnly': False, 'name': 'shimo_gatedlaunch', 'path': '/', 'secure': False, 'value': '4'}, {'domain': '.shimo.im', 'expiry': 1625147154, 'httpOnly': False, 'name': 'Hm_lvt_aa63454d48fc9cc8b5bc33dbd7f35f69', 'path': '/', 'secure': False, 'value': '1593611110'}, {'domain': '.shimo.im', 'expiry': 1593644399, 'httpOnly': False, 'name': 'sajssdk_2015_cross_new_user', 'path': '/', 'secure': False, 'value': '1'}, {'domain': '.shimo.im', 'expiry': 1593614705, 'httpOnly': True, 'name': 'shimo_sid', 'path': '/', 'secure': False, 'value': 's%3AKI2vTfT3QDr3SmHjkDFHCp7FI7h3Y48O.8ZTmSGZwypLCzxy5c%2BqMxfapFXjHoYSiiUHsi1YMdrk'}, {'domain': '.shimo.im', 'httpOnly': False, 'name': 'anonymousUser', 'path': '/', 'secure': False, 'value': '-8015453060'}, {'domain': '.shimo.im', 'expiry': 1909143905, 'httpOnly': False, 'name': 'shimo_kong', 'path': '/', 'secure': False, 'value': '1'}, {'domain': '.shimo.im', 'httpOnly': False, 'name': 'deviceIdGenerateTime', 'path': '/', 'secure': False, 'value': '1593611105733'}, {'domain': '.shimo.im', 'httpOnly': False, 'name': 'deviceId', 'path': '/', 'secure': False, 'value': 'eba3c743-1bc3-421c-a4ea-0f000b052eb4'}, {'domain': '.shimo.im', 'httpOnly': False, 'name': 'Hm_lpvt_aa63454d48fc9cc8b5bc33dbd7f35f69', 'path': '/', 'secure': False, 'value': '1593611155'}, {'domain': 'shimo.im', 'httpOnly': False, 'name': '_csrf', 'path': '/', 'secure': False, 'value': '9ijVoWREDtq-w0O84KKzkxsv'}]
```


2. 通过模拟浏览器行为，爬取电影详情页的短评。

可以使用（1）scrapy （2）selenium。但是机制不一样：（1）前提是在电影详情页中给出了短评页面的链接，且不加密；（2）没有给出的情况下，则需要模拟浏览器的行为，通过点击这个短评页面的按钮，从而进入短评页面。

```python
from selenium import webdriver
import time

try:
    browser = webdriver.Chrome()

    browser.get('https://movie.douban.com/subject/1292052')
    time.sleep(1)

    # btm1 = browser.find_element_by_xpath("//*[@id='hot-comments']/a")
    btm1 = browser.find_element_by_xpath("//a[@href='comments?sort=new_score&status=P']")
    btm1.click()
    time.sleep(10)
    print(browser.page_source)

except Exception as e:
    print(e)

finally:
    browser.close()
```

3. 我们抓到了指定的数据，我们需要将数据下载下来，但是我们发现该数据非常庞大，若是直接 Python 去下载的话，可能会出现下载过于缓慢或者下载失败等问题。因此，我们在写此功能时，如下载图片/pdf，我们经常会使用分块下载这个功能。

块的大小如何指定：（1）内存 （2）网络的并发性能

```python
############# 小文件下载 #############
import requests
image_url = 'https://www.python.org/static/community_logos/python_logo-master-v3-TM.png'
r = requests.get(image_url)
# 以写入的方式打开文件，并且是以二进制的格式，因为是图片，所以希望以按顺序的方式写入。
with open('python_logo.png', 'wb') as f:
    f.writer(r.content)

############# 大文件下载 #############
# 若是文件比较大，且下载下来的文件要是先放在内存中，内存还是比较有压力的。
# 所以，为了防止内存不够用的现象出现，我们要想办法把下载的文件分块写到磁盘中。

# Iterates over the response data. When stream=True is set on the request, 
# this avoids reading the content at once into memory for large responses. 
# The chunk size is the number of bytes it should read into memory. 
# This is not necessarily the length of each item returned as decoding can take place.


import requests
file_url = 'http://python.xxx.yyy.pdf'
r = requests.get(file_url, stream=True) # 流式进行下载
with open('python.pdf', 'wb') as pdf:
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            pdf.write(chunk)
```

## 验证码识别

#### Some helpful tutorials
* 在线打码平台识别验证码 https://www.jianshu.com/p/5f94f8887a5d
* 难度更大的进阶：知乎模拟登录 + 中英文验证码识别 https://zhuanlan.zhihu.com/p/42010466

```python
import requests
import os
from PIL import Image # 对图片来做一定的处理
import pytesseract # 简单的图像识别库（from C++）

# Download the picture
session = requests.session()
img_url = 'https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=1320441599,4127074888&fm=26&gp=0.jpg'
agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
headers = {'User-Agent': agent}
r = session.get(img_url, headers=headers)

with open('cap.jpg', 'wb') as f:
    f.write(r.content)

# Open and present the file
im = Image.open('cap.jpg')
im.show()

# Grayscale image
gray = im.convert('L')
gray.save('c_gray2.jpg')
im.close()

# 二值化，让深色的能够更深，浅色的能够更浅
threshold = 100
table = []

# 设了一个中间值：256
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

print('table:', table)

# table: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
# 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
# 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

out = gray.point(table, '1')
out.save('c_th.jpg')

th = Image.open('c_th.jpg')
print(pytesseract.image_to_string(th, lang='chi_sim+eng'))
# KDQU

# 各种语言识别库 https://github.com/tesseract-ocr/tessdata
# 放到 /usr/local/Cellar/tesseract/版本/share/tessdata

```

## 中间件

想象这样一个场景，C国通过一名特工给J国传递情报，在传递的过程中，特工B要经过一个中转站，可是出来并不是特工B，而是特工M，情报的内容也遭到了篡改。

上面这个例子中的中转站，就是我们的Middleware，中文名叫做中间件。本来我们的爬虫是直接访问网站的，但是设置了中间件以后，爬虫会先跑到中间件里面做一些不可告人的勾当，然后再去访问网站。

这里的不可告人的勾当，包括但不限于：更换代理IP，更换Cookie，更换User-Aget。

注意：中间件不止一个，因此，它们的运行取决于设置的优先级。

### 下载中间件 & 系统代理IP

在爬虫开发中，更换代理IP是非常常见的情况，有时候甚至每一次访问都需要随机选择一个代理IP来进行。

原因：通过同一个IP去并发数据量请求的时候，并发的数据量太大了，导致网站把我们这个IP列为有风险的IP。从而通过反爬虫的技术，将我们的IP封掉，或者封禁几分钟。这对爬虫进度会有影响。

中间件本身是一个Python的类，更换IP是在访问每个网页之前。所以，会用到 process_request 方法，这个方法中的代码会在每次爬虫访问网页之前执行。settings.py中，后面的数字表示优先级。数字越小，优先级越高，越先执行。例如，如果你有一个更换代理的中间件，还有一个更换Cookie的中间件，那么更换代理的中间件显然是需要在更换Cookie的中间件之前运行的。如果你把这个数字设为None，那么就表示禁用这个中间件。

视频中讲解了：
* 如何开启下载中间件，并且让下载中间件支持代理IP功能。这样，我们在下载之前就能做了一个处理，可以读取代理的IP。
* 也要通过阅读分析源码，观察到底是从哪儿加载了代理IP。

### 自定义中间件 & 随机代理IP


### Some helpful resources:
* HttpProxyMiddleware: A middleware for scrapy. Used to change HTTP proxy from time to time. https://github.com/kohn/HttpProxyMiddleware
* Using a custom proxy in a Scrapy spider: https://support.scrapinghub.com/support/solutions/articles/22000219743-using-a-custom-proxy-in-a-scrapy-spider
* 爬虫实战 Scrapy爬取猫眼电影: https://www.jianshu.com/p/cca6fe9b5650



