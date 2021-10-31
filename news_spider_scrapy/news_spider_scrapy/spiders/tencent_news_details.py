from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy_redis.spiders import RedisSpider
from ..items import NewsDetailItem

"""
redis中新闻url的消费者。消费完后redis中无数据.
"""


class TencentNewsDetail(RedisSpider):
    name = 'TencentNewsDetail'
    redis_key = 'tencent_detail_news_url'
    allowed_domains = ['qq.com']

    mobile_url = 'https://xw.qq.com/cmsid/{}'
    mobile_ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38' \
                ' (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'

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
        'REDIS_START_URLS_AS_SET': True,
        'ITEM_PIPELINES': {
        },
        'DOWNLOADER_MIDDLEWARES': {
        },
    }

    def parse(self, response, **kwargs):
        # url_ = self.mobile_url.format(response.url.split('/')[-1].split('.')[0])
        yield Request(
            url=response.url,
            callback=self.parse_detail,
            headers={
                'User-Agent': self.mobile_ua,
                'Referer': response.url
            }
        )

    def parse_detail(self, response):
        try:
            if response.url == 'https://xw.qq.com/404.html':
                return

            news = NewsDetailItem()
            """
            Re库是Python的标准库，主要用于字符串匹配；
            re.findall()搜索字符串，以列表类型返回全部能匹配的子串；
            常用标记re.S，正则表达式中的.操作符能够匹配所有字符，默认匹配除换行外的所有字符；
            """
            # data = ''.join(re.findall(r'globalConfig\s=\s(\{.*?\});', response.text, re.S))
            # json_data = demjson.decode(data)
            #
            # for k, v in zip(list(json_data.keys()), list(json_data.values())):
            #     item[k] = v
            # yield item
            news['url'] = response.url
            soup = BeautifulSoup(response.text, "lxml")
            news['title'] = soup.find('div', class_='LEFT').h1.text
            news['content'] = ''
            article = soup.find_all('p', class_='one-p')
            for sentence in article:
                news['content'] += sentence.text
        except Exception as e:
            self.logger.error('parse_content error {}, {}, {}'.format(e, response.url, response.text))
