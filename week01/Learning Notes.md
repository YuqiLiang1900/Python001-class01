# Learning Notes for Week One

## Objective for Week One
Web scrape key information of movies in Douban.com and Maoyan.com

## Knowledge tree
Two ways of web scraping: (1) Requests + Beautiful Soup / Regular Expression (2) Scrapy + XPath / Regular Expression

### Requests + Beautiful Soup
1. Requests

Requests allows you to send HTTP/1.1 requests extremely easily. There’s no need to manually add query strings to your URLs, or to form-encode your POST data. Keep-alive and HTTP connection pooling are 100% automatic, thanks to urllib3. Visit https://requests.readthedocs.io/en/master/user/quickstart/.

2. Beautiful Soup (bs4)

After sending a request, the web server will send us back a response. This response contains the source code of the web page, and status code, etc. To further extract the infomation which we want (in our case, the title, genres, release date and link of each movie), we need to use bs4.

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


### Regular Expression
