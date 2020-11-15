# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    parsed_user = scrapy.Field()
    relation_type = scrapy.Field()
    user_id = scrapy.Field()
    username = scrapy.Field()
    full_name = scrapy.Field()
    photo = scrapy.Field()

