# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Top250Item(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    director = scrapy.Field()
    release_time = scrapy.Field()
    score = scrapy.Field()
    comment_number = scrapy.Field()
    brief_comment = scrapy.Field()
    related_info = scrapy.Field()
    picture_web = scrapy.Field()
    pass
