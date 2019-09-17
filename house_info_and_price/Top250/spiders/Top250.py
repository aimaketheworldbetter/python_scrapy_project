# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from Top250.items import Top250Item
from scrapy.http import Request
from copy import deepcopy
import urllib.parse
import time

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
                    #'Top250.pipelines.savePicture': 360,  # 0-1000 的值，先后顺序
                },
            'DOWNLOADER_MIDDLEWARES' :
                {
                    'Top250.middlewares.Top250DownloaderMiddleware': 543,
                }

        }
    main_page = 'https://tj.ke.com/ershoufang/rs'
    xiaoqumingchenghanzi = [
        '金旭园',
        '鞍山道',
        '岳阳道'
    ]
    xiaoqumingcheng = []
    for word in xiaoqumingchenghanzi:
        word = urllib.parse.quote(word)
        xiaoqumingcheng.append(word)

    start_urls = [
        main_page+xiaoqumingcheng[0]
    ]

    def parse(self, response):
        self.counts +=1
        # print('正在处理第',self.counts,'页')
        items = Top250Item()
        selector = Selector(response)
        # 提取内容
        divs = selector.xpath('//li[@class="clear"]')
        #使用 for 去处理
        for each in divs:

            # .extract() 返回对应的字符串
            # xpath得到的是 列表 类型的数据
            related_info_web = each.xpath('a/@href').extract()[0]
            danjia = each.xpath('div[@class="info clear"]/div[@class="address"]/div[@class="priceInfo"]/div[@class="unitPrice"]/span/text()').extract()[0]
            zongjia = each.xpath('div[@class="info clear"]/div[@class="address"]/div[@class="priceInfo"]/div[@class="totalPrice"]/span/text()').extract()[0]
            # 赋值 给 items
            # items['houseinfo'] = houseinfo
            # items['staricon'] = staricon
            danjia = danjia[2:8]
            items['zongjia'] = zongjia
            items['danjia'] = danjia
            # yield items
            # 爬取详情页得 ,每一条都要用请求去处理，也将就是提交请求
            # 获取工作的地址
            #related_info_web = each.xpath('div[@class="info"]/div[@class="hd"]/a/@href').extract()[0]
            # 把请求 和 已经 有部分数据的items 传给 解析详情页的函数，
            # items需要 深度拷贝，否则会有重复数据 from copy import deepcopy
            yield Request(related_info_web,meta={'front_item':deepcopy(items)},callback=self.parse_detail,dont_filter=True)
        # 获取下一页的链接。一定要注意一样事情，在for之外获取
        if self.counts < len(self.xiaoqumingcheng):
            nextLink = self.main_page+self.xiaoqumingcheng[self.counts]
            print(nextLink)
            time.sleep(2)
            yield Request(nextLink, callback=self.parse) # 递归将下一页的地址传给这个函数自己， 再 进行爬


    # ###########写个函数处理详情页，取出来的东西没有一致性，需要改进这个函数#############
    def parse_detail(self, response):
        time.sleep(2)
        items = response.meta['front_item']
        selector = Selector(response)

        div1 = selector.xpath('//div[@class="introContent"]//li/span/text()').extract()
        div2 = selector.xpath('//div[@class="introContent"]//li/text()').extract()
        #miaoshu = selector.xpath('//div[@class="detailHeader VIEWDATA"]//h1/@title').extract()
        miaoshu = selector.xpath('//div[@class="detailHeader VIEWDATA"]//h1/@title').extract()[0]
        items['miaoshu'] = miaoshu
        if len(div1)>2:
            div1.pop(-2)
            div1.pop(-2)
        huxing = "无"
        louceng = "无"
        mianji = "无"
        taoneimianji = "无"
        chaoxiang = "无"
        guapaishijian = "无"
        jiaoyiquanshu = "无"
        shangcijiaoyi = "无"
        for name, value in zip(div1,div2):
            value.replace("\n","").replace(" ","").replace("n","")
            if name=="房屋户型":
                huxing=value
            elif name=="所在楼层":
                louceng=value
            elif name=="建筑面积":
                mianji=value
            elif name=="套内面积":
                taoneimianji=value
            elif name=="房屋朝向":
                chaoxiang=value
            elif name=="挂牌时间":
                guapaishijian=value
            elif name=="交易权属":
                jiaoyiquanshu=value
            elif name=="上次交易":
                shangcijiaoyi=value

        items['huxing'] = huxing
        items['louceng'] = louceng
        items['mianji'] = mianji
        items['taoneimianji'] = taoneimianji
        items['chaoxiang'] = chaoxiang
        items['guapaishijian'] = guapaishijian[:11]
        if jiaoyiquanshu[:2] == "私产":
            items['jiaoyiquanshu'] = jiaoyiquanshu[:2]
        else:
            items['jiaoyiquanshu'] = jiaoyiquanshu[:3]
        items['shangcijiaoyi'] = shangcijiaoyi[:10]
    #     # 最后别忘了 把 items 提交上去
        yield items
