import scrapy
from scrapy.selector import Selector
from maoyan.items import MaoyanItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['m.maoyan.com']
    start_urls = ['https://m.maoyan.com/?showType=3#movie/classic']
    film_number = 30 

    def start_requests(self):
        for i in range(0, (self.film_number + 1 - 10), 10):
            url = 'https://m.maoyan.com/ajax/moreClassicList?sortId=1&showType=3&limit=10'\
            '&offset={}&optimus_uuid=1EAC78C0B6EF11EAAF59052F3C3ECF63F9B57BD35D90469CA9D6'\
            '4879E1D591F1&optimus_risk_level=71&optimus_code=10'.format(i)
            print('url', url)
            yield scrapy.Request(url=url, callback=self.parse_channel_page)

    def parse_channel_page(self, response):

        # 给items.py中的类:MaoyanItem(scrapy.Item)实例化
        item = MaoyanItem()
        # Set a baseline xpath
        movies = Selector(response=response).xpath("//a")

        for movie in movies:

            title = movie.xpath(
                ".//div[@class='title line-ellipsis']/text()").extract_first()
            if title:
                item['title'] = title.strip()
            else:
                item['title'] = 'NaN'
            
            genres = movie.xpath(
                ".//div[@class='actors line-ellipsis']/text()").extract_first()
            if genres:
                item['genres'] = genres.strip()
            else:
                item['title'] = 'NaN'

            temp_release_date = movie.xpath(
                ".//div[@class='show-info line-ellipsis']/text()").extract_first()
            if temp_release_date is None:
                release_date = 'NaN'
            elif '-' in temp_release_date:
                release_date = temp_release_date.strip()[:10]
            elif '-' not in temp_release_date:
                release_date = temp_release_date.strip()[:4]
            item['release_date'] = release_date

            temp_link = movie.xpath(
                "./@href").extract_first()
            if temp_link:
                link = '{}{}'.format(self.allowed_domains[0], temp_link)
            else:
                link ='NaN'
            item['link'] = link

            # 把item对象交给管道文件处理
            yield item

