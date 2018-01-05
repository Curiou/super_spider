# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
import time
import random
from selenium import webdriver



class AssettransactionSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:

            yield r


    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SeleniumMiddleware(object):
    def process_request(self, request, spider):
        # url = 'http://www.cnassets.com/login.html'
        # list_pwd = ['18666296873:xiaoxiao',
        # '17717856741:wangyalin',
        # # '13460306050:yibingtao',
        # '17621694486:123456.'
        # '13601604687:Wuhz123456']
        # # 创建一个浏览驱动
        # # service_args=['--igmore-ssl-errors=true', '--ssl-protocol=TLSvl']
        # driver = webdriver.Chrome()
        # # 获取url对应的响应
        # # driver.get(request.url)
        # # time.sleep(1)
        # # detil = driver.find_elements_by_xpath('//*[@id="btn_release_info"]')[0]
        # # detil.click()
        # driver.get(url)
        # time.sleep(4)
        # user_pwd = random.sample(list_pwd, 1)[0]
        # user = user_pwd.split(":")[0]
        # pwd = user_pwd.split(":")[1]
        # # print (user,pwd)
        # el_user = driver.find_elements_by_xpath('//*[@id="zhPhone"]')[0]
        # el_user.send_keys(user)
        # el_pwd = driver.find_elements_by_xpath('//*[@id="zhPwd"]')[0]
        # el_pwd.send_keys(pwd)
        # el_login = driver.find_elements_by_xpath('//*[@id="login-zhanghao"]/form/div/button')[0]
        # el_login.click()
        # cookie = driver.get_cookies()
        driver = webdriver.PhantomJS()
        # time.sleep(3)
        driver.get(request.url)
        time.sleep(0.1)
        # detil = driver.find_elements_by_xpath('//*[@id="btn_release_info"]')[0]
        # detil.click()
        # time.sleep(1)
        # 保存渲染之后的源码
        data = driver.page_source
        # print (data)
        # 关闭浏览器驱动
        driver.close()
        # 构建响应
        res = HtmlResponse(request.url, body=data.encode(),encoding='utf-8',request=request)
        # 返回响应
        return res


# from AssetTransaction.settings import USER_AGENT_LIST
# from AssetTransaction.settings import PROXY_LIST
# import random
# import base64
#
# class RandomUserAgentMiddleware(object):
#     def process_request(self, request, spider):
#
#         # 随机获取一个请求头
#         user_agent = random.choice(USER_AGENT_LIST)
#         # print (user_agent)
#         # 设置请求头
#         request.headers['User-Agent'] = user_agent
