#encoding=utf-8

import sys, time
import urllib2
sys.path.append("./")
import json
from spiderx.common.baseCrawler import BaseCrawler
from spiderx.common.utility.resultUtil import BaseResultHandler, HourlySaveLocalHandler
from spiderx.common.utility.urlUtil import UrlManager
from superbase.constant import CFG_JOB_BATCH, CFG_JOB_NAME
from spiderx.common.constant import TAG_LIST_PAGE_PATTERN, TAG_LIST_ITEMS, TAG_LIST_TOTAL_PAGE_NUM, TAG_LIST_NO_RESULT, \
    CFG_HTTP_ENCODING, CFG_DOWN_MAXPAGENUM, CFG_DOWN_MAXNUM, CFG_DOWN_INDEX, TAG_LIST_PAGE_SIZE
from superbase.globalData import gConfig
from spiderx.common.utility.parseUtil import CssElement, RegexHandler, NextLevelHandler, SpecialHandler, Extractor, \
    ListElement
from superbase.utility.safeUtil import safeReg1
from superbase.utility.processUtil import callMethod

keyword_list = ["亿宝贷", "善林", "时说", "赚赚盈", "易宽", "shandaibao", "yibaodai"]


class ShanLin(BaseCrawler):
    """
    0.
    """

    def __init__(self, params=None):
        myCfg = {
            # 添加这两个配置只是为了调试方便
            # 为了生成错误的log日志
            CFG_JOB_BATCH: "shanlin20171220",
            # 不可以加动态的时间节点
            CFG_JOB_NAME: "shanlin",

            CFG_HTTP_ENCODING: "utf-8",
            # CFG_DOWN_MAXPAGENUM: 10,
            CFG_DOWN_INDEX: "www_github_com/codeSearch",
            # CFG_DOWN_MAXNUM: 10,
        }
        BaseCrawler.__init__(self, params, myCfg)


    def parse(self):
        """
        https://github.com/search?utf8=%E2%9C%93&q=%E5%96%84%E6%9E%97&type=
        """
        # 全局爬虫参数：实际项目中，建议在__init__中设置
        gConfig.set(CFG_DOWN_INDEX, "www_github_com/codeSearch")  # 索引需要统一设计，多级，便于存储检索
        url = "https://github.com/search?utf8=%E2%9C%93&q=%E5%96%84%E6%9E%97&type="
        company_detail_conf = {
            # 基于pyquery写的，用法和pyquery一样，css节点
            # listElement是先找父节点，在遍历父节的每一个元素
            "rank": ListElement("div#js-pjax-container > div > div > div > div > ul > div", itemCssElement={
                "titil": CssElement("div > h3 > a.v-align-middle"),
                "url": CssElement("div > h3 > a.v-align-middle", "href"),

                "type": CssElement("div:nth-child(2)"),
                "detail": CssElement("div:nth-child(1) >p"),
                "update_time": CssElement("div > div.d-flex > p > relative-time","datetime"),
            }),
        }
        # company_detail_conf["rank"]["url"] = safeReg1(url, "https://github.com", "url")
        #

        class MyResultHamdler(HourlySaveLocalHandler):
            def preProcess(self,result):
                result.update(self.callBackResult)
                index_url = "https://github.com"
                url_list = result["rank"]
                for url in url_list:
                    url["url"] = index_url + url["url"]
                return result

        self.downOneDetail(url, company_detail_conf, MyResultHamdler({"key":"善林"}))
        # BaseResultHandler 有判断错误日志的作用

        self.jobDone()


    def parse2(self):
        # 列表配置，有固定的几个key
        JdListConf = {
            TAG_LIST_PAGE_PATTERN: "&p=",
            TAG_LIST_ITEMS: "div#js-pjax-container > div > div > div > div > ul > div",
            # TAG_LIST_ITEMS: '*  > div.column.three-fourths.codesearch-results > div > ul > div',
            # js-pjax-container > div > div.columns > div.column.three-fourths.codesearch-results > div > ul > div:nth-child(1)
            TAG_LIST_PAGE_SIZE: 10,
            TAG_LIST_NO_RESULT: u"对不起，没有该查询结果",  # 可以不需要
            TAG_LIST_TOTAL_PAGE_NUM: CssElement("div#js-pjax-container > div > div > div > div > div > div > a:nth-last-child(2)"),  # RegexHandler有正则提取的功能
        }

        companyDetailConf = {
            # 如果没有就取value的值
            "watch": CssElement(
                "#js-repo-pjax-container > div > div > ul > li:nth-child(3) > a.social-count"),
        # 直接取属性
            "star": CssElement(
                "#js-repo-pjax-container > div > div > ul > li:nth-child(2) > div > form.unstarred.js-social-form > a"),
        # 直接取元素
            "fork_num": CssElement(
                "#js-repo-pjax-container > div > div > ul > li:nth-child(3) > a.social-count"),
        # 直接取元素
        }
        def getCompanyDetail(url, conf, callBackParams):
            # 生成错误日志
            return self.downOne(url, conf)
        # #js-pjax-container > div > div.columns > div.column.three-fourths.codesearch-results > div > ul > div:nth-child(1) > div.col-8.pr-3 > h3 > a
        JdItemConf = {
            "titil": CssElement("div > h3 > a.v-align-middle"),
            "url": CssElement("div > h3 > a.v-align-middle", "href"),
            "type": CssElement("div:nth-child(2)"),
            "status": CssElement("div > h3 > a.v-align-middle", "href", handler=NextLevelHandler(companyDetailConf, getCompanyDetail, "https://github.com", {"key": "20171225"})),
            "detail": CssElement("div:nth-child(1) >p"),    # , handler=RegexHandler(ur"(.*?(善\ 林) .*?)")
            "update_time": CssElement("div > div > p > relative-time","datetime"),
        }

        def getCompanyDetail(url, conf, callBackParams):
            # 生成错误日志
            return self.downOne(url, conf)

        class MyResultHamdler(HourlySaveLocalHandler):

            def preProcess(self, result):
                result.update(self.callBackResult)
                index_url = "https://github.com"
                result["url"] = index_url + result["url"]
                return result

        # https://github.com/search?utf8=%E2%9C%93&q=%E4%B8%AA%E4%BA%BA%E5%8D%9A%E5%AE%A2&type=Repositories
        keyword_list = ["赚赚盈","yibaodai","易宽","亿宝贷","shanlinbao","shanlin","shanlindai","善林","善林宝","善林贷"]
        for keyword in keyword_list:
            keyword = urllib2.quote(keyword)
            beginUrl = "https://github.com/search?o=desc&q={}&s=&type=Repositories&utf8=%E2%9C%93".format(keyword)

            urlMgr = UrlManager(self.http, self.parser, beginUrl)
            # print(urlMgr,"hhhhhhhhhhhhh")
            self.downLists(JdListConf, JdItemConf, MyResultHamdler, urlMgr)

            # 任务完成 需要调用JobDone
            self.jobDone()

if __name__ == '__main__':
    callMethod(ShanLin, sys.argv[1:])
    # ShanLin().parse()
    ShanLin().parse2()
