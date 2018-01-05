# encoding=utf-8
import requests
from lxml import etree
import json
import os
import shutil
import time

class Elema(object):
    # 初始化函数
    def __init__(self):

        # print (self.url_list)
        # 设置请求的头部
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36",
            "Referer": "https://www.ele.me/place/wtw39muyt1n",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-encoding": "gzip, deflate, br",
            "Accept-language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7",
            "Dnt": "1",
            "Cookie": "ubt_ssid=j16rntnyj3l4jtc5m4j6l7vux5zxc2nd_2017-12-12; perf_ssid=jff1r41n9m4gyvqbgxn4omto3fhsx3uu_2017-12-12; _utrace=ee72ffac57534c8672a1c24898bf684e_2017-12-12; eleme__ele_me=ff57c290d6c60138dd3446b48f5c6ab0%3Aa086fec4b3f68f01cad495dec93fd9abb5b5a2c2; firstEnterUrlInSession=https%3A//www.ele.me/shop/157658769; track_id=1513073688%7Ccf471fbc5751634fa404079039f7ab894bf5cde3a7fec7b7d5%7Ca2bcb79dd44dbd80220fe62defde833e; pageReferrInSession=https%3A//www.ele.me/place/wtw3x4p3u41",
            "Upgrade-insecure-requests": "1",
            "Cache-control": "max-age=0"
        }
        self.file = open('Ele3.txt', 'w')
    def url_detil(self):
        # 设置url列表
        site = ["wtw39muyt1n",
                'wtw3kpu1du7',
                'wtw3d8kbb4b',
                'wtw3d8kfntc',
                'wtw6jxej86t',
                'wtw3yj1z60k',
                'wtw67xkf60p'
                ]
        for name in site:
            url = 'https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash={}&latitude=31.23388&limit=30&longitude=121.350741&offset=0'.format(name)
            url_list = [url + str(i * 30) for i in range(28)]
            for url in url_list:
                data = self.get_content(url)
                time.sleep(2)
                page_list = self.parse_list_page(data)


    # 发送请求
    def get_content(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

    # 保存网页数据
    def save_url(self,data):
        newname = 'hhh.txt'
        with open(newname, 'wb')as f:
            f.write(data)

    # 解析列表页面数据
    def parse_list_page(self, response):
        # self .save_data(data)
        dict_data = json.loads(response.decode())
        # 遍历节点列表
        for node in dict_data:
            temp = {}
            temp['shop_id'] = node["id"]
            temp["shop_name"] = node['name']
            goods_url = self.join_url(temp['shop_id'])
            data = self.get_content(goods_url)
            time.sleep(2)
            # print (data)
            temp["foods_name"] = self.detil_dict(data)
            self.save_data(temp)
            # print (temp)
        # return

    # 解析商品的数据
    def detil_dict(self, response):
        temp = []
        try:
            list_data = json.loads(response.decode())
            foods_list = list_data[0]["foods"]
        # print (foods_list)
        except Exception as e:
            print (e)
            return temp
        for foods in foods_list:
            goods_name = foods["name"]
            temp.append(goods_name)
        # print (dict_data)
        return temp

    # 构建商户的url
    def join_url(self, shop_id):
        index_url = "https://www.ele.me/restapi/shopping/v2/menu?restaurant_id="
        url = index_url + str(shop_id)
        return url

    # 保存数据
    def save_data(self, data):
        # for data in data_list:
        if data["foods_name"] != []:
            str_data = json.dumps(data, ensure_ascii=False) + ',\n'
            self.file.write(str_data)

    def run(self):
        self.url_detil()
        # self.download_pic()


def main():
    pic = Elema()
    pic.run()


if __name__ == '__main__':
    main()



