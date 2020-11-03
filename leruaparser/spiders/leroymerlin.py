import scrapy
from scrapy.http import HtmlResponse
from leruaparser.items import LeruaparserItem
from scrapy.loader import ItemLoader

class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//product-card//a[@slot='name']")
        next_page = response.xpath("//div/a[@navy-arrow='next']/@href").extract_first()
        for link in links:
            yield response.follow(link, callback=self.item_parse)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def item_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaparserItem(), response=response)
        loader.add_xpath('part_number', "//span[@slot='article']/@content")
        loader.add_xpath('name', "//h1[@slot='title']/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_value('link', response.url)
        loader.add_xpath('pics', "//picture[@slot='pictures']/source[@media=' only screen and (min-width: 1024px)']/@srcset")
        loader.add_xpath('features', '//section[@id="nav-characteristics"]')
        yield loader.load_item()