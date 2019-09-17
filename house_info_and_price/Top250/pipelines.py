# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Top250Pipeline(object):
    def process_item(self, item, spider):
        return item

from openpyxl import Workbook
import os
from urllib import request
class saveToExcel(object):
    def __init__(self):
        self.workbook = Workbook()
        self.sheet = self.workbook.active
        self.sheet.title = 'house'
        self.sheet.append('描述,总价,单价,户型,楼层,面积,套内面积,朝向,挂牌时间,交易权属,上次交易'.split(','))
    def process_item(self, item, spider):
        # item 是字典
        miaoshu = item['miaoshu']
        zongjia = item['zongjia']
        danjia = item['danjia']
        huxing = item['huxing']
        louceng = item['louceng']
        mianji = item['mianji']
        taoneimianji = item['taoneimianji']
        chaoxiang = item['chaoxiang']
        guapaishijian = item['guapaishijian']
        jiaoyiquanshu = item['jiaoyiquanshu']
        shangcijiaoyi = item['shangcijiaoyi']
        self.sheet.append([miaoshu,zongjia,danjia,huxing,louceng,mianji,taoneimianji,chaoxiang,guapaishijian,jiaoyiquanshu,shangcijiaoyi])
        return item
    # 当接收到 爬虫关闭时，将执行close_spider函数 ，spider 参数必须得有
    def close_spider(self,spider):
        self.workbook.save('../House.xlsx')
        print('excel 数据存储结束')
