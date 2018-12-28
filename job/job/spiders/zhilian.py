# -*- coding: utf-8 -*-
import scrapy
import json,time,random
from job.items import JobItem


class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['zhaopin.com']
    start_urls = ['http://sou.zhaopin.com/']

    url = 'https://fe-api.zhaopin.com/c/i/sou?'
    headers = {
        'Host': 'fe-api.zhaopin.com',
        'Origin': 'https://sou.zhaopin.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
    }
    # kw = 'Java开发'
    # kw = 'Python'
    kw = 'PHP'#关键字
    page = 1#页码

    #发送请求
    def start_requests(self):
        yield scrapy.FormRequest(
            url = self.url,
            headers = self.headers,
            method = 'GET',
            formdata = {
                'start' :str((self.page-1)*90),
                'pageSize':'90',
                'workExperience':'-1',
                'education':'-1',
                'companyType':'-1',
                'employmentType':'-1',
                'jobWelfareTag':'-1',
                'kw': self.kw,
                'kt':'3',
                '_v': '0.84269824',
                'x-zp-page-request-id': '081b0f20bc5a4752a7db7315bce7fc06-1545653322592-595069'
            },
            callback=self.parse
        )

    # 数据处理
    def parse(self, response):
        item = JobItem()
        data = json.loads(response.text)
        result = data['data']['results'] #数据合集
        numfound = data['data']['numFound'] #总条数
        for message in result:
            item['city'] = message['city']['items'][0]['name']#城市
            item['jobname'] = message['jobName']#职位名称
            item['company'] = message['company']['name']#公司名称
            item['salary'] = message['salary']#工资
            item['welfare'] = ''
            for i in message['welfare']:
                item['welfare'] += i + ' '#福利待遇
            if len(message['city']['items']) == 2:
                item['address'] = message['city']['items'][1]['name']#区域
            else:
                item['address'] = ''
            item['education'] = message['eduLevel']['name']#学历要求
            item['workyear'] = message['workingExp']['name']#工作经验
            item['link'] = message['positionURL']#详情页网址
            item['createtime'] = message['updateDate']#添加时间
            yield item
        print('正在请求第%s页' % self.page)
        time.sleep(random.randint(1,10))#随机休眠

        if self.page < int(numfound/90) :#判断是否是最后一页
            self.page += 1
            yield scrapy.FormRequest(
                url=self.url,
                headers=self.headers,
                method='GET',
                formdata={
                    'start': str((self.page - 1) * 90),
                    'pageSize': '90',
                    'workExperience': '-1',
                    'education': '-1',
                    'companyType': '-1',
                    'employmentType': '-1',
                    'jobWelfareTag': '-1',
                    'kw': self.kw,
                    'kt': '3',
                    '_v': '0.84269824',
                    'x-zp-page-request-id': '081b0f20bc5a4752a7db7315bce7fc06-1545653322592-595069'
                },
                callback=self.parse
            )
            return self.parse








