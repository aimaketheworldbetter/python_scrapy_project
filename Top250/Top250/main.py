# -*- coding: utf-8 -*-
# @Time    : 12/18/2018 8:33 PM
# @Author  : Meng Wang
# @File    : main.py
# @Software: PyCharm
from scrapy import cmdline
cmdline.execute('scrapy crawl Top250'.split())