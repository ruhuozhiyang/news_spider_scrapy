# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class NewsUrlItem(scrapy.Item):
    url = scrapy.Field()
    pass


class NewsDetailItem(scrapy.Item):
    url = scrapy.Field()    # 文章链接
    title = scrapy.Field()  # 标题
    content = scrapy.Field()  # 正文内容
    author = scrapy.Field()  # 作者
    date = scrapy.Field()  # 日期
    summary = scrapy.Field()  # 大纲
    pass
