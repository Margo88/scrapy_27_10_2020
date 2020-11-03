# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import hashlib
from scrapy.utils.python import to_bytes
from pymongo import MongoClient

class LeruaparserPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongo_base = client.leroymerlin_items

    def process_item(self, item, spider):
        item['price'] = self.process_price(item['price'])
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_price(self, string):
        try:
            price = float(string.replace(' ', '').replace(',', '.'))
        except Exception as e:
            price = string
        return price

class LeroymerlinPicsPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['pics']:
            for pic in item['pics']:
                try:
                    yield scrapy.Request(pic)
                except Exception as e:
                    print(e)
        return item

    def item_completed(self, results, item, info):
        if results:
            item['pics'] = [i[1] for i in results if i[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f"/{item['part_number']}/{image_guid}.jpg"
