# Learning Notes for Week Two

## Objective for Week Two
Further understanding of the web-scraping framework Scrapy

## Knowledge tree

### Handling Exception Errors

### PyMySQL: Saving Data to a Database

Note: in later courses, we will introduce an easier way ORM.

The general process:
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

### Avoid being detected by the web server

#### HTTP Header Info: User-agent, Referer

We can use a random browser header to simulate the requests from a broswer. 

A more strict way to constrain from the perspective of the website: asking to log in. The cookies in the request to a web server contains such a information.

##### Random user-agent

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

##### Referer

指是从哪个链接里跳转过来的。有些网站会验证你的 user-agent, host, and referer.

有些网站也会增加自己的一些参数：e.g. douban.com - headers: x-client-data


#### Cookie 模拟登录，解决反爬虫

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


