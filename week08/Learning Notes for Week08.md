# Learning Notes for Week08

## 变量赋值

```python
# Question 1: whether they have different ids
a = 123
b = 123
c = a
print(id(a))
print(id(b))
print(id(c))
```

Yes, their id is identical - '4400206800'.

```python
# Question 2: what would be their values?
a = 456
print(id(a)) # 当我们为变量a去赋予不同的值的时候，它的id内存地址会发生变化。
c = 789
c = b = a
print(a, b, c)
```

Output:

```python
140212854980688
456 456 456
```

```python
# Question 3: what would be their values?
# 对列表完整进行替换，和对列表的某个元素进行替换，会产生不同的结果。
x = [1, 2, 3]
y = x
x.append(4)
print(x)
print(y)
```

Output:

```python
[1, 2, 3, 4]
[1, 2, 3, 4]
```

*判断是否为同一个对象*

```python
print(a is b)
# 底层：通过判断a和b两个变量的id是否相等
```

*判断是否拥有同一个值*

```python
print(a == b)
```

![image-20200815100949369](/Users/lei/Library/Application Support/typora-user-images/image-20200815100949369.png)

![image-20200815103826719](/Users/lei/Library/Application Support/typora-user-images/image-20200815103826719.png)

![image-20200815110949411](/Users/lei/Library/Application Support/typora-user-images/image-20200815110949411.png)



## 闭包

```python
# 内部函数对外部函数作用域里变量的引用（非全局变量），则称内部函数为闭包

def counter(start=0):
  count = [start]
  def incr():
    count[0] += 1
    return count[0]
  return incr

c1 = counter(10)

print(c1()) # output: 11
print(c1()) # output: 12
```

![image-20200812104858591](/Users/lei/Library/Application Support/typora-user-images/image-20200812104858591.png)

![image-20200812105707848](/Users/lei/Library/Application Support/typora-user-images/image-20200812105707848.png)

*第7节闭包，最后的例子里内部函数的enclosure里，如果属性变量a是数字对象，就要先声明为nonlocal才能进行加等操作，而如果是序列容器对象，为啥就不用声明nonlocal呢？*

![image-20200812111544267](/Users/lei/Library/Application Support/typora-user-images/image-20200812111544267.png)

![image-20200812111601096](/Users/lei/Library/Application Support/typora-user-images/image-20200812111601096.png)

所以这个问题的话，可否这样理解呀：

赋值即重新定义，不管是可变类型还是不可变类型，只要内函数有赋值，且等号右边的变量是在外函数，就得nonlocal申明；如果等号右边的变量是在外函数以外，就用global进行申明？

如果没有赋值操作，那么内函数遇到了这个在内函数里没有定义的变量a，就会自动向外进行查找，如果在外函数找到了，就不会报错（那如果没有在外函数找到，但是在外函数外部才有的话，就会报错。此时的解决办法，就是global a）

嗯嗯global的话，这个变量就会和函数外部的全局变量相对应，如果是nonlocal的话，就会和外函数内部、内函数外部的变量相对应。

![image-20200812111507841](/Users/lei/Library/Application Support/typora-user-images/image-20200812111507841.png)

![image-20200812111523495](/Users/lei/Library/Application Support/typora-user-images/image-20200812111523495.png)



```python
# nonlocal 访问外部函数的局部变量
# 注意start的位置，return的作用域和函数内的作用域不同

def counter2(start=0):
  def incr():
    nonlocal start
    start += 1
    return start
  return incr

c1 = counter2(5)
print(c1())
print(c2())

def counter2(start=0):
  def incr():
    start = 1
    return start
  return incr

c1 = counter2(5)
print(c1())
```





## 装饰器

Decorators allow you to define reusable building blocks that can change or extend the behavior of other functions. And they let you do that without permanently modifying the wrapped function itself. The function’s behavior changes only when it’s *decorated*.

Now what does the implementation of a simple decorator look like? In basic terms, a decorator is *a callable that takes a callable as input and returns another callable*.

**记住装饰器模板**

```python
def decorator(func):
  routes[path] = (func, methods or ['GET'])
  def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

装饰器核心就两层嵌套函数，中间闭包作用域里的变量叫自由变量。

**最外层嵌套函数是用来处理装饰器自身接收参数的**，所以它不是装饰器最核心的部分。

**面向对象编程中，属性用来保存数据的状态。类实例化以后是实例对象，实例对象随时调用自己的属性获取属性值。但是，函数中不行，函数执行完就被销毁了，内部变量就被弄丢了。所以，在嵌套函数中，闭包中的变量，也是自由变量，也能保存状态。外层函数执行完，内层函数和自由变量还在，没被销毁，所以也实现了数据状态的保存。**

咱们装饰器自由变量应该在哪里？
带参数的装饰器最外层是用来接收装饰器本身的参数的。

自由变量（闭包作用域中）用来保存状态，也只有在这里修改全局变量才有意义，最内部函数还没执行呢，修改不了  routes

![image-20200814092154535](/Users/lei/Library/Application Support/typora-user-images/image-20200814092154535.png)

![image-20200814093351563](/Users/lei/Library/Application Support/typora-user-images/image-20200814093351563.png)

若是三层装饰器的话：

（注意调用顺序）

![image-20200814094346899](/Users/lei/Library/Application Support/typora-user-images/image-20200814094346899.png)

![image-20200814095419437](/Users/lei/Library/Application Support/typora-user-images/image-20200814095419437.png)

![image-20200814095052351](/Users/lei/Library/Application Support/typora-user-images/image-20200814095052351.png)

```python
# utils.py

# TODO routes 最终效果如下
# routes = {
#     '/': (index, ['GET']),
#     '/index': (index, ['GET']),
# }

routes = {}

# TODO 需要实现一个 route 装饰器，替换原来手动构造 routes 字典的代码，让装饰器自动完成这个功能
def route(path, methods=None):
    def decorator(func):
        routes[path] = (func, methods)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 而非写在这儿：routes[path] = (func, methods)
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

```python
"""
控制器 controllers.py
"""
from todo.utils import render_template, route


# TODO 装饰器用法如下，跟 Flask 用法相同
@route('/', methods=['GET'])
def index():
    """首页视图函数"""
    return render_template('index.html')
```

```python
# server.py

def make_response(request, headers=None):
    """构造响应报文"""
    # 默认状态码为 200
    status = 200
    # 获取匹配当前请求路径的处理函数和函数所接收的请求方法
    # request.path 等于 '/' 或 '/index' 时，routes.get(request.path) 将返回 (index, ['GET'])
    route, methods = routes.get(request.path)

    # 如果请求方法不被允许，返回 405 状态码
    if request.method not in methods:
        status = 405
        data = 'Method Not Allowed'
    else:
        # 请求首页时 route 实际上就是我们在 controllers.py 中定义的 index 视图函数
        data = route()

    # 获取响应报文
    response = Response(data, headers=headers, status=status)
    response_bytes = bytes(response)
    print(f'response_bytes: {response_bytes}')

    return response_bytes
```



### Everything is Python is an object

First of all let’s understand functions in Python:

```python
def hi(name="yasoob"):
    return "hi " + name

print(hi())
# output: 'hi yasoob'

# We can even assign a function to a variable like
greet = hi
# We are not using parentheses here because we are not calling the function hi
# instead we are just putting it into the greet variable. Let's try to run this

print(greet())
# output: 'hi yasoob'

# Let's see what happens if we delete the old hi function!
del hi
print(hi())
#outputs: NameError

print(greet())
#outputs: 'hi yasoob'
```

### Defining functions within functions

So those are the basics when it comes to functions. Let’s take your knowledge one step further. In Python we can define functions inside other functions:

```python
def hi(name="yasoob"):
    print("now you are inside the hi() function")

    def greet():
        return "now you are in the greet() function"

    def welcome():
        return "now you are in the welcome() function"

    print(greet())
    print(welcome())
    print("now you are back in the hi() function")

hi()
#output:now you are inside the hi() function
#       now you are in the greet() function
#       now you are in the welcome() function
#       now you are back in the hi() function

# This shows that whenever you call hi(), greet() and welcome()
# are also called. However the greet() and welcome() functions
# are not available outside the hi() function e.g:

greet()
#outputs: NameError: name 'greet' is not defined
```

So now we know that we can define functions in other functions. In other words: we can make *nested functions*. Now you need to learn one more thing, that **functions can return functions too**.

It is not necessary to execute a function within another function, we can return it as an output as well:

```python
def hi(name="yasoob"):
    def greet():
        return "now you are in the greet() function"

    def welcome():
        return "now you are in the welcome() function"

    if name == "yasoob":
        return greet
    else:
        return welcome

a = hi()
print(a)
#outputs: <function greet at 0x7f2143c01500>

#This clearly shows that `a` now points to the greet() function in hi()
#Now try this

print(a())
#outputs: now you are in the greet() function
```

![image-20200812075152957](/Users/lei/Library/Application Support/typora-user-images/image-20200812075152957.png)

Just take a look at the code again. In the `if/else` clause we are returning `greet` and `welcome`, **not `greet()` and `welcome()`**. Why is that? It’s because **when you put a pair of parentheses after it, the function gets executed; whereas if you don’t put parenthesis after it, then it can be passed around and can be assigned to other variables without executing it**. Did you get it? Let me explain it in a little bit more detail. 

When we write `a = hi()`, `hi()` gets executed and because the name is yasoob by default, the function `greet` is returned. If we change the statement to `a = hi(name = "ali")` then the `welcome` function will be returned. **We can also do print `hi()()` which outputs *now you are in the greet() function***.

The following function has that property and could be considered the simplest decorator one could possibly write:

```python
def null_decorator(func):
    return func
```

As you can see, `null_decorator` is **a callable (it’s a function)**, **it takes another callable as its input, and it returns the same input callable without modifying it**.

Let’s use it to *decorate* (or *wrap*) another function:

```python
def greet():
    return 'Hello!'

greet = null_decorator(greet)

>>> greet()
'Hello!'
```

In this example I’ve defined a `greet` function and then **immediately decorated it by running it through the `null_decorator` function**. I know this doesn’t look very useful yet (I mean we specifically designed the null decorator to be useless, right?) but in a moment it’ll clarify how Python’s decorator syntax works.

Instead of explicitly calling `null_decorator` on `greet` and then reassigning the `greet` variable, you can use Python’s `@` syntax for decorating a function in one step:

```python
@null_decorator
def greet():
    return 'Hello!'

>>> greet()
'Hello!'
```

Putting an `@null_decorator` line in front of the function definition is the same as defining the function first and then running through the decorator. Using the `@` syntax is just *syntactic sugar*, and *a shortcut for this commonly used pattern*.

Note that using the `@` syntax decorates the function immediately at definition time. **This makes it difficult to access the undecorated original without brittle hacks**. Therefore you might choose to decorate some functions manually in order to retain the ability to call the undecorated function as well.

### Decorators can modify behaviors

Now that you’re a little more familiar with the decorator syntax, let’s write another decorator that *actually does something* and modifies the behavior of the decorated function.

Here’s a slightly more complex decorator which converts the result of the decorated function to uppercase letters:

```python
def uppercase(func):
    def wrapper():
        original_result = func()
        modified_result = original_result.upper()
        return modified_result
    return wrapper
```

Instead of simply returning the input function like the null decorator did, this `uppercase` decorator defines a new function on the fly (a closure) and uses it to *wrap* the input function **in order to modify its behavior at call time**.

The `wrapper` closure has access to the undecorated input function and it is free to execute additional code before and after calling the input function. (Technically, it doesn’t even need to call the input function at all.)

Note how **up until now the decorated function has never been executed**. Actually calling the input function at this point wouldn’t make any sense—you’ll want the decorator to be able to modify the behavior of its input function when it gets called eventually.

Time to see the `uppercase` decorator in action. What happens if you decorate the original `greet` function with it?

```python
@uppercase
def greet():
    return 'Hello!'

>>> greet()
'HELLO!'
```

I hope this was the result you expected. Let’s take a closer look at what just happened here. Unlike `null_decorator`, **our `uppercase` decorator returns a *different function object* when it decorates a function**:

```python
>>> greet
<function greet at 0x10e9f0950>

>>> null_decorator(greet)
<function greet at 0x10e9f0950>

>>> uppercase(greet)
<function uppercase.<locals>.wrapper at 0x10da02f28>
```

And as you saw earlier, it needs to do that in order to modify the behavior of the decorated function when it finally gets called. The `uppercase` decorator is a function itself. And the only way to influence the “future behavior” of an input function it decorates is to replace (or *wrap*) the input function with a closure.

That’s why `uppercase` defines and returns another function (the closure) that can then be called at a later time, run the original input function, and modify its result.

**Decorators modify the behavior of a callable through a wrapper so you don’t have to permanently modify the original. The callable isn’t permanently modified—its behavior changes only when decorated**.

This let’s you “tack on” reusable building blocks, like logging and other instrumentation, to existing functions and classes. It’s what makes decorators such a powerful feature in Python that’s frequently used in the standard library and in third-party packages.

### Applying multiple decorators to a single function

Perhaps not surprisingly, you can apply more than one decorator to a function. This accumulates their effects and it’s what makes decorators so helpful as reusable building blocks.

Here’s an example. The following two decorators wrap the output string of the decorated function in HTML tags. By looking at how the tags are nested you can see which order Python uses to apply multiple decorators:

```python
def strong(func):
    def wrapper():
        return '<strong>' + func() + '</strong>'
    return wrapper

def emphasis(func):
    def wrapper():
        return '<em>' + func() + '</em>'
    return wrapper
```

Now let’s take these two decorators and apply them to our `greet` function at the same time. You can use the regular `@` syntax for that and just “stack” multiple decorators on top of a single function:

```python
@strong
@emphasis
def greet():
    return 'Hello!'
```

What output do you expect to see if you run the decorated function? Will the `@emphasis` decorator add its `<em>` tag first or does `@strong` have precedence? Here’s what happens when you call the decorated function:

```python
>>> greet()
'<strong><em>Hello!</em></strong>'
```

This clearly shows in **what order the decorators were applied: from *bottom to top***. First, the input function was wrapped by the `@emphasis` decorator, and then the resulting (decorated) function got wrapped again by the `@strong` decorator.

To help me remember this bottom to top order I like to call this behavior *decorator stacking*. *You start building the stack at the bottom and then keep adding new blocks on top to work your way upwards*.

If you break down the above example and avoid the `@` syntax to apply the decorators, the chain of decorator function calls looks like this:

```python
decorated_greet = strong(emphasis(greet))
```

Again you can see here that the `emphasis` decorator is applied first and then the resulting wrapped function is wrapped again by the `strong` decorator.

This also means that deep levels of decorator stacking will have an effect on performance eventually because they keep adding nested function calls. Usually this won’t be a problem in practice, but it’s something to keep in mind if you’re working on performance intensive code.

```python
# 注册
@route('index', methods=['GET', 'POST'])
def static_html():
  return render_template('index.html')

# 等效于
static_html = route('index', methods=['GET', 'POST'])(static_html)

def route(rule, **options):
  def decorator(f):
    endpoint = options.pop('endpoint', None)
    # 使用类似字典的结构以 'index' 为 key，以 method static_html 其他参数为 value 存储绑定关系
    self.add_url_rule(rule, endpoint, f, **options)
    return f
  return decorator
```

解析：

![image-20200812084431847](/Users/lei/Library/Application Support/typora-user-images/image-20200812084431847.png)

```python
# 包装
def html_header(func): # 再传进来的函数不是 content(), 而是 body_header()
  def decorator():
    return f'<html>{func()}</html>'
  return decorator

def body_header(func): 
  def decorator():
    retur f'<body>{func()}</body>'
  return decorator

@html_header
@body_header # body_header 外层再嵌套一个 html_header 装饰器
def content():
  return 'hello world'

content() # 最后运行的是 html 的一个 decorator

# 相当于
decorated_content = html_header(body_header(content))

# output
# '<html><body>hello world</body></html>'
```

### Decorating functions that accept arguments

All examples so far only decorated a simple *nullary* `greet` function that didn’t take any arguments whatsoever. So the decorators you saw here up until now didn’t have to deal with forwarding arguments to the input function.

If you try to apply one of these decorators to a function that takes arguments it will not work correctly. How do you decorate a function that takes arbitrary arguments?

This is where [Python’s `*args` and `**kwargs` feature](https://www.youtube.com/watch?v=WcTXxX3vYgY) for dealing with variable numbers of arguments comes in handy. The following `proxy` decorator takes advantage of that:

```python
def proxy(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

There are two notable things going on with this decorator:

- It uses the `*` and `**` operators in the `wrapper` closure definition to collect all positional and keyword arguments and stores them in variables (`args` and `kwargs`).
- The `wrapper` closure then forwards the collected arguments to the original input function using the `*` and `**` “argument unpacking” operators.

(It’s a bit unfortunate that the meaning of the star and double-star operators is overloaded and changes depending on the context they’re used in. But I hope you get the idea.)

Let’s expand the technique laid out by the `proxy` decorator into a more useful practical example. Here’s a `trace` decorator that logs function arguments and results during execution time:

```python
def trace(func):
    def wrapper(*args, **kwargs):
        print(f'TRACE: calling {func.__name__}() '
              f'with {args}, {kwargs}')

        original_result = func(*args, **kwargs)

        print(f'TRACE: {func.__name__}() '
              f'returned {original_result!r}')

        return original_result
    return wrapper
```

Decorating a function with `trace` and then calling it will print the arguments passed to the decorated function and its return value. This is still somewhat of a toy example—but in a pinch it makes a great debugging aid:

```python
@trace
def say(name, line):
    return f'{name}: {line}'

>>> say('Jane', 'Hello, World')
'TRACE: calling say() with ("Jane", "Hello, World"), {}'
'TRACE: say() returned "Jane: Hello, World"'
'Jane: Hello, World'
```

```python
# 被修饰函数带参数
def outer(func): # 外函数传递的是函数作为参数，并没有处理 foo(a, b) 的参数
  def inner(a, b): # 因此，需要在内函数中对参数a, b进行处理
    print(f'inner: {func.__name__}')
    print(a, b)
    func(a, b)
  return inner

@outer
def foo(a, b):
  print(a+b)
  print(f'foo:{foo.__name__}')
  
foo(1, 2)

# output:
# inner: foo 判断失误
# 1 2
# 3
# foo: inner 判断失误

foo.__name__
# output: 'inner'
```

![image-20200812084850678](/Users/lei/Library/Application Support/typora-user-images/image-20200812084850678.png)

![image-20200812085326242](/Users/lei/Library/Application Support/typora-user-images/image-20200812085326242.png)

![image-20200812085346701](/Users/lei/Library/Application Support/typora-user-images/image-20200812085346701.png)

当希望装饰器能接受更多的参数，从而有更广泛的用途：

```python
# 被修饰函数带不定长参数

def outer2(func):
  def inner2(*args, **kwargs):
    func(*args, **kwargs)
    print('Keywords:', *args, **kwargs)
    print('Keywrods:', args, kwargs)
  return inner2

@outer2
def foo2(a, b, c):
  print(a+b+c)

foo2
# <function __main__.outer2.<locals>.inner2(*args, **kwargs)>  

foo2(1, 3, 5)
# output
# 9
# Keywords: 1 3 5
# Keywrods: (1, 3, 5) {}
```

![image-20200812082353724](/Users/lei/Library/Application Support/typora-user-images/image-20200812082353724.png)

![image-20200812082600203](/Users/lei/Library/Application Support/typora-user-images/image-20200812082600203.png)

#### What does [functools.wraps do?](https://stackoverflow.com/questions/308999/what-does-functools-wraps-do)

When you use a decorator, you're replacing one function with another. In other words, if you have a decorator

```python
def logged(func):
    def with_logging(*args, **kwargs):
        print(func.__name__ + " was called")
        return func(*args, **kwargs)
    return with_logging
```

then when you say

```python
@logged
def f(x):
   """does some math"""
   return x + x * x
```

it's exactly the same as saying

```python
def f(x):
    """does some math"""
    return x + x * x
f = logged(f)
```

and **your function `f` is replaced with the function `with_logging`**. Unfortunately, this means that if you then say

```python
print(f.__name__)
```

it will print `with_logging` **because that's the name of your new function**. In fact, if you look at the docstring for `f`, it will be blank because `with_logging` has no docstring, and so the docstring you wrote won't be there anymore. Also, if you look at the pydoc result for that function, it won't be listed as taking one argument `x`; instead it'll be listed as taking `*args` and `**kwargs` because that's what with_logging takes.

**If using a decorator always meant losing this information about a function, it would be a serious problem**. That's why we have `functools.wraps`. **This takes a function used in a decorator and adds the functionality of copying over the function name, docstring, arguments list, etc**. And since `wraps` is itself a decorator, the following code does the correct thing:

```python
from functools import wraps
def logged(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + " was called")
        return func(*args, **kwargs)
    return with_logging

@logged
def f(x):
   """does some math"""
   return x + x * x

print(f.__name__)  # prints 'f'
print(f.__doc__)   # prints 'does some math'
```

```python
# 被修饰函数带返回值
# 这个装饰器什么都没做，是作为一个装饰器的框架/样式/模板，不用修改函数本身
# 比如，想在执行之前给这个函数做些事情，就在 ret = func(*args, **kwargs) 之前加些代码；
# 如果想在执行之后给这些函数做些事情，就在 ret = func(*args, **kwargs) 之后加些代码

def outer3(func):
  def inner3(*args, **kwargs):
    ret = func(*args, **kwargs)
    return ret
  return inner3

@outer3
def foo3(a, b, c):
  return (a+b+c)

print(foo3(1,3,5))
# 此处，return (a+b+c) 为 9, 所以 ret = func(*args, **kwargs) 为 9
```

```python
# 装饰器函数也能带参数
def outer_arg(bar):
  def outer(func):
    def inner(*args, **kwargs):
      ret = func(*args, **kwargs)
      print(bar)
      return inner # 与
  return outer

# 相当于 outer_arg('foo_arg')(foo)()
# outer_org的返回值 = outer_arg('foo_arg')
# outer 即 这个返回值(foo)？
# () 是想让这个函数执行，而不是只有这个对象
@outer_arg('foo_arg')
def foo(a, b, c):
  return (a + b + c)

print(foo(1, 3, 5))
```

```python
# 装饰器堆叠
# 调用顺序不同，有可能会出现不同的结果
@classmethod
@synchronized(lock)
def foo(cls):
  pass

def foo(cls):
  pass

foo = synchronized(lock)(foo)
foo = classmethod(foo)
```

Speaking of debugging—there are some things you should keep in mind when debugging decorators:

### How to Write “Debuggable” Decorators

When you use a decorator, really what you’re doing is replacing one function with another. One downside of this process is that it “hides” some of the metadata attached to the original (undecorated) function.

For example, the original function name, its docstring, and parameter list are hidden by the wrapper closure:

```python
def greet():
    """Return a friendly greeting."""
    return 'Hello!'

decorated_greet = uppercase(greet)
```

If you try to access any of that function metadata you’ll see the wrapper closure’s metadata instead:

```python
>>> greet.__name__
'greet'
>>> greet.__doc__ # 这都行
'Return a friendly greeting.'

>>> decorated_greet.__name__
'wrapper'
>>> decorated_greet.__doc__
None
```

This makes debugging and working with the Python interpreter awkward and challenging. Thankfully there’s a quick fix for this: the [`functools.wraps` decorator](https://docs.python.org/3/library/functools.html#functools.wraps) included in Python’s standard library.

You can use `functools.wraps` in your own decorators to **copy over the lost metadata from the undecorated function to the decorator closure**. Here’s an example:

```python
import functools

def uppercase(func):
    @functools.wraps(func)
    def wrapper():
        return func().upper()
    return wrapper
```

Applying `functools.wraps` to the wrapper closure returned by the decorator carries over the docstring and other metadata of the input function:

```python
@uppercase
def greet():
    """Return a friendly greeting."""
    return 'Hello!'

>>> greet.__name__
'greet'
>>> greet.__doc__
'Return a friendly greeting.'
```

As a best practice I’d recommend that you **use `functools.wraps` in all of the decorators you write yourself**. It doesn’t take much time and it will save you (and others) debugging headaches down the road.

```python
# @functools.wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES)
# 用于在定义包装器函数时发起调用 update_wrapper() 作为函数装饰器
# 它等价于 partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)

from time import ctime, sleep
from functools import wraps
def outer_arg(bar):
  def outer(func):
    # 结构不变，增加wraps
    @wraps(func)
    def inner(*args, **kwargs):
      print('%s called at %s'%(func.__name__, ctime()))
      ret = func(*args, **kwargs)
      print(bar)
      return ret
   return inner
return outer

@outer_arg('foo_arg')
def foo(a, b, c):
  """__doc__"""
  return (a + b + c)

print(foo.__name__)
# output: foo
```

`@wraps(func)` 主要保持，函数是不变的。

```python
# flask 使用 @wraps(func) 的案例

from functools import wraps

def requires_auth(func):
  @wraps(func)
  def auth_method(*args, **kwargs):
    if not auth:
      authenticate()
    return auth_method
  
@requires_auth
def func_demo():
  pass
```

再来一例：

```python
from functools import wraps

def logit(logfile='out.log'):
  def logging_decorator(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
      log_string = func.__name__ + ' was called'
      print(log_string)
      with open(logfile, 'a') as opened_file:
        opened_file.write(log_string + '\n')
      return func(*args, **kwargs)
    return wrapped_function
  return logging_decorator

@logit()
def myfunc1():
  pass

myfunc1()
# Output: myfunc1 was called

@logit(logfile='func2.log')
def myfunc2():
  pass
```

**functools.lru_cache**

```python
# an example from Fluent Python
# functools.lru_cache(maxsize=128, typed=False) 有两个可选参数
# maxsize 代表缓存的内存占用值，超过这个值之后，旧的结果就会被释放
# typed若为True，则会把不同的参数类型得到的结果分开保存

import functools

@functools.lru_cache() # 若是没有写上，就会运行多几倍的时间
def fibonacci(n):
  if n < 2:
    return n
  return fibonacci(n-2) + fibonacci(n-1)

if __name__ == '__main__':
  import timeit
  print(timeit.timeit('fibonacci(6)', setup='from __main__ import fibonacci'))
```



### Writing your first decorator

In the last example we actually made a decorator! Let’s modify the previous decorator and make a little bit more usable program:

```python
def a_new_decorator(a_func):

    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")

        a_func()

        print("I am doing some boring work after executing a_func()")

    return wrapTheFunction

def a_function_requiring_decoration():
    print("I am the function which needs some decoration to remove my foul smell")

a_function_requiring_decoration()
#outputs: "I am the function which needs some decoration to remove my foul smell"

a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration)
#now a_function_requiring_decoration is wrapped by wrapTheFunction()

a_function_requiring_decoration()
#outputs:I am doing some boring work before executing a_func()
#        I am the function which needs some decoration to remove my foul smell
#        I am doing some boring work after executing a_func()
```

Did you get it? We just applied the previously learned principles. This is exactly what the decorators do in Python! *They wrap a function and modify its behaviour in one way or another*. Now you might be wondering why we did not use the @ anywhere in our code? That is just a short way of making up a decorated function. Here is how we could have run the previous code sample using @.

```python
@a_new_decorator
def a_function_requiring_decoration():
    """Hey you! Decorate me!"""
    print("I am the function which needs some decoration to "
          "remove my foul smell")

a_function_requiring_decoration()
#outputs: I am doing some boring work before executing a_func()
#         I am the function which needs some decoration to remove my foul smell
#         I am doing some boring work after executing a_func()

#the @a_new_decorator is just a short way of saying:
a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration)
```

I hope you now have a basic understanding of how decorators work in Python. Now there is one problem with our code. If we run:

```python
print(a_function_requiring_decoration.__name__)
# Output: wrapTheFunction
```

That’s not what we expected! Its name is “a_function_requiring_decoration”. Well, our function was replaced by wrapTheFunction. **It overrode the name and docstring of our function**. Luckily, Python provides us a simple function to solve this problem and that is `functools.wraps`. Let’s modify our previous example to use `functools.wraps`:

```python
from functools import wraps

def a_new_decorator(a_func):
    @wraps(a_func)
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")
        a_func()
        print("I am doing some boring work after executing a_func()")
    return wrapTheFunction

@a_new_decorator
def a_function_requiring_decoration():
    """Hey yo! Decorate me!"""
    print("I am the function which needs some decoration to "
          "remove my foul smell")

print(a_function_requiring_decoration.__name__)
# Output: a_function_requiring_decoration
```

Now that is much better.

### Some use-cases of decorators

**Blueprint:**

```python
from functools import wraps
def decorator_name(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not can_run:
            return "Function will not run"
        return f(*args, **kwargs)
    return decorated

@decorator_name
def func():
    return("Function is running")

can_run = True
print(func())
# Output: Function is running

can_run = False
print(func())
# Output: Function will not run
```

Note: `@wraps` takes a function to be decorated and adds the functionality of copying over the function name, docstring, arguments list, etc. This allows us to access the pre-decorated function’s properties in the decorator.

Now let’s take a look at the areas where decorators really shine and their usage makes something really easy to manage.

#### Authorization

Decorators can help to check whether someone is authorized to use an endpoint in a web application. They are extensively used in Flask web framework and Django. Here is an example to employ decorator based authentication:

**Example :**

```python
from functools import wraps

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            authenticate()
        return f(*args, **kwargs)
    return decorated
```

#### Logging

Logging is another area where the decorators shine. Here is an example:

```python
from functools import wraps

def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + " was called")
        return func(*args, **kwargs)
    return with_logging

@logit
def addition_func(x):
   """Do some math."""
   return x + x


result = addition_func(4)
# Output: addition_func was called
```

I am sure you are already thinking about some clever uses of decorators.

## Decorators with Arguments

Come to think of it, isn’t `@wraps` also a decorator? But, it takes an argument like any normal function can do. So, why can’t we do that too?

This is because when you use the `@my_decorator` syntax, you are applying a wrapper function with a single function as a parameter. Remember, everything in Python is an object, and this includes functions! With that in mind, we can write a function that returns a wrapper function.

### 7.6.1. Nesting a Decorator Within a Function

Let’s go back to our logging example, and create a wrapper which lets us specify a logfile to output to.

```python
from functools import wraps

def logit(logfile='out.log'):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string = func.__name__ + " was called"
            print(log_string)
            # Open the logfile and append
            with open(logfile, 'a') as opened_file:
                # Now we log to the specified logfile
                opened_file.write(log_string + '\n')
            return func(*args, **kwargs)
        return wrapped_function
    return logging_decorator

@logit()
def myfunc1():
    pass

myfunc1()
# Output: myfunc1 was called
# A file called out.log now exists, with the above string

@logit(logfile='func2.log')
def myfunc2():
    pass

myfunc2()
# Output: myfunc2 was called
# A file called func2.log now exists, with the above string
```

### 7.6.2. Decorator Classes

```python
class MyClass(object):
  def __init__(self, var='init_var', *args, **kwargs):
    self._v = var
    super(MyClass, self).__init__(*args, **kwargs)
    
  def __call__(self, func):
    # 类的函数装饰器
    @wraps(func)
    def wrapped_function(*args, **kwargs):
      func_name = func.__name__ + ' wad called'
      print(func_name)
      return func(*args, **kwargs)
    return wrapped_function
  
  def myfunc():
    pass
  
  MyClass(100)(myfunc)() 
  # output:
  # myfunc was called
  
  # 其他经常在类装饰器的python自带装饰器：
  # classmethod
  # staticmethod
  # property
  
```



再来看一个例子：

```python
class Count(object):
  def __init__ (self, func):
    self._func = func
    self.num_calls = 0
    
  def __call__(self, *args, **kwargs):
    self.num_calls += 1
    print('num of call is {}'.format(self.num_calls))
    return self._func(*args, **kwargs)
  
  @Count
  def example():
    print('Hello')
```



![image-20200813150904299](/Users/lei/Library/Application Support/typora-user-images/image-20200813150904299.png)

**装饰器装饰类**

```python
@decorator
class MyClass(object):
  def __init__(self, number):
    self.number = number
    
  # 重写display
  def display(self):
    print('number is', self.number)
    
six = MyClass(6)
for i in range(5):
  six.display()
```



Now we have our logit decorator in production, but when some parts of our application are considered critical, failure might be something that needs more immediate attention. Let’s say sometimes you want to just log to a file. Other times you want an email sent, so the problem is brought to your attention, and still keep a log for your own records. This is a case for using inheritence, but so far we’ve only seen functions being used to build decorators.

Luckily, classes can also be used to build decorators. So, let’s rebuild logit as a class instead of a function.

```python
class logit(object):

    _logfile = 'out.log'

    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        log_string = self.func.__name__ + " was called"
        print(log_string)
        # Open the logfile and append
        with open(self._logfile, 'a') as opened_file:
            # Now we log to the specified logfile
            opened_file.write(log_string + '\n')
        # Now, send a notification
        self.notify()

        # return base func
        return self.func(*args)



    def notify(self):
        # logit only logs, no more
        pass
```

This implementation has an additional advantage of being much cleaner than the nested function approach, and wrapping a function still will use the same syntax as before:

```python
logit._logfile = 'out2.log' # if change log file
@logit
def myfunc1():
    pass

myfunc1()
# Output: myfunc1 was called
```

Now, let’s subclass logit to add email functionality (though this topic will not be covered here).

```python
class email_logit(logit):
    '''
    A logit implementation for sending emails to admins
    when the function is called.
    '''
    def __init__(self, email='admin@myproject.com', *args, **kwargs):
        self.email = email
        super(email_logit, self).__init__(*args, **kwargs)

    def notify(self):
        # Send an email to self.email
        # Will not be implemented here
        pass
```

From here, `@email_logit` works just like `@logit` but sends an email to the admin in addition to logging.

### Python Decorators – Key Takeaways

- Decorators define reusable building blocks you can apply to a callable to modify its behavior without permanently modifying the callable itself.
- The `@` syntax is just a shorthand for calling the decorator on an input function. Multiple decorators on a single function are applied bottom to top (*decorator stacking*).
- As a debugging best practice, use the [`functools.wraps`](https://docs.python.org/3/library/functools.html#functools.wraps) helper in your own decorators to carry over metadata from the undecorated callable to the decorated one.

### 答疑

**1**

想问一下为啥这里装饰器在模块导入的时候就会自动运行？主要是如果装饰器里写的一些print（）打印，那一这样自动运行不就乱套了吗？

![image-20200812072308901](/Users/lei/Library/Application Support/typora-user-images/image-20200812072308901.png)

**2**



### References

* [7. Decorators](https://book.pythontips.com/en/latest/decorators.html)
* [Python Decorators: A Step-By-Step Introduction](https://dbader.org/blog/python-decorators)



















