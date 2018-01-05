#encoding=utf-8
import requests,request
import json
from lxml import etree
import random
import os
import shutil
import re
from selenium import webdriver
from scrapy.http import HtmlResponse
import time


class Test(object):
    # 初始化函数
    def __init__(self,url):
        # 设置请求的头部
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ("
                          "KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
            "Accept - Encoding": "gzip, deflate",
            "Accept - Language":"zh - CN, zh;q = 0.9",
            "Connection":"keep - alive",
            "Content - Type": "application / x - www - form - urlencoded;charset = UTF - 8",
            'Cookie':'hi.sso.cookiekey = "37e5d9bd,bb3c56ed826bbe67e47d122fcc8ce754f57f45d2ad74f854e8ac5ca56d54c584ef303f68ea0f7aa5cb04addeace1518a4675e3cf69339f54";JSESSIONID = 5EA60944F60B305E0663DF07A1C699A5;Hm_lvt_3b8134abcea272b53d4cab51edc9fd57 = 1512523337;Hm_lpvt_3b8134abcea272b53d4cab51edc9fd57 = 1512610482',
            "Host":"www.cnassets.com",
            "Origin":"http: // www.cnassets.com",
        }
        # 设置要访问的地址
        self.url = url
        self.urllist = list()

    # 发送请求
    def get_content(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

    def save_data(self,data):
        newname = 'hhh.txt'
        with open(newname, 'wb')as f:
            f.write(data)

    def url_list(self, data):
        sn = data.xpath('//body[@id="detail"]/div[4]/div[1]/div[2]/div[1]/span[2]/text()').extract_first()
        if sn == None:
            return
        self.urllist.append(data.url)


    def run(self):
        data = self.get_content(self.url)
        self.url_list(data)
        text = re.match(r'(http\://www\.cnassets\.com/moreInformation/\w*?/12/)(\d+?)/0\.html', self.url)
        str1 = text.group(1)
        str2 = text.group(2)
        # print (str1, str2)
        self.url = str1 + str(int(str2) + 1) + '/0.html'
        self.run()
        print (self.urllist)

def main():
    url = 'http://www.cnassets.com/moreInformation/equity/12/1/0.html'
    pic = Test(url)
    pic.run()


if __name__ == '__main__':
    main()
