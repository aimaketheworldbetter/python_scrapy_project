# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Top250Item(scrapy.Item):
    # define the fields for your item here like:
    zongjia = scrapy.Field()
    danjia = scrapy.Field()
    miaoshu = scrapy.Field()
    huxing = scrapy.Field()
    louceng = scrapy.Field()
    mianji = scrapy.Field()
    taoneimianji = scrapy.Field()
    chaoxiang = scrapy.Field()
    guapaishijian = scrapy.Field()
    jiaoyiquanshu = scrapy.Field()
    shangcijiaoyi = scrapy.Field()
    pass
