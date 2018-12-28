# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class JobPipeline(object):
    def __init__(self):
        self.conn = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='123456',
            db='myjob',
            charset='utf8',
        )
        self.cur = self.conn.cursor()
    def process_item(self, item, spider):
        try:
            self.cur.execute(
                "insert into job (city,jobname,company,salary,welfare,address,education,workyear,link,createtime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" , (item['city'], item['jobname'], item['company'], item['salary'],item['welfare'], item['address'],item['education'], item['workyear'],item['link'], item['createtime'])
            )
            self.conn.commit()
        except Exception as e:
            print(e)
        return item

