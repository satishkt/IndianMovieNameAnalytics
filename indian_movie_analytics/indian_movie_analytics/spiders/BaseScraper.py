from indian_movie_analytics.items import IndianMoviesNameAnalyticsItem

__author__ = 'satish'

import logging
import locale

import scrapy
import string
from scrapy.selector import Selector
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


class BaseScraper(scrapy.Spider):
    handle_httpstatus_list = [404]
    _logger = logging.getLogger('indian_movie_analytics')
    _logger.setLevel(logging.INFO)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('movie-analytics-debug.log')
    fh.setLevel(logging.DEBUG)

    eh = logging.FileHandler('movie-analytics-error.log')
    eh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    eh.setFormatter(formatter)


    # add the handlers to logger
    _logger.addHandler(ch)
    _logger.addHandler(fh)
    _logger.addHandler(eh)

    pipeline=[]

    name = "IMASpider"
    allowed_domains = ["http://www.gomolo.com/"]
    seasons_list_urls = []
    parse_episode_urls = []
    base_url = "http://www.gomolo.com"

    search_strs = list(string.ascii_uppercase)
    search_strs.append('$')
    start_urls = ['http://www.gomolo.com/indian-movies-list-films-database?SearchChar=%s' % s for s in search_strs]


    start_urls =[
        "http://www.gomolo.com/indian-movies-list-films-database"
    ]

    def __init__(self):
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        self.failed_urls = []
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)


    def parse(self, response):
        self._logger.debug("In the response method for url %s", response.url)
        hxs = Selector(response)
        trs = hxs.xpath('//*[@id="divMain"]/table/tr')
        print trs
        for tr in trs[1:]:
            movie_url = tr.xpath('td[@class="res-cont-col1"]/a/@href').extract()
            movie_title = tr.xpath('td[@class="res-cont-col1"]/a/@title').extract()
            if len(movie_url) >= 1 :
                self._logger.debug(" Spawning a spider for movie %s  " % movie_title)
                yield scrapy.Request(movie_url[0], callback=self.page_detail)
                self.crawledPageUrls.append(movie_url[0])
            else:
                self._logger.err(tr.extract())

    def page_detail(self, response):
        self._logger.msg(response.url)
        hxs = Selector(response)
        item = IndianMoviesNameAnalyticsItem()
        movie_name  = hxs.xpath('//*[@id="LblMovieName"]/text()').extract()
        movie_year  = hxs.xpath('//*[@id="LblReleaseyear"]/text()').extract()
        language = hxs.xpath('//*[@id="lblLanguage"]/text()').extract()
        genre = hxs.xpath('//*[@id="divGenre"]/p/a/text()').extract()
        user_rating = hxs.xpath('//*[@id="divUserRating"]/span[2]/text()').extract()
        critic_rating = hxs.xpath('//*[@id="divExRate"]/span[2]/text()').extract()
        no_of_critics_rated = hxs.xpath('//*[@id="divExRate"]/span[2]/a/text()').extract()
        director = hxs.xpath('//*[@id="divDirc"]/p/a/text()').extract()
        producer = hxs.xpath('//*[@id="divProd"]/p/a[1]/text()').extract()
        music_dir = hxs.xpath('//*[@id="divMusicby"]/p/a/text()').extract()

        if len(movie_name) >=1 :
            item['movie_name'] = movie_name[0]
        if len(movie_year)>=1:
            item['year'] = movie_year[0]
        if len(language)>=1:
            item['language']= language[0]
        if len(genre) >=1:
            item['genre'] = genre[0]
        if len(user_rating) >=1:
            item['user_rating'] =user_rating[0]
        if len(critic_rating) >=1:
            item['critic_rating'] =critic_rating[0]
        if len(no_of_critics_rated) >= 1:
            item['no_of_critics_rated'] = no_of_critics_rated[0]
        if len(director)>=1:
            item['director'] =director[0]

        return item


    def handle_spider_closed(self, spider, reason): # added self
        self.crawler.stats.set_value('failed_urls',','.join(spider.failed_urls))

    def process_exception(self, response, exception, spider):
        ex_class = "%s.%s" % (exception.__class__.__module__,  exception.__class__.__name__)
        self._logger.error("Error url %s , Processing exception %s",response.url,ex_class)
        self.crawler.stats.inc_value('downloader/exception_count', spider=spider)
        self.crawler.stats.inc_value('downloader/exception_type_count/%s' % ex_class, spider=spider)


    def item_dropped(self,item,response,exception,spider):
        self._logger.error("Item dropped for url %s ",response.url)









