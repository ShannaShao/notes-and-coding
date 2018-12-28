# -*- coding: utf-8 -*-
import scrapy
from job.items import JobItem
import re,time,random
from bs4 import BeautifulSoup


# 前程无忧网
class Qiancheng51Spider(scrapy.Spider):
    name = 'qiancheng51'
    allowed_domains = ['51job.com']
    start_urls = ['http://www.51job.com/']

    base_url = 'https://search.51job.com/list/000000,000000,0000,32,9,99,'
    kw = 'Java' #关键字在
    page = 1 #页码
    w_url = '.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    # 拼接url
    url = base_url + kw + ',2,' + str(page) + w_url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
    }

    # 发送请求
    def start_requests(self):
        yield scrapy.FormRequest(
            url=self.url,
            headers=self.headers,
            method='GET',
            callback=self.parse
        )

    def parse(self, response):
        item = JobItem()
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        # 全部页数
        allpage = int(re.match('共(\d+)页，到第', soup.find(attrs={'class': 'td'}).string).group(1))
        # 职位结果
        result = soup.find_all(attrs={'class':'el'})[16:]
        print(result)
        for message in result:
            job_soup = BeautifulSoup(str(message), 'html.parser')
            if '-' in str(job_soup.find(attrs={'class':'t3'}).string):
                split = str(job_soup.find(attrs={'class':'t3'}).string).split('-')
                item['city'] = split[0]#城市
                item['address'] = split[1]#区域
            else:
                item['city'] = str(job_soup.find(attrs={'class':'t3'}).string)
                item['address'] = ''
            item['jobname'] = ''.join(re.findall('\S+',str(job_soup.a.string)))  # 职位名称
            item['company'] = str(job_soup.find(attrs={'class':'t2'}).string)  # 公司名称
            item['salary'] = str(job_soup.find(attrs={'class':'t4'}).string) # 工资
            item['welfare'] = '' # 福利待遇
            item['education'] = '不限'  # 学历要求
            item['workyear'] = '不限'  # 工作经验
            item['link'] = str(job_soup.a['href'])  # 详情页网址
            item['createtime'] = '2018-'+str(job_soup.find(attrs={'class':'t5'}).string)
            yield item

        print('正在请求第%s页' % self.page)
        time.sleep(random.randint(1, 10))  # 随机休眠
        if self.page < allpage:  # 判断是否是最后一页
            self.page += 1
            yield scrapy.FormRequest(
                url=self.base_url + self.kw + ',2,' + str(self.page) + self.w_url,
                headers=self.headers,
                method='GET',
                callback=self.parse,
                dont_filter=True
            )
            return self.parse