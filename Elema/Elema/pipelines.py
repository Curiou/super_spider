# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import json


class ElemaPipeline(object):
    def __init__(self):
        self.file = open('csv_data.csv', 'wb')
        fieldnames = [
            'shop_id',
            'shop_name',
            'foods_name',
        ]
        self.writer = csv.DictWriter(self.file, fieldnames=fieldnames)
        self.writer.writeheader()

    def process_item(self, item, spider):
        self.writer.writerow(item)
        return item

    def __del__(self):
        self.file.close()


class JsonPipeline(object):
    def __init__(self):
        self.file = open('assettransaction.txt', 'w')

    def process_item(self, item, spider):
        str_data = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.file.write(str_data)
        return item

    def __del__(self):
        self.file.close()