# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    jobname = scrapy.Field() #职位名称
    city = scrapy.Field()#城市
    company = scrapy.Field()#公司名称
    salary = scrapy.Field()#薪水
    welfare = scrapy.Field()#福利
    address = scrapy.Field()#公司地址
    education = scrapy.Field()#学历要求
    workyear = scrapy.Field()#工作经验
    createtime = scrapy.Field()#发布时间
    link = scrapy.Field()#详情页网址

