import scrapy
import json
from ..items import NewsUrlItem
from scrapy.http import FormRequest


class TencentNewsScrapy(scrapy.Spider):
    name = 'TencentNewsScrapy'
    tencent_news_url = 'https://pacaio.match.qq.com/irs/rcd'

    custom_settings = {
        'CONCURRENT_REQUESTS': 64,
        'DOWNLOAD_DELAY': 0,
        'COOKIES_ENABLED': False,
        'LOG_LEVEL': 'INFO',
        'RETRY_TIMES': 15,
        'DEFAULT_REQUEST_HEADERS': {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,'
                      'image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
        },
        'REDIS_HOST': '127.0.0.1',
        'REDIS_PORT': '6379',
        'REDIS_DB': '0',  # 注意此处不要写db0.
        'ITEM_PIPELINES': {
            'news_spider_scrapy.pipelines.RedisUrlsPipeline': 301,
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 'qq_news.middlewares.ProxyMiddleware': 543,
        },
    }

    def start_requests(self):
        yield FormRequest(
            url=self.tencent_news_url,
            callback=self.parse,
            formdata={
                "cid": "58",
                "token": "c232b098ee7611faeffc46409e836360",
                "ext": "milite",
                "page": "0",
                "expIds": "",
                "callback": "__jp0"
            },
            meta={},
        )
        pass

    def parse(self, response, **kwargs):
        data = ''
        try:
            data = json.load(response.text)
        except Exception:
            data = json.loads(response.text[(response.text.find('(') + 1):response.text.rfind(')')])

        try:
            data = data['data']
        except Exception:
            pass
        for ele in data:
            print(ele['vurl'])
            item = NewsUrlItem()
            item['url'] = ele['vurl']
            yield item

