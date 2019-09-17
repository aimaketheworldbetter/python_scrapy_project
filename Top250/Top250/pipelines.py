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
        self.sheet.title = 'TOP250'
        self.sheet.append('电影名,导演,上映时间,电影评分,评论人数,简评,剧情简介'.split(','))
    def process_item(self, item, spider):
        # item 是字典
        name = item['name']
        director = item['director']
        release_time = item['release_time']
        score = item['score']
        comment_number = item['comment_number']
        brief_comment = item['brief_comment']
        related_info = item['related_info']
        #picture_web = item['picture_web']
        self.sheet.append([name,director,release_time,score,comment_number,brief_comment,related_info])
        return item
    # 当接收到 爬虫关闭时，将执行close_spider函数 ，spider 参数必须得有
    def close_spider(self,spider):
        self.workbook.save('../TOP250.xlsx')
        print('excel 数据存储结束')

class savePicture(object):
    def __init__(self):
        if os.path.exists('王勐'):
            os.chdir('王勐')
            if os.path.exists('images'):
                os.chdir('images')
            else:
                os.mkdir('images')
                os.chdir('images')
        else:
            os.mkdir('王勐')
            os.chdir('王勐')
            os.mkdir('images')
            os.chdir('images')
    def process_item(self, item, spider):
        # item 是字典
        name = item['name']
        picture_web = item['picture_web']
        request.urlretrieve(picture_web, name + '.jpg')
        return item
    # 当接收到 爬虫关闭时，将执行close_spider函数 ，spider 参数必须得有
    def close_spider(self,spider):
        print('图片存储完毕')