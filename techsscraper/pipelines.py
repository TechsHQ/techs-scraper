# -*- coding: utf-8 -*-
import pymongo
import os

import hashlib

from util import get_db_name

class MongoDBPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=os.environ.get('MONGODB_URI', 'mongodb://localhost:27017'),
            mongo_db=get_db_name(os.environ.get('MONGODB_URI', 'mongodb://localhost:27017')) or 'blogs'
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        hash = hashlib.sha1(item['url'].encode('UTF-8')).hexdigest()
        self.db[spider.blog_name].update_one({'_id': hash}, {'$set': dict(item)}, upsert=True)
        return item
