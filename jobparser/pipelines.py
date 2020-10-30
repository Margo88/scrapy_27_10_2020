# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongo_base = client.job_scrapy

    def process_item(self, item, spider):
        item['min_salary'], item['max_salary'], item['currency'] = self.process_salary(item['salary'])
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_salary(self, salary):
        if ' на руки' in salary:
            currency = salary[-2]
        elif len(salary) == 1:
            currency = None
        else:
            currency = re.sub(r'\d+', '', salary[-1])

        b = [i.replace('\xa0', '') for i in salary if re.match(r'\d+', i)]
        print(b)
        if len(b) == 0:
            salary_min = None
            salary_max = None
        elif salary[0] == 'до':
            salary_min = None
            salary_max = re.sub(r'[а-я\.a-z]', '', b[0])
        elif len(b) == 2:
            salary_min = re.sub(r'[а-я\.a-z]', '', b[0])
            salary_max = re.sub(r'[а-я\.a-z]', '', b[1])
        else:
            salary_min = re.sub(r'[а-я\.a-z]', '', b[0])
            salary_max = None
        return [salary_min, salary_max, currency]
