'''
1)Написать приложение, которое будет проходиться по указанному списку
двух и/или более пользователей и собирать данные об их подписчиках и подписках.
2) По каждому пользователю, который является подписчиком или на которого
подписан исследуемый объект нужно извлечь имя, id, фото (остальные данные по желанию).
Фото можно дополнительно скачать.
3) Собранные данные необходимо сложить в базу данных. Структуру данных нужно заранее продумать, чтобы:
4) Написать запрос к базе, который вернет список подписчиков только указанного пользователя
5) Написать запрос к базе, который вернет список профилей, на кого подписан указанный пользователь
'''

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from pymongo import MongoClient
from instaparser import settings
from instaparser.spiders.instagram import InstagramSpider

# client = MongoClient('127.0.0.1', 27017)
# db = client.instagram
# collection = db['my_stars']

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstagramSpider)

    process.start()

    # subscriptions = collection.find({'parsed_user': 'stas_mihailoff', 'relation_type': 'subscriptions'})
    # subscribers = collection.find({'parsed_user': 'stas_mihailoff', 'relation_type': 'subscribers'})
