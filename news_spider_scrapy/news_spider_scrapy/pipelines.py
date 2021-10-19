# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import redis
import pymongo


class RedisUrlsPipeline(object):

    def __init__(self, redis_host, redis_port, redis_db):
        self.redis_client = redis.StrictRedis(
            host=redis_host, port=redis_port, db=redis_db)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def process_item(self, item, spider):
        if type(item).__name__ == 'NewsUrl':
            redis_key = 'tencent_news:start_url'
            self.redis_client.sadd(redis_key, item['url'])
            spider.logger.debug(
                '===== Success push start_urls to REDIS with url {} ====='.format(item['url']))
            return item
