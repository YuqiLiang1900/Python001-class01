# Learning Notes for Week10

## 期末总结

## url 反向生成 vs redirect 重定向

![image-20200906203013532](/Users/lei/Library/Application Support/typora-user-images/image-20200906203013532.png)

`{% url 'sentiment:comment' %}` 是 django 模板引擎读到以后，自动转换成了 /comments，然后就变成了 a 标签的 href 属性，点击 a 标签就会跳转到这个 url，这是 a 标签的作用，全程不需要 redirect重定向，redirect重定向是另一个概念，是我们要在 views 视图函数里跳转到某个页面的时候才会使用的。

forloop 是 django 提供的一个对象，这个对象上有很多属性，forloop.counter 属性就是当前循环的那个计数器，代表循环到第几次了，所以可以作为序号使用。

## 模版渲染语法

### 函数设计用法

![image-20200906203104249](/Users/lei/Library/Application Support/typora-user-images/image-20200906203104249.png)

### extends & block

![image-20200906203258876](/Users/lei/Library/Application Support/typora-user-images/image-20200906203258876.png)

![image-20200906203402920](/Users/lei/Library/Application Support/typora-user-images/image-20200906203402920.png)

### tab 自动补全

block 然后 tab，如果父模板中所有的 block 都被覆写了以后，就不会有提示了

![image-20200906203430804](/Users/lei/Library/Application Support/typora-user-images/image-20200906203430804.png)

![image-20200906203455218](/Users/lei/Library/Application Support/typora-user-images/image-20200906203455218.png)

![image-20200906203448312](/Users/lei/Library/Application Support/typora-user-images/image-20200906203448312.png)

![image-20200906203600052](/Users/lei/Library/Application Support/typora-user-images/image-20200906203600052.png)

Q：所以就基本上有四类：nav, style, title, script? 不是还有 content 嘛？一般如何判断用啥关键词呢？

A：用啥关键词还是要看内容要写什么，这几个是比较常用的，侧边栏可以叫 sidebar，就跟变量起名字一样的道理

### TO-DO Practice

![image-20200906204218458](/Users/lei/Library/Application Support/typora-user-images/image-20200906204218458.png)

## css

### css 背景花纹无法完全撑开

![image-20200906203218222](/Users/lei/Library/Application Support/typora-user-images/image-20200906203218222.png)

![image-20200906203157625](/Users/lei/Library/Application Support/typora-user-images/image-20200906203157625.png)

![image-20200906203207333](/Users/lei/Library/Application Support/typora-user-images/image-20200906203207333.png)

### css 语法

![image-20200906203918372](/Users/lei/Library/Application Support/typora-user-images/image-20200906203918372.png)

Q：

```html
body {
    background-image: url(/static/img/leaves-pattern.png);
}
```

那这个url（）里面写的  /static/img/leaves-pattern.png，为啥不用引号“”这样呢😂

A:

css 语法规定😂，https://www.w3school.com.cn/cssref/pr_background-image.asp
不要被已有知识圈住，即使用已有知识类比学习新知识更快，但也要接受不同的思想

![image-20200906204034032](/Users/lei/Library/Application Support/typora-user-images/image-20200906204034032.png)

Q: 

嗯嗯，我就是在想是不是css有不同的数据结构，不然这个不是字符串的话该怎么放到函数里被处理呢😂

A: 

就像 django 过滤器这个语法设计就很另类，不用有舍不同数据结构，就当一个大的字符串读到 python 里，然后在字符串拆分解析就好了，css 咋解析的我也不知道，浏览器内部的事情，html 和 css 都不是编程语言，没有流程控制啥的逻辑，只要记住就行了，就像写好的函数一样，我们想用就调用一下

## Git 在 PyCharm 中的回退用法

没事，git 要常用才能熟练，git 命令超多，我研究也不深入，先把常用的几个命令用熟了，然后找时间在系统的学几遍才能真正掌握 git 的强大

![image-20200906203735977](/Users/lei/Library/Application Support/typora-user-images/image-20200906203735977.png)

## Yield in Scrapy

![image-20200906203824890](/Users/lei/Library/Application Support/typora-user-images/image-20200906203824890.png)

![image-20200906203815767](/Users/lei/Library/Application Support/typora-user-images/image-20200906203815767.png)

这块确实讲的不透彻，就这张图来说，spider 中 yield xxx 以后，这个 xxx 会被传递到 scrapy 的 engine，然后 engine 去通过类似 if isinstance(xxx, XX): 这种方式来判断，xxx 是什么东西，如果是 item 就传给 pipelines 进行入库，如果是 scrapy.Request 实例对象 就传给 downloader 去继续下载.

云里雾里是因为你本身就对 yield 语法理解不深，然后现在还不够站在全局的角度来思考框架运作流程，这个不着急，咱们要多写几次才能慢慢的理解的，其实还是要进行反复练习的，我也写了好几个月爬虫才觉得编程入门了。

框架的核心在 engine，再加上 scheduler 去调度，完成整个流程，框架虽然极度复杂，但用起来还算简单

## Celery

![image-20200906204232093](/Users/lei/Library/Application Support/typora-user-images/image-20200906204232093.png)

![image-20200906204239459](/Users/lei/Library/Application Support/typora-user-images/image-20200906204239459.png)

都装一下看看，这个要想启动成功还挺麻烦的，等下时间来得及的话最好2倍速过一遍视频，稍微有个了解，能让他跑起来

## 前端知识

### 日期功能

![image-20200906204602737](/Users/lei/Library/Application Support/typora-user-images/image-20200906204602737.png)

![image-20200906204542833](/Users/lei/Library/Application Support/typora-user-images/image-20200906204542833.png)

嗯，有日期按钮肯定是 date 了😂

`input type="date"` 这种属性都是后加的功能，前端比较痛苦的一点就是浏览器兼容性问题，自己写一些功能的时候就要考虑兼容性，但是用 bootstrap 啥的他们把兼容性做好了，我们不用考虑。

Q：对我就发现，有些网站的页面没问题，但有些网站的页面就黑成一坨了完全看不清

A：这个应该是插件的问题，插件肯定不能考虑所有网页，有考虑不到的页正常

日期控件部分代码跟我写的一样吗
问题二应该是凌晨的时间，end 可以视图函数中处理下 + 一天，或者 + '23:59:59'

## TODO 卡断点问题

![image-20200906204652423](/Users/lei/Library/Application Support/typora-user-images/image-20200906204652423.png)

因为卡到断点了，所以会自动切到 PyCharm 界面，浏览器现在是显示不出来页面的，一直刷新状态

最后执行完 return render(request, 'products.html', context=context) 才会显示页面

整个断点执行完成，已经退出视图函数了

