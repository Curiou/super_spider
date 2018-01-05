# encoding=utf-8
import requests
import sys


class DianPing(object):

    def __init__(self, num):
        self.num = int(num)
        # self.base_url = 'https://tieba.baidu.com/f?kw=%s&ie=utf-8&pn=%s'%(tieba_name, (num-1)*50)
        self.base_url = 'http://www.dianping.com/search/category/1/10/p{}'.format(num-1)
        self.url_list = [self.base_url + str(i) for i in range(num)]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ('
                          'KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            # "Accept-Encoding":"gzip, deflate",
            # "Accept-Language":"zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7",
            # "Connection":"keep-alive",
            "Cookie":'showNav=#nav-tab|0|0; navCtgScroll=0; _lxsdk_cuid=1608ca57394c8-01fa0947c81a42-5b44271d-1fa400-1608ca57394c8; _lxsdk=1608ca57394c8-01fa0947c81a42-5b44271d-1fa400-1608ca57394c8; _hc.v=1caa0904-85a0-cd13-db2a-12e508a01d09.1514188142; aburl=1; pvhistory="6aaW6aG1Pjo8Lz46PDE1MTQxODk0MTU3MzRdX1s="; m_flash2=1; cityid=1; switchcityflashtoast=1; source=m_browser_test_33; default_ab=index%3AA%3A1%7CshopList%3AA%3A1; _lx_utm=utm_source%3Ddp_pc_food; JSESSIONID=EDB553FDD81FAC808D3ED6A173963FF0; cy=1; cye=shanghai; s_ViewType=10; _lxsdk_s=1609c1d1fcf-c7b-35c-f2e%7C%7C114',
            # "DNT":"1",
            # "Host":"www.dianping.com",
            "Referer":"http://www.dianping.com/search/category/1/10",
            # "Upgrade-Insecure-Requests":"1",
        }

    def get_page(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

    def save_file(self, data, index):
        filename = "dianping" + '_' + str(index) + '.html'
        with open(filename, 'wb') as f:
            f.write(data)

    def run(self):

        for url in self.url_list:
            # 3.1发送请求获取响应
            data = self.get_page(url)
            # 3.2保存成文件
            index = self.url_list.index(url)
            self.save_file(data, index)


def main():
    dianping = DianPing(4)
    dianping.run()


if __name__ == '__main__':
    main()
