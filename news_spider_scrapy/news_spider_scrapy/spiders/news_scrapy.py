import scrapy


class NewsScrapySpider(scrapy.Spider):
    name = 'news_scrapy'
    allowed_domains = ['tencent.com']
    start_urls = ['http://tencent.com/']

    def parse(self, response):
        pass
