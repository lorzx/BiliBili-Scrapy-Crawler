# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class BilibilicrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class BilibiliUserPipeline(object):
    def process_item(self, item, spider):

        # ========= if deploy in Scrapy Cloud, leave the comment =========
        # ========= remember setting your own db user name, password and db_name

        # con = pymysql.connect(host="127.0.0.1", user="root", passwd="your_password", db="database_name", charset="utf8")
        # cur = con.cursor()
        # sql = ("INSERT INTO bilibili_user_info(mid, name, sex, face, coins, spacesta, \
        #         birthday, place, description, article, following, fans, playnum, sign, level, exp) \
        #        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        # lis = (item["mid"],item["name"],item["sex"],item["face"],item["coins"],item["spacesta"],item["birthday"],item["place"],
        #        item["description"],item["article"],item["following"],item["fans"],item["playnum"],item["sign"],item["level"],item["exp"])
        # cur.execute(sql, lis)
        # con.commit()
        # cur.close()
        # con.close()
        return item
