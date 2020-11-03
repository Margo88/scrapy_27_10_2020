# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from scrapy.http import HtmlResponse

def get_features(string):
    features = {}
    response = HtmlResponse(url="_", body=string, encoding='utf-8')
    all_features = response.xpath("//div[@class='def-list__group']")
    for f in all_features:
        type = f.xpath('.//dt/text()').extract_first()
        value = f.xpath('.//dd/text()').extract_first()
        features[type] = value.replace('  ', '').replace('\n', '')
    return features

class LeruaparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    part_number = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    pics = scrapy.Field()
    features = scrapy.Field(input_processor=MapCompose(get_features), output_processor=TakeFirst())