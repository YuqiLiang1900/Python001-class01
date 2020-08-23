# Learning Notes for Week09

zip

为啥我们用for迭代就不用写 list() 的原因，是for能迭代生成器，所以用不着list(), 外面套一个list()基本上是因为我们想看它到底长啥样，以及需要对其进行增减元素的时候，对嘛？

以及需要对其进行增减元素的时候，这个时候已经是对转换好的 list 进程操作了，已经不是对原来的 zip() 返回值进行操作

![image-20200818144108974](/Users/lei/Library/Application Support/typora-user-images/image-20200818144108974.png)



![image-20200818144707765](/Users/lei/Library/Application Support/typora-user-images/image-20200818144707765.png)

*args 和 ** kwargs

![image-20200821134749963](/Users/lei/Library/Application Support/typora-user-images/image-20200821134749963.png)

![image-20200821134550861](/Users/lei/Library/Application Support/typora-user-images/image-20200821134550861.png)

我也不知道为啥第一个参数叫 self，但没事，第一个位置参数传啥都行。

如果是 `def print(self, *args, **kwargs, sep = ' ', ...)` 应该就可以？===== **这个定义语法是错的，`**kwargs` 必须放到最后。

不过现在 3.8 新加了一个 / 只传位置参数。

![image-20200821134658549](/Users/lei/Library/Application Support/typora-user-images/image-20200821134658549.png)

![image-20200821134717924](/Users/lei/Library/Application Support/typora-user-images/image-20200821134717924.png)

![image-20200821135010557](/Users/lei/Library/Application Support/typora-user-images/image-20200821135010557.png)

Conf

```python
# urls.py
from functools import partial

from django.urls import path, re_path, register_converter
from . import views, converters

register_converter(converters.IntConverter, 'myint')
register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatterns = [
  path('', views.index),
  re_path('<int:year>', views.year), # 只接收整数，其他类型返回404
  path('<int:year>/<str:name>', views.name).
  # path('<myint:year>', views.year), # 自定义过滤器
  path('books', views.books),
  path('test1', views.test1),
  path('test2', views.test2)
]
```

查看Django源码：

 ```python
# lib - python3.7 - site-package - django - urls - conf.py

path = partial(_path, Pattern=RoutePattern)
re_path = partial(_path, Pattern=RegexPattern)

def partial(func, *args, **keywords):
  def newfunc(*fargs, **fkeywords):
    newkeywords = keywords.copy()
    newkeywords.update(fkeywords)
    return func(*args, *fargs, **newkeywords)
  newfunc.func = func
  newfunc.args = args
  newfunc.keywords = keywords
  return newfunc
 ```

Partial 偏函数的作用：

函数实现的功能越强大，传进去的函数也就越多越复杂。有时候我们传递的参数，其中有一部分在A场景下能使用，B场景中希望大部分的参数是默认固定下来的，我只传关键的这些参数就可以了。在这种情况，针对不同的场景可能还要分别编写不同的函数，但是如果功能大部分相同，就写一个函数即可。如，在A场景下，我这三个参数都要传进去，这个函数才能正常运行，得到我们想要的结果。B场景下，只需要传递一个参数。即A场景下，我们逐个传参数，B场景下，我们用偏函数。由此，**不必要的参数就能被固定住，我们只需要传必要的参数**。path 和 re_path 正好就是我们的B场景。

![image-20200818191048064](/Users/lei/Library/Application Support/typora-user-images/image-20200818191048064.png)



![image-20200818191856981](/Users/lei/Library/Application Support/typora-user-images/image-20200818191856981.png)

![image-20200818191530142](/Users/lei/Library/Application Support/typora-user-images/image-20200818191530142.png)



## View视图

![image-20200819121922897](/Users/lei/Library/Application Support/typora-user-images/image-20200819121922897.png)



## 响应

```python
# views.py

def test1(request):
  # 已经引入了 HttpResponse
  # from django.http import HttpResponse
  response1 = HttpResponse()
  # 定义一个空白的页面，return这个页面进行追踪和调试 - F12 查看 http header 头部信息
  response2 = HttpResponse('Any Text', content_type='text/plain')
  # 用关键字参数设置响应的返回头部
  # return response1
	return response2

def test2(request):
  # 使用 HttpResponse 的子类1，比如可以用于为文本加入特定的格式
  # from django.http import JsonResponse
  response3 = JsonResponse({'foo': 'bar'}) # response.content
  response3['Age'] = 120
  # 添加头部信息还可以有这样一个方式，直接把它当成字典来用，这样就自动添加了头部的信息
  
  # 使用 HttpResponse 的子类2，没有显式指定 404
  # from django.http import HttpResponseNotFound
  response4 = HttpResponseNotFound('<h1>Page not found</h1>')
  # 返回码变成了404，而且有 <h1>Page not found</h1> 的前端信息
  # django没有实现的话，可以自己实现
  
  return response4
```

```python
class HttpResponse():
  ...
  def __repr__(self):
    return '<%(cls)s status_code=%(status_code)d%(content_type)s>' % {
      'cls': self.__class__.__name__,
      'status_code': self.status_code,
      'content_type': self._content_type_for_repr,
    }
  
class HttpResponseNotFound(HttpResponse):
  status_code = 404
```



![image-20200820142139251](/Users/lei/Library/Application Support/typora-user-images/image-20200820142139251.png)

自己去定义一些特殊的头部之后：

![image-20200820142419829](/Users/lei/Library/Application Support/typora-user-images/image-20200820142419829.png)

![image-20200820143420446](/Users/lei/Library/Application Support/typora-user-images/image-20200820143420446.png)

![image-20200820143822043](/Users/lei/Library/Application Support/typora-user-images/image-20200820143822043.png)

## 从请求到响应

![image-20200820144251581](/Users/lei/Library/Application Support/typora-user-images/image-20200820144251581.png)

* 1: WSGI 协议 通过 `manage.py` 去启动
* 2: Request Middleware 请求中间件中，一般做得最多的就是反爬虫。看看有没有 cookie，请求过来有没有特殊的头部信息的校验。有的话就放行，没有的话打入返回中间件，404 或者 418。
* 4: 视图中间件，如果没有这个视图，就打回去，404
* 6: 若是views.py 里不是直接返回的，而是需要用到数据库里的东西，则进入到6
* 7: 是 6 的扩展，叫做模型的查询管理器（就是 object）
* 9: render 直接返回一个模版，则经过了文件，没有经过模型的查询管理器去访问数据库

注意1：每一次请求，从始到终，都带着 request 请求的对象，所以我们在此间做每一次请求的判断就比较容易。Flask没有这个功能，则需要用上下文来实现这个功能。

注意2: template 不会直接就返回，而是靠 view 去中转。所以，view视图就只做两件事情：（1）进来的是HttpRequest对象， 返回正确的结果即 HttpResponse 对象（根据需求也可以扩展成该对象的子类），（2）返回错误，抛出异常，进行打印。

注意3: 无论如何，都最后经过返回的中间件进行处理，d -> e. 

注意4: 8 上下文，比如在视图操作之前，或是在model操作前后，统一地做一些事情，但我又不希望view和model之间耦合太深。上下文也还可以去判断当前运行的状态。

注意5: 以上针对的是 GET 请求，那么对于 POST 请求时：django会把上传文件放在 _file 属性里，并且只有当 content-type 是 multipart/form-data 的时候，才会有数据。

注意6：中间件一般而言是做全局性的处理。

## model 模型

### 自增主键创建

为什么自定义的 Model 要继承 models.Model

* 不需要显式定义主键
* 自动拥有查询管理器对象（`object`）
* 可以使用 ORM API 对数据库、表实现CRUD

```python
# 作品名称和作者（主演）
class Name(models.Model):
  # id 自动创建
  name = models.CharField(max_length=50)
  author = models.CharField(max_length=50)
  stars = models.CharField(max_length=5)
  
class T1(models.Model):
  id = models.BigAutoField(primary_key=True)
  n_star = models.IntegerField()
  short = models.CharField(max_length=400)
  sentiment = models.FloatField()
  
  class Meta:
    managed = False
    db_table = 't1'
    
   
```

源码：

```python
class Model(metaclass=ModelBase):
  # 创建这个类的时候，不希望用默认的__new__来创建，而是希望增加一些自己的额外功能，
  # 才会去用到这个元类功能
  def __init__(self, *args, **kwargs):
    # Alias some things as locals to avoid repeat global lookups
    cls = self.__class__
    opts = self._meta
    _setattr = setattr
    _DEFERRED = DEFERRED
    
    pre_init.send(sender=cls, args=args, kwargs=kwargs)
    
    # Set up the storage for instance state
```

相关的自增 id 信息在 ModelBase 里： 

元类必须满足

* 父类是 type
* new 魔术方法返回的必须是一个类

```python
# 与 model 类的文件位置一致
class ModelBase(type):
  """Metaclass for all models."""
  def __new__(cls, name, bases, attrs, **kwargs):
    super_new = super().__name__
    
    # Also ensure inivitialization is only perfored for subclass
    # (excluding Model class itself).
    
    parents = [b for b in bases if isinstance(b, ModelBase)]
    if not parents:
      return super_new(cls, name, bases, attrs)
    
    # Create the class
    module = attrs.pop('__module__')
    new_attrs = {'__module__': module}
    classcell = attrs.pop('__classcell__', None)
    if classcell is not None:
      new_attrs['__classcell__'] = classcell
    attr_meta = attrs.pop('Meta', None)
    
    # Pass all attrs without a (Django-specific) contribute_to_class()
    # method to type.__new__() so that they're properly initialized
    # (i.e. __set_name__()).
    
    contributable_attrs = {}
    for obj_name, obj in list(attrs.items()):
      pass
    # 创建新的类对象
    new_class = super_new(cls, name, bases, new_attrs, **kwargs)
    
    abstract = getattr(attr_meta, 'abstract', False)
    meta = attr_meta or getattr(new_class, 'Meta', None)
    base_meta = getattr(new_class, '_meta', None)
    
    app_label = None
    
    # 以上，是生成了新的类，还是空的
    
    # Look for an application configuration to attach the model to.
    app_config = apps.get_containing_app_config(module)
    
    if getattr(meta, 'app_label', None) is None:
      pass
    
    # 添加 _meta 属性
    new_class.add_to_class('_meta', Options(meta, app_label))
    if abstract:
      pass
    
    is_proxy = new_class._meta.proxy
    
    # If the model is a proxy, ensure that the base class
    # hasn't been swapped out.
    if is_proxy and base_meta and base_meta.swapped:
      raise TypeError("%s cannot proxy that swapped model '%s'." % (name, base_meta.swapped))
    
    ...
    
    # 建立自增主键，跟踪进去继续分析
    new_class._prepare()
    new_class._meta.apps.register_model(new_class._meta.app_label, new_class)
    # 创建新的类
    return new_class
  
  
 def _prepare(cls):
  """Create some methods once self._meta has been populated."""
  opts = cls._meta
  opts._prepare(cls) # Options()._prepare
  # _meta 是 Options 类的实例对象
  # 所以调用的是
  # django.db.models.options.py 下的 _prepare() 方法
  
  
# Options class -> _prepare()

class Options():
  ...
  def _prepare(self):
    ...
    if self.pk is None:
      if self.parents:
        pass
      else:
        # 自增主键
        auto = AutoField(verbose_name='ID', primary_key = True, auto_created=True)
        # 增加id字段
        model.add_to_class('id', auto)
```



### 查询管理器

![image-20200820182019435](/Users/lei/Library/Application Support/typora-user-images/image-20200820182019435.png)

通过查看源代码，研究的重点：`BaseManager.from_queryset()` 如何变成了 `BaseManagerFromQuerySet` 这个类

![image-20200820182413483](/Users/lei/Library/Application Support/typora-user-images/image-20200820182413483.png)

```python
@classmethod
def from_queryset(cls, queryset_class, class_name=None):
  if class_name is None:
    # class_name = BaseManagerFromQuerySet
    class_name = '%sFrom%s' % (cls.__name__, queryset_class.__name__)
    # 创建新的类
  return type(class_name, (cls,), {
    '_queryset_class': queryset_class,
    **cls._get_queryset_methods(queryset_class),
  })
```



## Template 模版的加载文件

在此，主要关注两个功能

* `render` 是如何找到 templates 目录的（templates 被定义于每个 application 中）
* 动态渲染模版是如何实现的

### Render 模版引擎

![image-20200820223009641](/Users/lei/Library/Application Support/typora-user-images/image-20200820223009641.png)

从 renturn 语句的内容可以看出，render 实际上是 HttpResponse 类的一个封装。

```python
def render_to_string(template_name, context=None, request=None, using=None):
  """
  Load a template and render it with a context. Return a string.
  template_name may be a string or a list of strings.
  """
  if isinstance(template_name, (list, tuple)):
    # 若是我们传进来的template名字是个字符串，则该逻辑部分不会被执行
    template = select_template(template_name, using=using)
  else:
    template = get_template(template_name, using=using)
  return template.render(context, request)
```

```python
def get_template(template_name, using=None):
  """
  Load and return a template for the given name.
  Raise TemplateDoesNotExist if no such template exists.
  """
  chain = []
  # 先去确认引擎
  engines = _engine_list(using)
  for engine in engines:
    try:
      # 若是我们如下图指定的引擎在引擎list当中，就开始对指定的引擎进行相应的处理
      return engine.get_template(template_name)
    except TemplateDoesNotExist as e:
      chain.append(e)
      
  raise TemplateDoesNotExist(template_name, chain=chain)
```

`engines = _engine_list(using)` 指的是，先调用看引擎是怎样的（下图框住的这个，打开之后是一个python的文件）。根据引擎不同，相应的处理方式也不同：

![image-20200820223805385](/Users/lei/Library/Application Support/typora-user-images/image-20200820223805385.png)

```python
def _engine_list(using=None):
  # 该方法返回后段列表，主要实现依赖于 engines
  # 它是一个 EngineHandler 类型的实例
  return engines.all() if using is None else [engines[using]]
```

![image-20200821124309543](/Users/lei/Library/Application Support/typora-user-images/image-20200821124309543.png)

*模版引擎*

```python
class EngineHandler:
  @cached_property
  def templates(self):
    self._templates = settings.TEMPLATES
    # 遍历模版后端配置
    for tpl in self._templates:
      tpl = {
        'NAME': default_name,
        'DIRS': [],
        'APP_DIRS': False,
        'OPTIONS': {},
        **tpl,
      }
    templates[tpl['NAME']] = tpl
    backend_names.append(tpl['NAME'])
    return templates
```

*加载模版文件*

![image-20200821125137911](/Users/lei/Library/Application Support/typora-user-images/image-20200821125137911.png)

## 表单

### HTML 代码

```html
<form action='result.html' method='post'>
  username:<input type='text' name='username' /><br>
  password:<input type='password' name='password' /><br>
  <input type='submit' value='登录'>
</form>
```

* <input> 指输入框
* `type='text'` 指明文显示
* `type='password'` 不会明文显示
* `type='submit'` 提交按钮
* 提交到哪儿去、用什么方式提交：`action='result.html' method='post'` 

![image-20200821130536039](/Users/lei/Library/Application Support/typora-user-images/image-20200821130536039.png)

但是实际上，密码校验肯定是要通过链接数据库才能实现的。

注意：Django 有 form 对象，这样就不用再手写大量代码了。

### 使用 Form 对象定义表单

Django有一个自动化表单功能的目的：简化开发流程

```python
# form.py
# 用 Django 代码来生成 HTML 代码
from django import forms
class LoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput, min_length=6)
```

密码校验：把不合法的数据拒绝掉，则需要请求中间件；通过了，服务器才能进行相应。

Form 其实可以写到 view 视图当中，但是建议分开，将功能单独拆出来，使得易读性强，逻辑清晰。

* `CharField()` 是标准的输入框
* 样式改成了 `PasswordInput`，并且限制了密码的最短长度。好处：输入密码的同时，就可以进行验证。

**定义好表单后，如何在 HTML 中呈现：**

```HTML
# 在 HTML 文件中，要这样去写

<p>Input your username and password</p>
<form action='/login2' method='post'>
  {% csrf_token %}
  {{ form }}
  <input type='submit' value='Login'>
</form>
```

* ` {{ form }}` 两对花括号，模版引擎引入变量。但注意，我们这里写的是 form，而非 LoginForm。所以，这里肯定还得有一个过渡。这里 LoginForm 是类，没办法把类传到模版引擎里的。

```python
# views.py 

from .form import LoginForm
from django.contrib.auth import authenticate, login

def login2(request):
  # 表单可以查看，也可以进行提交，所以就分成两个部分：post 和 get
  if request.method == 'POST':
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
      # 读取表单的返回值
      cd = login_form.cleaned_data
      user = authenticate(username=cd['username'], password=cd['password'])
      if user:
        # 登录用户
        login(request, user)
        return HttpResponse('登录成功')
      else:
        return HttpResponse('登录失败')
      
   if request.method == 'GET':
    	login_form = LoginForm()
      return render(request, 'form2.html', {'form': login_form})
      
# 之前的 login
def login(request):
  return render(request, 'form1.htnl', locals())
      
```

相应地，也要加入 urls.py 中：

```python
# urls.py

from . import views, converters

urlpatterns = [
  path('', views.index),
  path('login', views.login)
  path('login2', views.login2)
]
```

![image-20200821141611648](/Users/lei/Library/Application Support/typora-user-images/image-20200821141611648.png)

![image-20200821143523740](/Users/lei/Library/Application Support/typora-user-images/image-20200821143523740.png)

实际上反向生成的 HTML 代码如下（因为没有对 HTML 格式进行过多处理，所以最后生成出来的会比较乱一些）：

![image-20200821143550366](/Users/lei/Library/Application Support/typora-user-images/image-20200821143550366.png)

![image-20200821144833130](/Users/lei/Library/Application Support/typora-user-images/image-20200821144833130.png)

![image-20200821144820901](/Users/lei/Library/Application Support/typora-user-images/image-20200821144820901.png)

所以这个意思是，如果我们要返回重定向的内容，就必须在 urlpatterns 里所有的视图函数都添加多一个字段，就是name嘛？

* 也可以这么写 return redirect('/') 就行了，简单明了，但是不够灵活。这个如果初学还是觉得 return redirect('/') 写法更简洁，但写代码写多了，如果需求改了，维护的时候就比较痛苦了
* 首页还好，一般地址就是 '/' ，如果是其他页面，可能 URL 后期会变动，比如首页以前是 '/' 后来改成了 '/index'，就得全局搜索 return redirect('/') 换成 return redirect('/index') 
  而使用 return redirect(resolve_url('index')) 写一次永久不改

![image-20200821144809819](/Users/lei/Library/Application Support/typora-user-images/image-20200821144809819.png)

![image-20200821152140197](/Users/lei/Library/Application Support/typora-user-images/image-20200821152140197.png)



## 用户管理验证

若是没有自动化功能，需要做很多事情，包括存储用户名、对密码进行加密等。Django的用户管理验证系统，帮助我们方便注册、创建相应的数据库的表、进行用户校验、对用户会话进行了一定处理。比如，用户在请求成功之后，希望再去登录相同网站的另外一个网页，不再需要再次验证。这些在请求中间件中实现，是最合理的。

### 如何编写验证功能

```python
# views.py 

from .form import LoginForm
from django.contrib.auth import authenticate, login

def login2(request):
  # 表单可以查看，也可以进行提交，所以就分成两个部分：post 和 get
  if request.method == 'POST':
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
      # 还可以设置很多校验的条件，比如用户名必须不能是中文，或者密码不能太简单
      
      # 读取用户填写表单的返回值
      cd = login_form.cleaned_data
      
      # 把取得的用户名 cd['username'] 和取得的密码 cd['password'] 
      # 分别赋值给关键字参数 username 和 password
      # 该验证函数 authenticate() 会上数据库里面，自动去找 username 和 password 字段
      user = authenticate(username=cd['username'], password=cd['password'])
      
      # 验证不成功则为空值
      if user:
        # 若是用户验证成功，则登录用户
        login(request, user)
        # 若是用户想退出
        # logout(request, user)
        return HttpResponse('登录成功')
      else:
        return HttpResponse('登录失败')
      
   if request.method == 'GET':
    	login_form = LoginForm()
      return render(request, 'form2.html', {'form': login_form})
      
# 之前的 login
def login(request):
  return render(request, 'form1.htnl', locals())
```





### 用户注册

![image-20200821151518408](/Users/lei/Library/Application Support/typora-user-images/image-20200821151518408.png)

进入 Mysql 终端：

![image-20200821151641031](/Users/lei/Library/Application Support/typora-user-images/image-20200821151641031.png)

![image-20200821151748516](/Users/lei/Library/Application Support/typora-user-images/image-20200821151748516.png)

![image-20200821151823116](/Users/lei/Library/Application Support/typora-user-images/image-20200821151823116.png)

![image-20200821151901982](/Users/lei/Library/Application Support/typora-user-images/image-20200821151901982.png)

![image-20200821151938904](/Users/lei/Library/Application Support/typora-user-images/image-20200821151938904.png)

![image-20200821152421204](/Users/lei/Library/Application Support/typora-user-images/image-20200821152421204.png)



## Validator 后端校验层

![image-20200822142743821](/Users/lei/Library/Application Support/typora-user-images/image-20200822142743821.png)

![image-20200822142620844](/Users/lei/Library/Application Support/typora-user-images/image-20200822142620844.png)

但 django 已经把 form.is_valid 这些都写好了。



![image-20200822144033326](/Users/lei/Library/Application Support/typora-user-images/image-20200822144033326.png)



![image-20200822151235999](/Users/lei/Library/Application Support/typora-user-images/image-20200822151235999.png)



![image-20200823095236903](/Users/lei/Library/Application Support/typora-user-images/image-20200823095236903.png)

![image-20200822161924554](/Users/lei/Library/Application Support/typora-user-images/image-20200822161924554.png)



![image-20200823100152945](/Users/lei/Library/Application Support/typora-user-images/image-20200823100152945.png)



刚刚 ipython 的问题就是你先进环境的时候，mysql 密码写的是错的，你进了 ipython 环境以后才改的 settings.py

然后这次的问题是因为，即使我们没有写 Model，但是 django 有一些自己的表要创建，所以还要执行数据库迁移

![image-20200823122411247](/Users/lei/Library/Application Support/typora-user-images/image-20200823122411247.png)



![image-20200823123630557](/Users/lei/Library/Application Support/typora-user-images/image-20200823123630557.png)

![image-20200823124951764](/Users/lei/Library/Application Support/typora-user-images/image-20200823124951764.png)





![image-20200823124937943](/Users/lei/Library/Application Support/typora-user-images/image-20200823124937943.png)

![image-20200823125135095](/Users/lei/Library/Application Support/typora-user-images/image-20200823125135095.png)