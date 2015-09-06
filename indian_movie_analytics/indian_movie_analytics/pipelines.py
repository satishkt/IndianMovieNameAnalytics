# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import functools
import scrapy
import json
import codecs


class IndianMovieAnalyticsPipeline(object):
    def process_item(self, item, spider):
        return item


def check_spider_pipeline(process_item_method):
    @functools.wraps(process_item_method)
    def wrapper(self, item, spider):
        # message template for debugging
        msg = '%%s %s pipeline step' % (self.__class__.__name__,)

        # if class is in the spider's pipeline, then use the
        # process_item method normally.
        if self.__class__ in spider.pipeline:
            # spider.log(msg % 'executing', level=log.DEBUG)
            return process_item_method(self, item, spider)

        # otherwise, just return the untouched item (skip this step in
        # the pipeline)
        else:
            # spider.log(msg % 'skipping', level=log.DEBUG)
            return item


    return wrapper


class JsonMovieAnalyticsPipeline(scrapy.Item):
    def __init__(self):
        self.file = codecs.open('indian_movie_analytics.json', 'wb', encoding='utf-8')

    @check_spider_pipeline
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()
