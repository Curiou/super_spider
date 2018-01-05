# encoding=utf-8

import sys,time
sys.path.append("./")
from spiderx.common.baseCrawler import BaseCrawler
from spiderx.common.utility.resultUtil import BaseResultHandler, HourlySaveLocalHandler
from superbase.utility.logUtil import logInfo
from spiderx.common.utility.urlUtil import UrlManager
from superbase.constant import CFG_JOB_BATCH, CFG_JOB_NAME, ET_RUN_BLOCK
from spiderx.common.constant import TAG_LIST_PAGE_PATTERN, TAG_LIST_ITEMS, TAG_LIST_TOTAL_PAGE_NUM, TAG_LIST_NO_RESULT, \
    CFG_HTTP_ENCODING, CFG_DOWN_MAXPAGENUM, CFG_DOWN_MAXNUM, CFG_DOWN_ACCOUNTID, BLOCKED_ELEMENT, CFG_BLOCK_MAXCHECK, \
    CFG_AB_STRATEGY, CFG_DOWN_INDEX, TAG_LIST_PAGE_SIZE
from superbase.globalData import gConfig
from superbase.utility.ioUtil import printDict
from spiderx.common.utility.parseUtil import CssElement, RegexHandler, NextLevelHandler, SpecialHandler, Extractor, \
    ListElement, EmmbedElement
from superbase.utility.processUtil import callMethod


class DianPingSpider(BaseCrawler):

    def __init__(self, params=None):
        myCfg = {
            # 添加这两个配置只是为了调试方便
            # 为了生成错误的log日志
            CFG_JOB_BATCH: "点评20171226",
            # 不可以加动态的时间节点
            CFG_JOB_NAME: "dianping",

            CFG_HTTP_ENCODING: "utf-8",
            # CFG_DOWN_MAXPAGENUM: 10,
            CFG_DOWN_INDEX: "www_dianping_com/search/category",
            # CFG_DOWN_MAXNUM: 10,
        }
        BaseCrawler.__init__(self, params, myCfg)

    def parse2(self):
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
        # json 数据，头文件要注意

        companyDetailConf = {
            # 如果没有就取value的值
            "belong_to": CssElement(
                ""),    # 属性

            "address": CssElement(
                ""),    # 地址

            "phone": CssElement(
                ""),    # 电话

            "feature": CssElement(
                ""),    # 特色

            "subbranch": CssElement(
                ""),    # 分店数
        }

        def getCompanyDetail(url, conf, callBackParams):
            # 生成错误日志
            return self.downOne(url, conf)
        JdItemConf = {
            "titil": CssElement("li > div.txt > div.tit > a:nth-child(1) > h4"),    # 标题
            "url": CssElement("li > div.txt > div.tit > a:nth-child(1)", "href"),   # 商铺连接

            "status": CssElement("li > div.txt > div.tit > a:nth-child(1)", "href",
                                 handler=NextLevelHandler(companyDetailConf, getCompanyDetail, callBackParams={"key": "20171225"})),
            "img_url":CssElement("li > div.pic > a > img", "href"), # 商铺主图链接
            "star_level":CssElement("li > div.txt > div.comment > span", "title"),  # 星级
            "appraise_num":CssElement("li > div.txt > div.comment > a.review-num > b"),  # 评价数
            "average_consumption": CssElement("li > div.txt > div.comment > a.mean-price > b"),     # 人均消费
            "comment_list": ListElement("li > div.txt > span",itemCssElement={
                "name":CssElement("span:nth-child(1)"),
                "grade":CssElement("span:nth-child(1) > b"),
            }),

            "type": CssElement("li > div.txt > div.tag-addr > a:nth-child(1) > span"),  # 口味类型
            "recommend":CssElement("li > div.txt > div.recommend > a"),   # 推荐菜

        }
        def getCompanyDetail(url, conf, callBackParams):
            # 生成错误日志
            return self.downOne(url, conf)

        class MyResultHamdler(HourlySaveLocalHandler):
            def preProcess(self, result):
                result.update(self.callBackResult)
                return result

        import urllib2
        keyword = urllib2.quote("shanlin")
        beginUrl = "https://github.com/search?o=desc&q={}&s=&type=Repositories&utf8=%E2%9C%93".format(keyword)
        urlMgr = UrlManager(self.http, self.parser, beginUrl)

        self.downLists(JdListConf, JdItemConf, MyResultHamdler, urlMgr)
        # 任务完成 需要调用JobDone
        self.jobDone()

if __name__ == '__main__':
    callMethod(DianPingSpider, sys.argv[1:])
    # DianPingSpider().parse()



