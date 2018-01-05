# -*- coding: utf-8 -*-
import scrapy
import json
from Elema.items import ElemaItem
class ElemaSpider(scrapy.Spider):
    name = 'elema'
    allowed_domains = ['www.ele.me']
    start_urls = ['https://www.ele.me/restapi/v2/pois?extras%5B%5D=count&geohash=wtw3sjq6n6um&keyword=浦&limit=20&type=nearby']

    # 地区页
    def parse(self, response):
        dict_data = json.loads(response.body.decode())
        # 遍历节点列表
        for node in dict_data:
            geohash = node['geohash']
            site_url = "https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash={}&latitude=31.21247&limit=30&longitude=121.60681&offset=".format(geohash)
            url_list = [site_url + str(i * 30) for i in range(30)]
            for url in url_list:
                yield scrapy.Request(url, callback=self.parse_area)

    # 商户页
    def parse_area(self,response):
        dict_data = json.loads(response.body.decode())
        # 遍历节点列表
        for node in dict_data:
            temp = {}
            temp['shop_id'] = node["id"]
            temp["shop_name"] = node['name']
            shop_url = "https://www.ele.me/restapi/shopping/v2/menu?restaurant_id=" + str(temp['shop_id'])
            yield scrapy.Request(shop_url, callback=self.detil_area, meta={"temp": temp})

    # 商品页
    def detil_area(self,response):
        s = response.meta["temp"]
        print (s,"\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\/")
        temp =[]
        item = ElemaItem()
        item["shop_id"] = response.meta["temp"]["shop_id"]
        item["shop_name"] = response.meta["temp"]["shop_name"]
        dict_data = json.loads(response.body.decode())[0]["foods"]
        # 遍历节点列表
        for node in dict_data:
            goods_name = node["name"]
            temp.append(goods_name)
        item["foods_name"] = temp
        yield item
