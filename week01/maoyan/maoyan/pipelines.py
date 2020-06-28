# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import csv


class MaoyanPipeline:
    # item: 从爬虫文件maoyan.py中yield的item数据
    def process_item(self, item, spider):
        title = item['title']
        genres = item['genres']
        release_date = item['release_date']
        link = item['link']

        with open('maoyan.csv', mode='a+', encoding='utf_8_sig') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                title, genres, release_date, link
            ])

        return item
