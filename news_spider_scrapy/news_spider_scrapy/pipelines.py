# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import redis


class RedisUrlsPipeline(object):

    def __init__(self, redis_host, redis_port, redis_db):
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

    # 是一个类方法，是一种依赖注入的方式.
    # 通过crawler对象，我们可以拿到Scrapy的所有核心组件，如全局配置的每个信息，然后创建一个Pipeline实例.
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            redis_host=crawler.settings.get('REDIS_HOST'),
            redis_port=crawler.settings.get('REDIS_PORT'),
            redis_db=crawler.settings.get('REDIS_DB'),
        )

    # process_item()是必须要实现的方法，被定义的Item Pipeline会默认调用这个方法对Item进行处理.
    def process_item(self, item, spider):
        if type(item).__name__ == 'NewsUrl':
            redis_key = 'tencent_news:start_url'
            self.redis_client.sadd(redis_key, item['url'])
            spider.logger.debug(
                '===== Success push start_urls to REDIS with url {} ====='.format(item['url']))
            return item
