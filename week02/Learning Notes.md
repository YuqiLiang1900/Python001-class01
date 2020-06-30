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

