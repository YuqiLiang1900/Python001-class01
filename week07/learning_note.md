# Learning Notes for Week07

python的提供一系列和属性访问有关的特殊方法：`__get__`, `__getattr__`, `__getattribute__`, `__getitem__`

## 属性的访问机制

一般情况下，属性访问的默认行为是从对象的字典中获取，并当获取不到时会沿着一定的查找链进行查找。例如 `a.x` 的查找链就是，从 `a.__dict__['x']` ，然后是 `type(a).__dict__['x']` ，再通过 `type(a)` 的基类开始查找。

若查找链都获取不到属性，则抛出 `AttributeError` 异常。

### `__getattr__` 方法

当对象的属性不存在时调用。**如果通过正常的机制（即通过`__dict__`）能找到对象属性的话，不会调用 `__getattr__` 方法**。

```python
class A(object):
    a = 1
    def __getattr__(self, item):
        print('__getattr__ call')
        return item

t = A()
print(t.a)
print(t.b)
# output
1
__getattr__ call
b
```

### `__getattribute__` 方法

不管属性是否存在，这个方法会**被无条件调用**。如果类中还定义了 `__getattr__` ，则不会调用 `__getattr__()`方法，除非在 `__getattribute__` 方法中显示调用`__getattr__()` 或者抛出了 `AttributeError` 。

```python
class A:
    a = 1
    def __getattribute__(self, item):
        print('__getattribute__ call')
        raise AttributeError

    def __getattr__(self, item):
        print('__getattr__ call')
        return item

t = A()
print(t.a)
print(t.b)
```

一般情况下，为了保留 `__getattr__` 的作用，`__getattribute__()` 方法中一般返回父类的同名方法：

```python
def __getattribute__(self, item):
    return object.__getattribute__(self, item)
```

使用基类的方法来获取属性能避免在方法中出现无限递归的情况。

### `__get__` 方法

这个方法比较简单说明，它与前面的关系不大。

如果一个类中定义了 `__get__()`, `__set__()` 或 `__delete__()` 中的任何方法。则这个类对象称为描述符。

```python
class Descri(object):
    def __get__(self, obj, type=None):
        print("call get")

    def __set__(self, obj, value):
        print("call set")

class A(object):
    x = Descri()

a = A()
a.__dict__['x'] = 1  # 不会调用 __get__
a.x                  # 调用 __get__
```

如果查找的属性是在描述符对象中，则这个描述符会覆盖上文说的属性访问机制，体现在查找链的不同，而这个行文也会因为调用的不同而稍有不一样：

- 如果调用是对象实例(题目中的调用方式)，`a.x` 则转换为调用： 。`type(a).__dict__['x'].__get__(a, type(a))`
- 如果调用的是类属性, `A.x` 则转换为：`A.__dict__['x'].__get__(None, A)`
- 其他情况见文末参考资料的文档

### `__getitem__` 方法

这个调用也属于无条件调用，这点与 `__getattribute__` 一致。区别在于 `__getitem__` 让类实例允许 `[]` 运算，可以这样理解：

- `__getattribute__` 适用于所有 `.` 运算符；
- `__getitem__` 适用于所有 `[]` 运算符。

```python
class A(object):
    a = 1

    def __getitem__(self, item):
        print('__getitem__ call')
        return item

t = A()
print(t['a'])
print(t['b'])
```

如果仅仅想要对象能够通过 `[]` 获取对象属性可以简单的：

```python
def __getitem(self, item):
    return object.__getattribute__(self, item)
```

### 总结

当这几个方法同时出现可能就会扰乱你了。我在网上看到一份示例还不错，稍微改了下：

```python
class C(object):
    a = 'abc'

    def __getattribute__(self, *args, **kwargs):
        print("__getattribute__() is called")
        return object.__getattribute__(self, *args, **kwargs)

    #        return "haha"
    def __getattr__(self, name):
        print("__getattr__() is called ")
        return name + " from getattr"

    def __get__(self, instance, owner):
        print("__get__() is called", instance, owner)
        return self

    def __getitem__(self, item):
        print('__getitem__ call')
        return object.__getattribute__(self, item)

    def foo(self, x):
        print(x)

class C2(object):
    d = C()

if __name__ == '__main__':
    c = C()
    c2 = C2()
    print(c.a)
    print(c.zzzzzzzz)
    c2.d
    print(c2.d.a)
    print(c['a'])
```

可以结合输出慢慢理解，这里还没涉及继承关系呢。总之，每个以 `__ get` 为前缀的方法都是获取对象内部数据的钩子，名称不一样，用途也存在较大的差异，只有在实践中理解它们，才能真正掌握它们的用法。

```python
In [6]: c.a                                                                     
__getattribute__() is called
Out[6]: 'abc'

In [7]: c.zzzzzzzz                                                              
__getattribute__() is called
__getattr__() is called 
Out[7]: 'zzzzzzzz from getattr'
  
In [8]: c2.d # 属性是一个类实例                                                                   
__get__() is called <__main__.C2 object at 0x7fbd083c8250> <class '__main__.C2'>
Out[8]: __getattribute__() is called
__getattribute__() is called
__getattr__() is called 
__getattribute__() is called
__getattribute__() is called
<__main__.C at 0x7fbd0840da50>
```



## Python 的自省机制

什么是自省？

在日常生活中，自省（introspection）是一种自我检查行为。

在**计算机编程中，自省是指这种能力：检查某些事物以确定它是什么、它知道什么以及它能做什么。自省向程序员提供了极大的灵活性和控制力**。

说的更简单直白一点：**自省就是面向对象的语言所写的程序在运行时，能够知道对象的类型。简单一句就是，运行时能够获知对象的类型**。

例如python, buby, object-C, c++都有自省的能力，这里面的c++的自省的能力最弱，只能够知道是什么类型，而像python可以知道是什么类型，还有什么属性。

**最好的理解自省就是通过例子**： [Type introspection](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Type_introspection) 这里是各种编程语言中自省（introspection）的例子（**这个链接里的例子很重要，也许你很难通过叙述理解什么是introspection，但是通过这些例子，一下子你就可以理解了**） 

回到Python，**Python中比较常见的自省（introspection）机制(函数用法)有： dir()，type(), hasattr(), isinstance()，通过这些函数，我们能够在程序运行时得知对象的类型，判断对象是否存在某个属性，访问对象的属性。**

### `dir()`

　`dir()` 函数可能是 Python 自省机制中最著名的部分了。它返回传递给它的任何对象的属性名称经过排序的列表。如果不指定对象，则 `dir() `返回当前作用域中的名称。让我们将 `dir()` 函数应用于 keyword 模块，并观察它揭示了什么：

```python
>>> import keyword
>>> dir(keyword)
['__all__', '__builtins__', '__doc__', '__file__', '__name__', '__package__', 'iskeyword', 'kwlist', 'main']
```

### `type()`
`type()` 函数有助于我们确定对象是字符串还是整数，或是其它类型的对象。它通过返回类型对象来做到这一点，可以将这个类型对象与 types 模块中定义的类型相比较：

```python
>>> type(42)
<class 'int'>
>>> type([])
<class 'list'>
 **hasattr()**
```

　对象拥有属性，并且 `dir()` 函数会返回这些属性的列表。但是，有时我们只想测试一个或多个属性是否存在。如果对象具有我们正在考虑的属性，那么通常希望只检索该属性。这个任务可以由 hasattr() 和 getattr() 函数来完成.

```python
>>> hasattr(id, '__doc__')
True
```

### `isinstance() `
可以使用` isinstance() `函数测试对象，以确定它是否是某个特定类型或定制类的实例：

```python
>>> isinstance("python", str)
True
```



## `__dict__` 和 `dir()`的区别

![image-20200806153405764](/Users/lei/Library/Application Support/typora-user-images/image-20200806153405764.png)

我们不会也不应该重写 `__dict__`，再说 `__dict__` 是属性不是方法。

`dir()` 就是一个单独的自省方法，`__dict__` 就是一个属性，没有必然联系。

如果同时存在，执行顺序是： `__getattribute__` > `__getattr__` > `__dict__`

那我只能强行理解内在逻辑是：
`__getattribute__` 不管属性是否存在，都会调用，
`__getattr__` 只有属性不存在，才会调用，
`__dict__` 是属性，不是方法。

![image-20200806154533293](/Users/lei/Library/Application Support/typora-user-images/image-20200806154533293.png)

在给 `__dict__` 直接进行操作的时候 python 还是会自动调用一次 `__getattribute__` 的。然后你得代码 `self.item = 100` 实际上是达不到想要的效果的，你应该 `setattr(self, item, 100)`。`self.item = 100` 就把属性写死成 `item` 了，没有设置传进来的属性，而且使用 `setattr(self, item, 100)` 就不会出现重复调用 `__getattribute__` 问题。

通过 `obj.__dict__[x] = y` 的方式赋值的时候，会自动调用一次 `__getattribute__`，这里除了赋值其实有个读取值的操作，就是说 `obj.__dict__[x] = y` 是分多步完成的，而且会先 `obj.__dict__` 取值，然后再改变其值了

## IPython

![image-20200806153935448](/Users/lei/Library/Application Support/typora-user-images/image-20200806153935448.png)

IPython 只是再测试一些小 demo 级别的代码时候方便快速查看测试结果用的，真正写代码还是写到文件中执行，所以问题也不大，下次遇到这种感觉上非常规的问题，就可以用 Python 原生的交互式命令行再验证下了，一般不测试这么底层的协议，是没啥大问题的，比如我经常把 IPython 当计算器用，不也挺好用的嘛

## `__repr__` vs `__str__`

![image-20200806154139404](/Users/lei/Library/Application Support/typora-user-images/image-20200806154139404.png)

`__repr__` 就是方便调试用的，几乎不太用，一般都断点调试

![image-20200806154208235](/Users/lei/Library/Application Support/typora-user-images/image-20200806154208235.png)



[这个打这么多次这么变态，所以说就是Ipython 和 pycharm 无法言说的bug嘛😂]
这个不算 BUG，你看下 `help()` 的时候就调用这么多次，IDE 可能会自己调用一些对象的自省方法，来获得更好的提示之类的功能吧

![image-20200806154238363](/Users/lei/Library/Application Support/typora-user-images/image-20200806154238363.png)

## 疑难问题

![image-20200806170050340](/Users/lei/Library/Application Support/typora-user-images/image-20200806170050340.png)

![image-20200806170104331](/Users/lei/Library/Application Support/typora-user-images/image-20200806170104331.png)

![image-20200806165952753](/Users/lei/Library/Application Support/typora-user-images/image-20200806165952753.png)

![image-20200806170017425](/Users/lei/Library/Application Support/typora-user-images/image-20200806170017425.png)

## `getattr(object, 'x')`

`getattr(object, 'x')` **is completely equivalent** to `object.x`.

There are **only two cases** where `getattr` can be useful.

- you can't write `object.x`, because you don't know in advance which attribute you want (it comes from a string). Very useful for meta-programming.
- you want to provide a default value. `object.y` will raise an `AttributeError` if there's no `y`. But `getattr(object, 'y', 5)` will return `5`.

## `@property`

The `property()` function returns a special [descriptor object](https://docs.python.org/howto/descriptor.html):

```python
>>> property()
<property object at 0x10ff07940>
```

It is this object that has *extra* methods:

```python
>>> property().getter
<built-in method getter of property object at 0x10ff07998>
>>> property().setter
<built-in method setter of property object at 0x10ff07940>
>>> property().deleter
<built-in method deleter of property object at 0x10ff07998>
```

These act as decorators *too*. They return a new property object:

```python
>>> property().getter(None)
<property object at 0x10ff079f0>
```

that is a copy of the old object, but with one of the functions replaced.

Remember, that the `@decorator` syntax is just syntactic sugar; the syntax:

```python
@property
def foo(self): return self._foo
```

really means the same thing as

```python
def foo(self): return self._foo
foo = property(foo)
```

so `foo` the function is replaced by `property(foo)`, which we saw above is a special object. Then when you use `@foo.setter()`, what you are doing is call that `property().setter` method I showed you above, which returns a new copy of the property, but this time with the setter function replaced with the decorated method.

The following sequence also creates a full-on property, by using those decorator methods.

First we create some functions and a `property` object with just a getter:

```python
>>> def getter(self): print('Get!')
... 
>>> def setter(self, value): print('Set to {!r}!'.format(value))
... 
>>> def deleter(self): print('Delete!')
... 
>>> prop = property(getter)
>>> prop.fget is getter
True
>>> prop.fset is None
True
>>> prop.fdel is None
True
```

Next we use the `.setter()` method to add a setter:

```python
>>> prop = prop.setter(setter)
>>> prop.fget is getter
True
>>> prop.fset is setter
True
>>> prop.fdel is None
True
```

Last we add a deleter with the `.deleter()` method:

```python
>>> prop = prop.deleter(deleter)
>>> prop.fget is getter
True
>>> prop.fset is setter
True
>>> prop.fdel is deleter
True
```

Last but not least, the `property` object acts as a [descriptor object](https://docs.python.org/reference/datamodel.html#implementing-descriptors), so it has [`.__get__()`](https://docs.python.org/reference/datamodel.html#object.__get__), [`.__set__()`](http://docs.python.org/reference/datamodel.html#object.__set__) and [`__delete__()`](http://docs.python.org/reference/datamodel.html#object.__delete__) methods to hook into instance attribute getting, setting and deleting:

```py
>>> class Foo: pass
... 
>>> prop.__get__(Foo(), Foo)
Get!
>>> prop.__set__(Foo(), 'bar')
Set to 'bar'!
>>> prop.__delete__(Foo())
Delete!
```

The Descriptor Howto includes a [pure Python sample implementation](http://docs.python.org/howto/descriptor.html#properties) of the `property()` type:

> ```python
> class Property:
>     "Emulate PyProperty_Type() in Objects/descrobject.c"
> 
>     def __init__(self, fget=None, fset=None, fdel=None, doc=None):
>         self.fget = fget
>         self.fset = fset
>         self.fdel = fdel
>         if doc is None and fget is not None:
>             doc = fget.__doc__
>         self.__doc__ = doc
> 
>     def __get__(self, obj, objtype=None):
>         if obj is None:
>             return self
>         if self.fget is None:
>             raise AttributeError("unreadable attribute")
>         return self.fget(obj)
> 
>     def __set__(self, obj, value):
>         if self.fset is None:
>             raise AttributeError("can't set attribute")
>         self.fset(obj, value)
> 
>     def __delete__(self, obj):
>         if self.fdel is None:
>             raise AttributeError("can't delete attribute")
>         self.fdel(obj)
> 
>     def getter(self, fget):
>         return type(self)(fget, self.fset, self.fdel, self.__doc__)
> 
>     def setter(self, fset):
>         return type(self)(self.fget, fset, self.fdel, self.__doc__)
> 
>     def deleter(self, fdel):
>         return type(self)(self.fget, self.fset, fdel, self.__doc__)
> ```

Here is a minimal example of how `@property` can be implemented:

```python
class Thing:
    def __init__(self, my_word):
        self._word = my_word 
    @property
    def word(self):
        return self._word

>>> print( Thing('ok').word )
'ok'
```

Otherwise `word` remains a method instead of a property.

```python
class Thing:
    def __init__(self, my_word):
        self._word = my_word
    def word(self):
        return self._word

>>> print( Thing('ok').word() )
'ok'
```



## `@classmethod`

classmethod 的两种最常用的场景：

![image-20200807123156589](/Users/lei/Library/Application Support/typora-user-images/image-20200807123156589.png)

![image-20200807123206714](/Users/lei/Library/Application Support/typora-user-images/image-20200807123206714.png)

## Bind Method 绑定方法

![An illustration of Python bound methods](https://www.technovelty.org/static/images/python-bound-method.png)

In the above diagram on the left, we have the fairly simple conceptual model of a class with a function. One naturally tends to think of the function as a part of the class and your instance calls into that function. This is conceptually correct, but a little abstracted from what's actually happening.

The right attempts to illustrate the underlying process in some more depth. The first step, on the top right, is building something like the following:

```python
class Foo():
   def function(self):
       print "hi!"
```

As this illustrates, the above code results in two things happening; firstly a *function object* for `function` is created and secondly **the `__dict__` attribute of the class is given a key `function` that points to this function object**.

Now the thing about this function object is that **it implements the *descriptor protocol***. In short, **if an object implements a `__get__` function; then when that object is accessed as an attribute of an object the `__get__` function is called**. You can read up on the descriptor protocol, but the important part to remember is that **it passes in the *context* from which it is called; that is the object that is calling the function**.

So, for example, when we then do the following:

```python
f = Foo()
f.function()
```

what happens is that we get the attribute `function` of `f` and then call it. `f` above doesn't actually know anything about `function` as such — what it does know is its class inheritance and so **Python goes searching the parent's class `__dict__` to try and find the `function` attribute**. It finds this, and as per the descriptor protocol when the attribute is accessed it calls the `__get__` function of the underlying function object.

What happens now is that **the function's `__get__` method returns essentially a wrapper object that stores the information to *bind* the function to the object**. This wrapper object is of type `types.MethodType` and you can see it stores some important attributes in the object — `im_func` which is the function to call, and `im_self` which is the object who called it. Passing the object through to `im_self` is how `function` gets it's first `self` argument (the calling object).

So when you print the value of `f.function()` you see it report itself as a *bound method*. So hopefully this illustrates that **a bound method is a just a special object that knows how to call an underlying function with context about the object that's calling it**.

To try and make this a little more concrete, consider the following program:

```python
import types

class Foo():

    def function(self):
        print "hi!"

f = Foo()

# this is a function object
print Foo.__dict__['function']

# this is a method as returned by
#   Foo.__dict__['function'].__get__()
print f.function

# we can check that this is an instance of MethodType
print type(f.function) == types.MethodType

# the im_func field of the MethodType is the underlying function
print f.function.im_func
print Foo.__dict__['function']

# these are the same object
print f.function.im_self
print f
```

Running this gives output something like

```python
$ python ./foo.py
<function function at 0xb73540d4>
<bound method Foo.function of <__main__.Foo instance at 0xb736960c>>
True
<function function at 0xb73540d4>
<function function at 0xb73540d4>
<__main__.Foo instance at 0xb72c060c>
<__main__.Foo instance at 0xb72c060c>
```

To pull it apart; we can see that `Foo.__dict__['function']` is a function object, but then `f.function` is a *bound method*. The bound method's `im_func` is the underlying function object, and the `im_self` is the object `f`: thus `im_func(im_self)` is calling `function` with the correct object as the first argument `self`.

**So the main point is to kind of shift thinking about a function as some particular intrinsic part of a class, but rather as a separate object abstracted from the class that gets bound into an instance as required**. **The class is in some ways a template and namespacing tool to allow you to find the right function objects; it doesn't actually implement the functions as such**.

There is plenty more information if you search for "descriptor protocol" and Python binding rules and lots of advanced tricks you can play. But hopefully this is a useful introduction to get an initial handle on what's going on!

## Python getattr() function

Python **getattr()** function is used to get the value of an object’s attribute and if no attribute of that object is found, default value is returned.

Basically, returning the default value is the main reason why you may need to use Python getattr() function. So, before starting the tutorial, lets see the basic syntax of Python’s getattr() function.

```python
getattr(object_name, attribute_name[, default_value])
```

### Python getattr() example

In this section, we will learn how to access attribute values of an object using `getattr()` function. Suppose, we are writing a class named `Student`. The basic attributes of Student class are `student_id` and `student_name`. Now we will create an object of the class Student and access it’s attribute.

```python
class Student:
    student_id=""
    student_name=""

    # initial constructor to set the values
    def __init__(self):
        self.student_id = "101"
        self.student_name = "Adam Lam"

student = Student()
# get attribute values by using getattr() function
print('\ngetattr : name of the student is =', getattr(student, "student_name"))

# but you could access this like this
print('traditional: name of the student is =', student.student_name)
```

So, the output will be like this

![python getattr example](https://cdn.journaldev.com/wp-content/uploads/2017/10/python-getattr.png)

### Python getattr() default value

In this section, we will use the python getattr() default value option. If you want to access any attribute that doesn’t belong to the object, then you can use the getattr() default value option.

For example, if the `student_cgpa` attribute is not present for the student, then will show a default value.

In the following example we will see example of default value. We will also learn what happens if the attribute is not present and we are not using the default value option.

```python
class Student:
    student_id=""
    student_name=""

    # initial constructor to set the values
    def __init__(self):
        self.student_id = "101"
        self.student_name = "Adam Lam"

student = Student()
# using default value option
print('Using default value : Cgpa of the student is =', getattr(student, "student_cgpa", 3.00))
# without using default value
try:
    print('Without default value : Cgpa of the student is =', getattr(student, "student_cgpa"))
except AttributeError:
    print("Attribute is not found :(")
```

So, after running the code you will get output like this

```python
Using default value : Cgpa of the student is = 3.0
Attribute is not found :(
```

Notice that `AttributeError` is raised when the default value is not provided while calling getattr() function.

### Reason for using Python getattr() function

The main reason to use python getattr() is that we can get the value by using the name of the attribute as String. So you can manually input the attribute name in your program from console.

Again, if an attribute is not found you can set some default value, which enables us to complete some of our incomplete data.

Also if your Student class is work in progress, then we can use getattr() function to complete other code. Once Student class has this attribute, it will automatically pick it up and not use the default value.

## Debug 模式

![image-20200808113903912](/Users/lei/Library/Application Support/typora-user-images/image-20200808113903912.png)

Red is the standard color for variables.

Blue indicates that a variable has changed while you're stepping through the code. If you continue to the next iteration of your loop (assuming offlineNotifications is a Collection), you will see those are the variables manipulated in the current execution of code.

这个打断点就要在第一行 if 那一行处打，这就像之前的 print 大法，也是在函数第一行进行 print，在 for 语句内部 print 有时候因为逻辑走不进去，所以 print 就不输出
1. 断点尽量往前打
2. 也要尽量避开逻辑判断，在逻辑判断之前，或者 if else 语句块各自打断点，保证断点都能进入



