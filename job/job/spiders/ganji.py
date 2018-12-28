# -*- coding: utf-8 -*-
import scrapy
from job.items import JobItem
import re,time,random
from bs4 import BeautifulSoup

class GanjiSpider(scrapy.Spider):
    name = 'ganji'
    allowed_domains = ['bj.ganji.com']
    start_urls = ['http://bj.ganji.com/']
    page = 2
    url = 'http://bj.ganji.com/zpjisuanjiwangluo/o%s/' % str(page)

    # 发送请求
    def start_requests(self):
        yield scrapy.FormRequest(
            url=self.url,
            method='GET',
            callback=self.parse
        )

    def parse(self, response):
        item = JobItem()
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        result = soup.find_all(attrs={'class': 'list-noimg job-list clearfix new-dl'})
        print(result[1])
        for message in result:
            job_soup = BeautifulSoup(str(message), 'html.parser')
            item['city'] = '北京'  #城市
            item['education'] = '不限'  # 学历要求
            item['workyear'] = '不限'  # 工作经验
            item['jobname'] = job_soup.find(attrs={'list_title gj_tongji'}).string
            item['company'] = job_soup.find(attrs={'new-dl-company'}).a['title']
            item['salary'] = ''.join(re.findall('\S+',str(job_soup.find(attrs={'class':'new-dl-salary'}).string)))
            item['link'] = job_soup.find(attrs={'class': 'list_title gj_tongji'})['href']
            if '-' in str(job_soup.find(attrs={'pub-time'}).span.string):
                item['createtime'] ='2018-' + str(job_soup.find(attrs={'pub-time'}).span.string)
            elif str(job_soup.find(attrs={'pub-time'}).span.string) == '昨天':
                item['createtime'] ='2018-12-25'
            else:
                item['createtime'] ='2018-12-26'
            item['address'] = job_soup.find(attrs={'class':'pay'}).string
            try:
                item['welfare'] =job_soup.find(attrs={'class':'new-dl-tags'}).find('i').string
            except:
                item['welfare'] = ''
            yield item

        print('正在请求第%s页' % self.page)
        time.sleep(random.randint(1, 10))  # 随机休眠
        if self.page < 100:
            self.page += 1
            yield scrapy.FormRequest(
                url='http://bj.ganji.com/zpjisuanjiwangluo/o%s/' % str(self.page),
                method='GET',
                callback=self.parse,
                dont_filter=True
            )
            return self.parse
