# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Dribbble1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 图片的链接
    img_url = scrapy.Field()
    # 图片的名字
    img_name = scrapy.Field()
    # 设计师名字
    designer = scrapy.Field()
    # 喜欢的次数
    like_count = scrapy.Field()
    # 浏览的次数
    watch_count = scrapy.Field()
    # 评论的次数
    talk_count = scrapy.Field()
    # 图片发行日期
    img_date = scrapy.Field()
    # 图片标签
    img_tag = scrapy.Field()
    # 图片描述
    img_info = scrapy.Field()

