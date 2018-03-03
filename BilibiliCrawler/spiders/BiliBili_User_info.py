# -*-coding:utf8-*-

import scrapy
import json
import random
import datetime
import time
from BilibiliCrawler.items import User_Item
from BilibiliCrawler.settings import USER_AGENTS, USER_ID_MIN, USER_ID_MAX

def datetime_to_timestamp_in_milliseconds(d):
    def current_milli_time(): return int(round(time.time() * 1000))
    return current_milli_time()

# ========= if use your own user_agents.txt ====================
# def LoadUserAgents(uafile):
#     """
#     uafile : string
#         path to text file of user agents, one per line
#     """
#     uas = []
#     with open(uafile, 'rb') as uaf:
#         for ua in uaf.readlines():
#             if ua:
#                 uas.append(ua.strip()[1:-1 - 1])
#     random.shuffle(uas)
#     return uas
# uas = LoadUserAgents("user_agents.txt")

# ========= if use default ua and want to deploy in Scrapy Cloud =========
uas = USER_AGENTS

class bilibili_scrapy(scrapy.Spider):
    name = "bilibili"

    def start_requests(self):
        # set USER_ID_MIN and USER_ID_MAX to define your own range in settings.py, default 1M info
        for m in range(USER_ID_MIN, USER_ID_MAX):
            for i in range(m * 100, (m + 1) * 100):
                url = 'https://space.bilibili.com/' + str(i)
                ua = random.choice(uas)
                head = {
                    'User-Agent': ua,
                    'Referer': 'https://space.bilibili.com/' + str(i) + '?from=search&seid=' + str(random.randint(10000, 50000))
                }
                formdata = {
                    '_': str(datetime_to_timestamp_in_milliseconds(datetime.datetime.now())),
                    'mid': url.replace('https://space.bilibili.com/', '')
                }
                yield scrapy.FormRequest(url='http://space.bilibili.com/ajax/member/GetInfo', callback=self.parse_item, formdata=formdata, headers=head)
            time.sleep(10)

        # =========== below is for debugging purpose =========
        # url = 'https://space.bilibili.com/123456'
        # ua = random.choice(uas)
        # head = {
        #     'User-Agent': ua,
        #     'Referer': 'https://space.bilibili.com/' + '123456' + '?from=search&seid=' + str(random.randint(10000, 50000))
        # }
        # formdata = {
        #     '_': str(datetime_to_timestamp_in_milliseconds(datetime.datetime.now())),
        #     'mid': url.replace('https://space.bilibili.com/', '')
        # }
        # yield scrapy.FormRequest(url='http://space.bilibili.com/ajax/member/GetInfo', callback=self.parse_item, formdata=formdata, headers=head)

    # ============ parse_item and parse_ff are used to extract the structured data ===============
    # ============ if you want to save the data to MySQL, see pipeline.py          ===============

    def parse_item(self, response):
        jsDict = json.loads(response.text)
        statusJson = jsDict['status'] if 'status' in jsDict.keys() else False
        if statusJson == True:
            if 'data' in jsDict.keys():
                jsData = jsDict['data']
                item = User_Item()
                item['mid'] = jsData['mid']
                item['name'] = jsData['name']
                item['sex'] = jsData['sex']
                item['face'] = jsData['face']
                item['coins'] = jsData['coins']
                item['spacesta'] = jsData['spacesta']
                item['birthday'] = jsData['birthday'] if 'birthday' in jsData.keys() else 'nobirthday'
                item['place'] = jsData['place'] if 'place' in jsData.keys() else 'noplace'
                item['description'] = jsData['description']
                item['article'] = jsData['article']
                item['playnum'] = jsData['playNum']
                item['sign'] = jsData['sign']
                item['level'] = jsData['level_info']['current_level']
                item['exp'] = jsData['level_info']['current_exp']
                request = scrapy.Request(url='https://api.bilibili.com/x/relation/stat?vmid=' + str(item['mid']) + '&jsonp=jsonp', callback=self.parse_ff)
                request.meta['item'] = item
                yield request

    def parse_ff(self, response):
        item = response.meta['item']
        js_fans_data = json.loads(response.text)
        item['following'] = js_fans_data['data']['following']
        item['fans'] = js_fans_data['data']['follower']
        yield item
