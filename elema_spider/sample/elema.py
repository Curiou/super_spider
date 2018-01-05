# -*- coding:utf-8 -*-
"""
   Author: du conglin <duconglin@shanglinjinrong.com>
   Copyright du conglin

"""
# -------------------------------------------------------------------------------
# 以上为版权信息
import json
import os
import sys
sys.path.append(".")
import time
from spiderx.common.constant import CFG_HTTP_OUTFORMAT, CFG_HTTP_INITURL, CFG_DOWN_INCMODE, TIME_OUT_SEC
# 用于结果保存的
from spiderx.common.utility.resultUtil import BaseResultHandler, HourlySaveLocalHandler
sys.path.append(".")
from spiderx.common.utility.resultUtil import BaseResultHandler
from spiderx.common.baseCrawler import BaseCrawler

from superbase.constant import CFG_DB_BUSINESS
from superbase.globalData import gTop, gConfig
from superbase.utility.logUtil import logInfo

from superbase.constant import CFG_JOB_BATCH, CFG_JOB_NAME, CFG_JOB_DEBUG, CFG_LOG_FILE_NAME

from superbase.utility.processUtil import callMethod


class AssetTransactionSpider(BaseCrawler):
    """
    饿了吗官网
    客户需求：
    商店名
    商店里的菜品名若干
    """
    def __init__(self, params=None):
        myCfg = {
            # 写出请求返回的相应形式
            CFG_HTTP_OUTFORMAT: "json",
            # 获得最新cookie
            CFG_HTTP_INITURL: "https://www.ele.me/place/wtw67xkf60p",
            # 用于生成log
            CFG_JOB_BATCH: "elema_20171215",
            CFG_JOB_NAME: "elema",
            CFG_DB_BUSINESS: "elema",
            # 延时伪装5秒
            TIME_OUT_SEC: 5,
        }
        BaseCrawler.__init__(self, params, myCfg)

    def detailTest(self, site='wtw67xkf60p'):
        """
        熟悉灵活的配置，包括深层嵌套
        # 店铺页
        https://www.ele.me/place/wtw67xkf60p?latitude=31.37322&longitude=121.44949
        # 店铺的json
        https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash=wtw67xkf60p&latitude=31.37322&limit=24&longitude=121.44949&offset=0
        # 商品页
        https://www.ele.me/shop/156599189
        # 商品的json
        https://www.ele.me/restapi/shopping/v2/menu?restaurant_id=156599189

        """
        urlTemp = "https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash={site}&latitude=31.37322&limit=30&longitude=121.44949&offset={page}"

        def save(result):
            # posts = result["statuses"]
            saveNum = 0
            for post in result:
                result={
                    "shop_id":post["id"],
                    "shop_name":post["name"],
                    # 三目运算
                    # "topicUser":post["retweeted_status"]["user_id"] if post["retweet_status_id"] else post["user_id"],
                }
                result["foods"] = prosser(result)
                saveNum += 1
            return saveNum

        # FIXME 店铺详情页的处理
        def prosser(result):
            try:
                posts = result[0]["foods"]
            except Exception as e:
                print (e)
            for post in posts:
                result = {
                    "foods_name": post["name"],
                    "foods_id": post["item_id"]
                }

        total = maxPage = 10000 #设定一个不可能最大数
        downNum = 0
        curPage = 30 * gConfig.get(CFG_DOWN_INCMODE, 1) #该参数可用做断点使用
        while curPage <= maxPage and downNum < total:
            url = urlTemp.format(site=site, page=0)
            result = self.downOne(url, None)
            if downNum == 0:
                maxPage = curPage + total/30 + 1
                logInfo("user=%s,curPage=%s,maxPage=%s,hasDowned=%s,total=%s" % (site, curPage, maxPage, total))
            curPage += 1
            downNum += save(result)
            logInfo("user=%s,curPage=%s,downNum=%s" % (site, curPage, downNum))

        self.downOneDetail(url, BaseResultHandler(HourlySaveLocalHandler()))

        # 任务完成 需要调用JobDone
        # self.jobDone()


if __name__ == '__main__':
    callMethod(AssetTransactionSpider, sys.argv[1:])
