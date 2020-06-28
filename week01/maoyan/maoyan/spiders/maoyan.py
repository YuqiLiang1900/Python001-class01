import scrapy
from scrapy.selector import Selector
from maoyan.items import MaoyanItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['m.maoyan.com']
    start_urls = ['https://m.maoyan.com/?showType=3#movie/classic']
    film_number = 10

    def start_requests(self):
        for i in range(0, (self.film_number + 1 - 10), 10):
            url = 'https://m.maoyan.com/ajax/moreClassicList?sortId=1&showType=3&limit=10&offset={}\
                &optimus_uuid=1EAC78C0B6EF11EAAF59052F3C3ECF63F9B57BD35D90469CA9D64879E1D591F1&optimus_risk_level=71\
                    &optimus_code=10'.format(i)
            yield scrapy.Request(url=url, callback=self.parse_channel_page)

    def parse_channel_page(self, response):

        # 给items.py中的类:MaoyanItem(scrapy.Item)实例化
        item = MaoyanItem()

        # Set a baseline xpath
        movies = Selector(response=response).xpath("//a")

        for movie in movies:

            title = movie.xpath(
                ".//div[@class='title line-ellipsis']/text()").extract_first().strip()
            genres = movie.xpath(
                ".//div[@class='actors line-ellipsis']/text()").extract_first().strip()
            release_date = movie.xpath(
                ".//div[@class='show-info line-ellipsis']/text()").extract_first().strip()[:10]

            temp_link = movie.xpath(
                "./@href").extract_first()
            link = '{}{}'.format(self.allowed_domains[0], temp_link)

            item['title'] = title
            item['genres'] = genres
            item['release_date'] = release_date
            item['link'] = link

            # print('title:', title)
            # print('genres:', genres)
            # print('release_date:', release_date)
            # print('link:', link)

            # 把item对象交给管道文件处理
            yield item

