# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http.request import Request
from Dribbble1.items import Dribbble1Item


class DribbbleSpider(scrapy.Spider):
    name = 'dribbble'
    allowed_domains = ['dribbble.com']
    baseUrl = "https://dribbble.com"
    # 要登录的网址
    # LoginUrl = "https://dribbble.com/session/new"
    # 起始抓取数据的网址
    start_urls = ['https://dribbble.com/places']

    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    # 处理start_urls里的登录的响应内容，提取登录需要的参数

    def start_requests(self):
        yield scrapy.Request("https://dribbble.com/session/new", callback=self.parse)

    def post_login(self, response):
        # 下面这句话用于抓取请求网页后返回网页中的_xsrf字段的文字, 用于成功提交表单
        authenticity_token = response.xpath("//input[@name='authenticity_token']/@value").extract()[0]
        # FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
        # 登陆成功后, 会调用after_login回调函数
        yield scrapy.FormRequest.from_response(response,
                                               headers = self.header,  # 注意此处的headers
                                               formdata={
                                               "authenticity_token" : authenticity_token,
                                               "login" : "547134028@qq.com",
                                               "password" : "hc123456"
                                               },
                                               callback=self.parse,
                                               )

    # def parse(self, response):
    #     # 提取登录需要的参数
    #     authenticity_token = response.xpath("//input[@name='authenticity_token']/@value").extract()[0]
    #     # 发送请求，并调用指定回调函数
    #     yield scrapy.FormRequest.from_response(
    #         response,
    #         formdata = {
    #             "authenticity_token" : authenticity_token,
    #             "login" : "xuxin1994",
    #             "password" : "xx941214,.,"
    #         },
    #         callback=self.parse_page
    #     )

    # 登录后访问的页面
    def parse(self, response):
        # url = "https://dribbble.com/shots"
        for url in self.start_urls:
            yield Request(url, headers=self.header, callback=self.parse_links)


    # 各组合分类链接
    def parse_links(self, response):
        # 各国家城市
        urls = response.xpath("//ol[@class='places-list group']//li/a/@href").extract()
        for url in urls:
            url = self.baseUrl + url
            yield scrapy.Request(url, headers=self.header, callback=self.parse_imgLink)
        # urls1 = response.xpath("//li[@class='more active'][2]//a/@href").extract()
        # urls2 = response.xpath("//li[@class='more active'][1]//a/@href").extract()
        # urls3 = response.xpath("//li[@class='more active'][3]//a/@href").extract()
        # # page为50之内
        # for url1 in urls1:
        #     url1 = self.baseUrl + url1
        #     for i in range(50):
        #         img_link = url1 + '&page=' + str(i)
        #         yield Request(url=img_link, headers=self.header, callback=self.parse_imgLink)
        # for url2 in urls2:
        #     url2 = self.baseUrl + url2
        #     for i in range(50):
        #         img_link = url2 + '&page=' + str(i)
        #         yield Request(url=img_link, headers=self.header, callback=self.parse_imgLink)
        # for url3 in urls3:
        #     url3 = self.baseUrl + url3
        #     for i in range(50):
        #         img_link = url3 + '&page=' + str(i)
        #         yield Request(url=img_link, headers=self.header, callback=self.parse_imgLink)


    # 处理响应内容
    def parse_imgLink(self, response):
        # item = Dribbble1Item()
        # img_urls = response.xpath('//picture//source[1]/@srcset').extract()
        # item = Dribbble1Item()
        # designers = response.xpath('//a[@class="url hoverable"]/text()').extract()
        # likes = response.xpath('//div[@id="main"]//li//li//a/text()').extract()
        # watchs = response.xpath('//li[@class="views"]//span/text()').extract()
        # talks = response.xpath('//li[@class="cmnt"]/span/text()').extract()
        # infos = response.xpath('//*/div/div[1]/div/a[2]/span/text()').extract()
        # img_names = response.xpath('//div[@id="main"]//a//strong/text()').extract()
        # for talk in talks:
        #     item['talk_count'] = talk.strip()
        # item = Dribbble1Item()
        # for url in img_urls:
        #     # item = Dribbble1Item()
        #     # item['designer'] = designer
        #     item['img_url'] = url
        #     # 返回数据
        #     # yield item
        # for designer in designers:
        #     # item = Dribbble1Item()
        #     item['designer'] = designer
        #     yield item
        # item['designer'] = designers
        # item['like_count'] = likes
        # item['watch_count'] = watchs
        # # item['talk_count'] = talk.strip()
        # item['img_info'] = infos
        # item['img_name'] = img_names

        img_sets = response.xpath('//div[@class="dribbble-img"]/a[1]/@href').extract()
        for img_set in img_sets:
            img_set = self.baseUrl + img_set
            yield Request(url=img_set, headers=self.header, callback=self.parse_imgUrl)

    def parse_imgUrl(self, response):
        # data = json.loads(response.body.decode('utf-8'))
        # print("===========")
        # print(data)
        # print("===========")
        item = Dribbble1Item()
        designers = response.xpath('//span[@class="shot-byline-user"]/a/text()').extract()
        # for designer in designers:
        #     item['designer'] = designer
        like_counts = response.xpath('//a[@class="likes-count stats-num"]/text()').extract()
        print("===========")
        print(like_counts)
        print("===========")
        # for like_count in like_counts:
        item['like_count'] = like_counts
        watch_counts = response.xpath('//span[@class="views-count stats-num"]/text()').extract()
        print("===========")
        print(watch_counts)
        print("===========")
        # for watch_count in watch_counts:
        item['watch_count'] = watch_counts
        talk_counts = response.xpath('//div[@class="screenshot-info-wrapper"]//div/h2/text()').extract()
        print("===========")
        print(talk_counts)
        print("===========")
        # for talk_count in talk_counts:
        item['talk_count'] = talk_counts
        img_infos = response.xpath('//div[@class="shot-desc"]/p/text()').extract()
        # for img_info in img_infos:
        #     item['img_info'] = img_info
        img_names = response.xpath('//div[@id="content"]//h1/text()').extract()
        # for img_name in img_names:
        #     item['img_name'] = img_name
        # m = response.meta['meta']
        img_dates = response.xpath('//span[@class="shot-byline-date"]/a/text()').extract()
        # for img_date in img_dates:
        #     item['img_date'] = img_date
        img_urls = response.xpath('//div[@class="single-img"]//img/@src').extract()
        img_tags = response.xpath('//li[@class="tag"]//strong/text()').extract()
        try:
            item['img_tag'] = ','.join(img_tags)
        except Exception as e:
            item['img_tags'] = ''
        item['designer'] = designers
        # item['like_count'] = like_counts.strip()
        # item['watch_count'] = watch_counts.strip()[0]
        # item['talk_count'] = talk_counts.strip()[0]
        item['img_info'] = img_infos
        item['img_name'] = img_names
        # item['img_tag'] = img_tags
        item['img_url'] = img_urls
        item['img_date'] = img_dates
        yield item
