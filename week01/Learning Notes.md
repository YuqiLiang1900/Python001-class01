# Learning Notes for Week One

## Objective for Week One
Web scrape key information of movies in Douban.com and Maoyan.com

## Knowledge tree
Two ways of web scraping: (1) Requests + Beautiful Soup / Regular Expression (2) Scrapy + XPath / Regular Expression

In essense, the proccess is the same: (1) send a request to the web server to get the source code of the webpage as the response; (2) extract the information which we want by bs4 / css / xpath / regular expression.

The mechanism of info extraction is extracting the nodes of the HTML web tree.
* Scrapy: selector class to extract information by XPath or CSS (https://www.accordbox.com/blog/scrapy-tutorial-8-scrapy-selector-guide/)

### Requests + Beautiful Soup
1. Requests

Requests allows you to send HTTP/1.1 requests extremely easily. There’s no need to manually add query strings to your URLs, or to form-encode your POST data. Keep-alive and HTTP connection pooling are 100% automatic, thanks to urllib3. Visit https://requests.readthedocs.io/en/master/user/quickstart/.

2. Beautiful Soup (bs4)

After sending a request, the web server will send us back a response. This response contains the source code of the web page, and status code, etc. To further extract the infomation which we want (in our case, the title, genres, release date and link of each movie), we need to use bs4.

Bs4 parses each HTML document into a complax tree data structure, in which every node of the tree is one of the four objects: (1) Beautiful Soup, (2) Tag, (3) Navigable String, and (4) Comment.

#### Important tips of bs4 syntax
1. Choosing a parser: do not use the default settings
2. attars


#### Some complementary projects
* A very intuitive tutorial on web scraping a Wikipedia webpage: https://www.pluralsight.com/guides/web-scraping-with-beautiful-soup
* Web scraping an e-commerce platform by bs4 and Selenium: https://towardsdatascience.com/in-10-minutes-web-scraping-with-beautiful-soup-and-selenium-for-data-professionals-8de169d36319

3. Tips while doing the assignment 1

#### Important parameters
* Setting up user agents: https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/
* Setting up cookies: 


### Scrapy + XPath

Response object also exposed a selector on selector attribute to make it convenient to use the selector. So in most cases, you can directly use it.

```python
>>> body = """
<html>
   <head>
      <title>Scrapy Tutorial Series By MichaelYin</title>
   </head>
   <body>
      <div class='links'>
         <a href='one.html'>Link 1<img src='image1.jpg'/></a>
         <a href='two.html'>Link 2<img src='image2.jpg'/></a>
         <a href='three.html'>Link 3<img src='image3.jpg'/></a>
      </div>
   </body>
</html>
"""
>>> sel = Selector(text=body)
>>> sel.xpath("//title/text()").extract()
[u'Scrapy Tutorial Series By MichaelYin']

>>> response = HtmlResponse(url="http://mysite.com", body=body, encoding='utf-8')
>>> Selector(response=response).xpath("//title/text()").extract()
[u'Scrapy Tutorial Series By MichaelYin']
```

When you use XPath or CSS method to select nodes from HTML, the output returned by the methods is SelectorList instance.

```python
[<Selector xpath='//a/@href' data=u'one.html'>,
 <Selector xpath='//a/@href' data=u'two.html'>,
 <Selector xpath='//a/@href' data=u'three.html'>]
 ```
 As you can see, SelectorList is a list of new selectors. If you want to get the textual data instead of SelectorList, just call .extract method.

```python
>>> response.selector.xpath('//a/@href').extract()
[u'one.html', u'two.html', u'three.html']
```

You can use extract_first to extract only first matched element, which can save you from extract()[0]

```python
>>> response.xpath("//a[@href='one.html']/img/@src").extract_first()
u'image1.jpg'
```
 

### Regular Expression
