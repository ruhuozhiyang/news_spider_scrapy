import json
from scrapy import Spider
from scrapy.http import Request
from scrapy.http import Response
from scrapy.http import FormRequest
from bs4 import BeautifulSoup
from ..items import NewsSpiderScrapyItem

TencentNewsUrl = 'https://pacaio.match.qq.com/irs/rcd'


# 要闻 https://pacaio.match.qq.com/pc/topNews?callback=__jp0
# https://pacaio.match.qq.com/irs/rcd?cid=108&ext=&token=349ee24cdf9327a050ddad8c166bd3e3&page=1&expIds=&callback=__jp1
# https://new.qq.com/cmsn/20180726/20180726A0QOLA00
# https://new.qq.com/ omn/20180726/20180726A0QOLA.html


def parse_news(response: Response):
    news = NewsSpiderScrapyItem()
    news['url'] = response.url
    soup = BeautifulSoup(response.text, "lxml")
    news['title'] = soup.find('div', class_='LEFT').h1.text
    news['content'] = ''
    article = soup.find_all('p', class_='one-p')
    for sentence in article:
        news['content'] += sentence.text
    print(news)
    # return news


def parse_contents(response: Response):
    try:
        data = json.load(response.text)
    except Exception:
        data = json.loads(response.text[(response.text.find('(') + 1):response.text.rfind(')')])

    try:
        data = data['data']
    except LookupError:
        pass
    for url in data:
        omn = url['vurl']
        if omn.endswith('00') and '/cmsn/' in omn:
            omn = omn.replace('/cmsn/', '/omn/')
            omn = omn[:omn.rfind('00')] + '.html'
        yield Request(url=omn, callback=parse_news)


class TencentSpider(Spider):
    name = 'news_scrapy'

    def parse(self, response, **kwargs):
        pass

    def start_requests(self):
        yield FormRequest(
            url=TencentNewsUrl,
            formdata={
                "cid": "58",
                "token": "c232b098ee7611faeffc46409e836360",
                "ext": "milite",
                "page": "0",
                "expIds": "",
                "callback": "__jp0"
            },
            callback=parse_contents,
            meta={
                "page": "0",
                "field": ""
            }
        )

