# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import json
import os
from AssetTransaction.items import AssettransactionItem
from scrapy.conf import settings
import scrapy
import requests
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from pymongo import MongoClient

class AssettransactionPipeline(object):
    def __init__(self):
        self.file = open('csv_data.csv', 'wb')
        fieldnames = [
            'asset_no',
            'url',
            'img_url',
            'subject',
            'type',
            'region',
            'transfer_price',
            'transfer_rate',
            'description',
            'remark',
            'information',
            'total_review',
            'contact_name',
            'contact_phone',
            'contact_email',
            'valuation',
            'release_time',
            'address',
            'category',
            'trade_type',
            'area',
            'use_area',
            'owner',
            'located',
            'use_type',
        ]
        self.writer = csv.DictWriter(self.file, fieldnames=fieldnames)
        self.writer.writeheader()

    def process_item(self, item, spider):
        # print(item,'hhhhhhhhhhhhhhhhhhhh')
        # str_data = json.dumps(dict(item), ensure_ascii=False)
        self.writer.writerow(item)
        return item

    def __del__(self):
        self.file.close()


class JsonPipeline(object):
    def __init__(self):
        self.file = open('assettransaction.json', 'w')

    def process_item(self, item, spider):
        str_data = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.file.write(str_data)
        return item

    def __del__(self):
        self.file.close()

class MyImagesPipeline(ImagesPipeline):
    IMAGES_STORE = settings['IMAGES_STORE']

    # 该方法用于提交需要下载的图片链接请求
    def get_media_requests(self, item, info):
        if not os.path.exists('images'):
            os.makedirs('images')
        headers = settings['DEFAULT_REQUEST_HEADERS']
        url_list =[]
        if item['img_url'] != 1 and item['img_url'] != None:
            url_list.append(item['img_url'])
        if item['information'] != 1 and item['information'] != None:
            url_list.append(item['information'])
        if len(url_list) == 0:
            return
        for url in url_list:
            response = requests.get(url, headers=headers).content
            suffix = url.split('/')[-1]
            if suffix.split('.')[-1] == 'html':
                suffix = suffix.split('.')[-2]+'.jpg'
            filename = 'images' + os.sep + '.' + suffix
            with open(filename, 'wb')as f:
                f.write(response)
        return item
        # if item['img_url'] != 1:
        #
        #     yield scrapy.Request(item['img_url'])
        # if item['information'] != 1:
        #
        #     yield scrapy.Request(item['information'])

    # def item_completed(self, results, item, info):
    #     image_path = [data['path'] for status, data in results if status]
    #     # print (image_path)
    #
    #     # 获取图片的旧名
    #     old_name = self.IMAGES_STORE + os.sep + image_path[0]
    #     # new_name = self.IMAGES_STORE + os.sep + image_path[0].split(os.sep)[0] + os.sep + item['nick_name'] + '.jpg'
    #
    #     # os.rename(old_name, new_name)
    #
    #     item['image_path'] = old_name
    #     return item


class MongoPipeline(object):
    def __init__(self):
        # 创建链接
        host = settings['MONGO_HOST']
        port = settings['MONGO_PORT']
        database = settings['MONGO_DB']
        collection = settings['MONGO_COLL']

        self.client = MongoClient(host, port)
        self.db = self.client[database]
        self.coll = self.db[collection]

    def process_item(self, item, spider):
        data = dict(item)
        self.coll.insert(data)
        return item

    def __del__(self):
        self.client.close()

    # class MyImagesPipeline(ImagesPipeline):
#     def get_media_requests(self, item, info):
#         for image_url in item['img_url']:
#             if image_url != 1:
#                 yield scrapy.Request(image_url)
#         for information in item['information']:
#             if information != 1:
#                 yield scrapy.Request(information)
#
#     def item_completed(self, results, item, info):
#         image_paths = [x['path'] for ok, x in results if ok]
#         if not image_paths:
#             raise DropItem("Item contains no images")
#         item['image_paths'] = image_paths
#         return item

    # def file_path(self, request, response=None, info=None):
    #     '''自定义图片保存路径,以图片的url保存,重写前是图片的url经过MD5编码后存储'''
    #     image_guid = request.url
    #     return 'full/%s' % (image_guid)
