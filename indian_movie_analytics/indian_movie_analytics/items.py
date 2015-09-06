# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field
from collections import defaultdict


class IndianMoviesNameAnalyticsItem(scrapy.Item):

    fields = defaultdict(scrapy.Field)

    ###If you find a field that is not in the fields listed
    #in the class,  then add the fields into the internal dict.

    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key] = scrapy.Field()
        super(IndianMoviesNameAnalyticsItem, self).__setitem__(key, value)

    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_name = Field()
    year = Field()
    language = Field()
    genre = Field()
    user_rating = Field()
    no_of_users_rated = Field()
    critic_rating = Field()
    no_of_critics_rated = Field()
    director = Field()
    producer = Field()
    music_director = Field()
    main_cast = Field()
    banner = Field()
    release_date = Field()
    awards = Field()


