# encoding=utf-8

import sys,time
sys.path.append("./")
from spiderx.common.baseCrawler import BaseCrawler
from spiderx.common.utility.httpUtil import getHeadersFromDriver
from spiderx.common.utility.resultUtil import HourlySaveLocalHandler
from spiderx.common.utility.urlUtil import UrlManager
from superbase.constant import CFG_JOB_BATCH, CFG_JOB_NAME
from spiderx.common.constant import TAG_LIST_PAGE_PATTERN, TAG_LIST_ITEMS, TAG_LIST_TOTAL_PAGE_NUM, TAG_LIST_NO_RESULT, \
    CFG_HTTP_ENCODING,  CFG_DOWN_INDEX, TAG_LIST_PAGE_SIZE,CFG_HTTP_INITURL
from spiderx.common.utility.parseUtil import CssElement, ListElement, RegexHandler
from superbase.utility.processUtil import callMethod

class DianPingSpider(BaseCrawler):

    def __init__(self, params=None):
        myCfg = {
            # 添加这两个配置只是为了调试方便
            # 为了生成错误的log日志
            CFG_JOB_BATCH: "点评20171226",
            # 不可以加动态的时间节点
            CFG_JOB_NAME: "dianping",
            # 首页设置用于获取cookie
            CFG_HTTP_INITURL: "http://www.dianping.com/",
            # 解码格式
            CFG_HTTP_ENCODING: "utf-8",
            # CFG_DOWN_MAXPAGENUM: 10,
            CFG_DOWN_INDEX: "www_dianping_com/search/category",
            # CFG_DOWN_MAXNUM: 10,
        }
        BaseCrawler.__init__(self, params, myCfg)

    def parse(self):

        # from selenium import webdriver
        # driver = webdriver.PhantomJS()
        # getHeadersFromDriver(driver, host="www.dianping.com",refer="http://www.dianping.com/search/category/1/10/p2?aid=17648683%2C23999832%2C16789967%2C63177252%2C59399241%2C27421074")
        # driver.close()

        # 列表配置，有固定的几个key
        JdListConf = {
            TAG_LIST_PAGE_PATTERN: "/p",
            TAG_LIST_ITEMS: "div#shop-all-list > ul",

            TAG_LIST_PAGE_SIZE: 15,
            TAG_LIST_NO_RESULT: u"对不起，没有该查询结果",  # 可以不需要
            TAG_LIST_TOTAL_PAGE_NUM: CssElement(
                "div.content-wrap > div.shop-wrap > div.page > a:nth-last-child(2)"),
            # RegexHandler有正则提取的功能
        }
        def getCompanyDetail(url, conf, callBackParams):
            # 生成错误日志
            return self.downOne(url, conf)
        JdItemConf = {
            "titil": CssElement("li > div.txt > div.tit > a:nth-child(1) > h4"),    # 标题
            "url": CssElement("li > div.txt > div.tit > a:nth-child(1)", "href"),   # 商铺连接
            "img_url":CssElement("li > div.pic > a > img", "src"), # 商铺主图链接
            "star_level":CssElement("li > div.txt > div.comment > span", "title"),  # 星级
            "appraise_num":CssElement("li > div.txt > div.comment > a.review-num > b"),  # 评价数
            "average_consumption": CssElement("li > div.txt > div.comment > a.mean-price > b"),     # 人均消费

            "comment_list": ListElement("li > div.txt > span",itemCssElement={      # 相应评论
                "name":CssElement("span:nth-child(1)", handler=RegexHandler(r"(.*?)\ .*?")),
                "grade":CssElement("span:nth-child(1) > b"),
            }),

            "type": CssElement("li > div.txt > div.tag-addr > a:nth-child(1) > span"),  # 口味类型
            "recommend":CssElement("li > div.txt > div.recommend > a"),   # 推荐菜
            "activity": ListElement("li > div.svr-info > div",itemCssElement={       # 活动类型及其策划
                "name":CssElement("anth-child(2) > span"),
                "grade":CssElement("a:nth-child(2)", handler=RegexHandler(r".*?\:(.*?)")),
            }),

        }

        class MyResultHamdler(HourlySaveLocalHandler):
            def preProcess(self, result):
                result.update(self.callBackResult)
                return result

        # import urllib2
        # keyword = urllib2.quote("善林")
        # beginUrl = "https://github.com/search?o=desc&q={}&s=&type=Repositories&utf8=%E2%9C%93".format(keyword)
        beginUrl = "http://www.dianping.com/search/category/1/10"
        urlMgr = UrlManager(self.http, self.parser, beginUrl)
        self.downLists(JdListConf, JdItemConf, MyResultHamdler, urlMgr)
        # 任务完成 需要调用JobDone
        self.jobDone()


if __name__ == '__main__':
    callMethod(DianPingSpider, sys.argv[1:])
    DianPingSpider().parse()



