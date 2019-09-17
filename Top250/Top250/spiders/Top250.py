# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from Top250.items import Top250Item
from scrapy.http import Request
from copy import deepcopy
import re

class Top250Spider(CrawlSpider):
    counts = 0
    name = 'Top250'
    # 我们也可以不用去setting内设置 pipeline ，middleware
    # 即使 setting文件内用，也不生效
    custom_settings = \
        {
            'ITEM_PIPELINES':
                {
                    'Top250.pipelines.saveToExcel': 300, # 0-1000 的值，先后顺序
                    'Top250.pipelines.savePicture': 360,  # 0-1000 的值，先后顺序
                },
            'DOWNLOADER_MIDDLEWARES' :
                {
                    'Top250.middlewares.Top250DownloaderMiddleware': 543,
                }

        }

    start_urls = [
        'https://movie.douban.com/top250'
    ]
    def parse(self, response):
        self.counts +=1
        print('正在处理第',self.counts,'页')
        items = Top250Item()
        selector = Selector(response)
        #######有些情况导演很多，名字很长，网页中没有‘主’这个字，取不到导演的名字。有待改进######
        reg1 = re.compile('导演: (.*?)主.*?')
        # 提取内容
        divs = selector.xpath('//div[@class="item"]')
        #使用 for 去处理
        for each in divs:
            # .extract() 返回对应的字符串
            # xpath得到的是 列表 类型的数据
            name = each.xpath('div[@class="info"]/div[@class="hd"]/a/span[@class="title"][1]/text()').extract()
            directorStr = each.xpath('div[@class="info"]/div[@class="bd"]/p[@class=""]/text()').extract()[0].strip()
            director = re.findall(reg1,directorStr)
            #######没有取到导演的名字，给一个默认值h######
            if director==[]:
                director=['h']
            #print(director)
            release_timeStr = each.xpath('div[@class="info"]/div[@class="bd"]/p[@class=""]/text()').extract()[1]
            release_time = re.sub("\D", "", release_timeStr)
            score = each.xpath('div[@class="info"]/div[@class="bd"]/div/span[@class="rating_num"]/text()').extract()
            comment_numberStr = each.xpath('div[@class="info"]/div[@class="bd"]/div/span[4]/text()').extract()[0]
            comment_number = re.sub("\D", "", comment_numberStr)
            brief_comment = each.xpath('div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            #######有些情况没有简评，给一个默认值‘无’######
            if brief_comment==[]:
                brief_comment = ['无']
            picture_web = each.xpath('div[@class="pic"]/a//@src').extract()
            # 赋值 给 items
            items['name'] = name[0]
            items['director'] = director[0]
            items['release_time'] = release_time
            items['score'] = score[0]
            items['comment_number'] = comment_number
            items['brief_comment'] = brief_comment[0]
            items['picture_web'] = picture_web[0]
            #yield items
            # 爬取详情页得 ,每一条都要用请求去处理，也将就是提交请求
            # 获取工作的地址
            related_info_web = each.xpath('div[@class="info"]/div[@class="hd"]/a/@href').extract()[0]
            # 把请求 和 已经 有部分数据的items 传给 解析详情页的函数，
            # items需要 深度拷贝，否则会有重复数据 from copy import deepcopy
            yield Request(related_info_web, meta={'front_item':deepcopy(items)},callback=self.parse_detail,dont_filter=True)

        # 获取下一页的链接。一定要注意一样事情，在for之外获取
        nextLink = selector.xpath('//span[@class ="next"]/link/@href').extract()
    # 第 10 页是最后一页，没有下一页的链接
        if nextLink:
            nextLink = nextLink[0]
            print(nextLink)
            yield Request(self.start_urls[0] + nextLink, callback=self.parse) # 递归将下一页的地址传给这个函数自己， 再 进行爬


    # ###########写个函数处理详情页，取出来的东西没有一致性，需要改进这个函数#############
    def parse_detail(self, response):
        # 接收 传过来的item
        items = response.meta['front_item']
        selector = Selector(response)
        # 提取信息
        # 因为有网页的不同，我们最好用 try 去获取内容
        #div = selector.xpath('//div[@class="related-info"]')
        related_info1 = selector.xpath('//div[@class="related-info"]/h2/i/text()').extract()
        related_info2 = selector.xpath('//div[@class="related-info"]//span/text()').extract()
        if related_info1 == []:
            related_info1 = ['无']
        if len(related_info2) < 2:
            related_info2 = ['无','无']
        items['related_info'] = related_info1[0] + ':' + related_info2[1]
        # 最后别忘了 把 items 提交上去
        yield items

