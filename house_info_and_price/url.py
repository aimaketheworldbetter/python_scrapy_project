# -*- coding: utf-8 -*-
# @Time    : 7/9/2019 10:16 PM
# @Author  : Meng Wang
# @File    : url.py
# @Software: PyCharm
import urllib.parse

word = '岳阳道'
word = urllib.parse.quote(word)
print(str(word))

word1 = '鞍山道'
word1 = urllib.parse.quote(word1)
print(word1)

xiaoqumingchenghanzi = [
    '岳阳道',
    '鞍山道'
]
xiaoqumingcheng = []
for word in xiaoqumingchenghanzi:
    word = urllib.parse.quote(word)
    xiaoqumingcheng.append(word)
    print(xiaoqumingcheng)
