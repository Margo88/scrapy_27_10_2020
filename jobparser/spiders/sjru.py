import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=kassir']

    def parse(self, response:HtmlResponse):
        links = response.xpath("//div/a[contains(@class , 'icMQ_ _6AfZ9')]/@href").extract()
        next_page = response.xpath("//div/a[contains(@class , 'f-test-link-Dalshe')]/@href").extract_first()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response:HtmlResponse):
        name = response.xpath("//h1/text()").extract_first()
        salary = response.xpath("//span/span[@class='_3mfro _2Wp8I PlM3e _2JVkc']/text()").extract()
        vacancy_link = response.url
        origin = self.allowed_domains[0]
        yield JobparserItem(name=name, salary=salary, vacancy_link=vacancy_link, origin=origin)
