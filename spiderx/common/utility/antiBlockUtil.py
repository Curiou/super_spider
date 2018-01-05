# -*- coding:utf-8 -*-
"""
   Author: bafeng huang<hbfhero@163.com>
   Copyright bafeng huang

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import json
import os
import time

from superbase.globalData import gConfig, gTop, PROJECT_ROOT
from superbase.utility.ioUtil import getPrintDict
from superbase.utility.logUtil import logError, logInfo
from superbase.utility.mailUtil import Mail
from superbase.utility.timeUtil import getTimestamp, getTimestampBySec

from superbase.constant import CFG_JOB_NAME, CFG_JOB_BATCH, \
    CFG_LOG_FILE_NAME, CFG_JOB_ENABLE, CFG_JOB_EMAIL, CFG_JOB_BEGINTIME, CFG_JOB_CHANGENODE, GD_JOB_ERROR, ADMIN_MAIL

from spiderx.common.constant import CFG_BLOCK_MAXCHECK, BLOCKED_ELEMENT, BLOCKED_INFO, CFG_HTTP_INTERVAL, \
    CFG_HTTP_ENCODING, \
    CFG_DOWN_ACCOUNTID
from superbase.utility.processUtil import applyFunc


class AntiBlock(object):
    """
   #针对某些url,check是否被block,也同时用于页面结构是否改变
antiBlocks=(
                {
                    'key':['cmp?keyword='],#url 标示key
                    'blockInfo':None,#如果有该info，直接使用
                    "blockElement":(
                                    ({"name":CssElement("body > ul > li:nth-child(1)")},u"公司名字"),#不确定有blockInfo时，用element判断,

                                   ),
                    "strategy":AntiBlockStategy(strategy="_postpone 3600,_changeAccount,_incInterval 2"),#默认策略实现类
                },
                {
                    'key':['jobui.com/company/'],#
                    'blockInfo':None,#如果有该info，直接使用
                    "blockElement":(({"name":("#navTab > a:first",None,None)},u"公司介绍"),),#不确定有blockInfo时，用element判断,
                    "strategy":MyAntiBlockStategy(strategy="_postpone 3600,_changeAccount),#自定义策略实现,子类,通常是
                },
               )


            爬虫是个循环,碰到block错误,基本策略是
            1,报告错误
            2,根据strategy预处理好下一次运行的配置,如切换账号,增加爬虫间隔
            3,set jobStatus = Error,set new beginTime, and update cfg
            4,将错误处理交给上层:
                4.1 交给worker,set errorHandler:worker
                    worker checkError and run it when beginTime reached
                4.2 交给foreman,set errorHandler:foreman
                    worker checkError and reAssign  it
    """

    def __init__(self, antiBlockConf, extractor):
        """
        初始化
        :param antiBlockConf: 反block策略
        :param extractor: 提取器
        """
        self.antiBlocks = antiBlockConf
        self.extractor = extractor
        self.blocked = 0
        self.blockCheck = 0

    def getAntiBlockConf(self, url):
        """
        获取反block策略
        :param url: 请求的url
        :return: 如果有设置反block策略，则返回item这个字典，如果没有，返回一个值为None的result
        """
        result = None

        # 遍历反block策略列表
        for item in self.antiBlocks:
            key = item['key']  # 获取item字典中键为‘key’的值
            for key1 in key:
                if url.find(key1) >= 0 or key1 == "*":
                    # 如果在url中找到获取字典元素中的字符串，就返回该反block策略
                    return item

        return result  # 返回None

    def checkBlock(self, url, content):
        """
        检测是否被block
        :param url: 请求的url
        :param content: 请求网页的内容
        :return: 是否被block，反block策略
        """
        antiBlock = self.getAntiBlockConf(url)  # 获取反block策略
        if antiBlock:
            # 如果获取到了反block策略，调用doCheckBlock方法，执行检测block
            self.doCheckBlock(url, content, antiBlock)
        return self.blocked, antiBlock["strategy"]

    def isBlocked(self):
        """
        判断是否被block
        :return:
        """
        return self.blocked

    def handleBlock(self, url, content, handleStrategy, downInfo):
        """
        处理block
        :param url: 请求的url
        :param content: 请求网页的内容
        :param handleStrategy: 处理方法
        :param downInfo: downNum,downTime,downInterval etc. 下载信息： 下载量，下载时间，下载时间间隔等
        :return:
        """
        if self.blocked == BLOCKED_ELEMENT:
            self.alarmPageError(url, content, downInfo)
        elif self.blocked == BLOCKED_INFO:
            handleStrategy.handle()
        else:
            logError("the block flag is none,pls double check the process!")

    def doCheckBlock(self, url, content, antiBlock):
        """
        执行检测被block,如果被block次数超出预先设定,则失败,结束并重置
        :param url: 请求的url
        :param content: 请求网页的内容
        :param antiBlock: 反block策略
        :return:
        """
        blockInfo = antiBlock.get("blockInfo", None)  # 获取blcokinfo， 如果没有，默认为None
        self.blocked = 0
        if blockInfo:
            # 获取到了blockinfo
            self.blocked = BLOCKED_INFO if content.find(
                blockInfo) > 0 else 0  # 如果获取到的blockinfo大于0，那么就赋值给self.blocked，不然就赋值为0
            if self.blocked:
                # 如果被block，打印log信息
                logError("!!!!block by %s,url=%s" % (gConfig.get(CFG_JOB_NAME), url))
            return
        else:  # check the elements
            # 没有获取到blockinfo
            blocked = False

            # 遍历
            for template, value in antiBlock.get("blockElement"):
                result = {}
                # 使用提取器
                self.extractor.getResultByContent(content, template, result)
                checkName = result.get("name", None)  # 将提取结果中键为‘name’的值赋值给checkName，如果没有，默认值为None
                if not checkName or checkName.find(value) == -1:
                    # 如果没有获取到结果，则表示被block
                    blocked = True
                else:
                    blocked = False  # 反之，没有被block
                    break  # 非block马上跳出
            if blocked:
                # 如果被block
                self.blockCheck += 1
                logError("the element not exist,block?%s" % url)
            else:
                # 反之,没有被block
                self.blockCheck = 0  # reset

            if self.blockCheck > gConfig.get(CFG_BLOCK_MAXCHECK):
                # 如果被block次数大于配置中设定的值
                logError("block by element,pls check the content,maybe the structure has changed!")  # log记录
                # 重置
                self.blocked = BLOCKED_ELEMENT
                self.blockCheck = 0

    def alarmPageError(self, url, content, downInfo):
        """
        解析元素有错,有可能是blocked 也有可能是页面结构变化,邮件警告,人工检查
        :param url:
        :param content:
        :param downInfo:downNum,downTime,downInterval etc.
        :return:
        """
        fname, filePath = AntiBlock.saveWrongPage(content)

        # 错误消息
        info = {
            'jobName': gConfig.get(CFG_JOB_NAME),  # 工作名称
            'batch': gConfig.get(CFG_JOB_BATCH),  # 分批处理
            'url': url,
            'filePath': filePath,  # 文件路径
            'type': self.blocked,  # 阻塞
            'detail': json.dumps(downInfo),
            'inTime': getTimestamp(),
        }

        title = "block-%s" % self.blocked  # 把阻塞的 作为标题
        content = getPrintDict(info)  # 字典形式的错误内容
        attach = [(fname, filePath)]

        emails2 = [gConfig.get(CFG_JOB_EMAIL, ADMIN_MAIL[0])]  # 获取job负责人,管理员邮箱

        # 获取是否启用任务调度
        if gConfig.get(CFG_JOB_ENABLE, 0):
            gTop.get('db').insert("block", info)
            from jobManager.job import Job
            Job().sendEmail(
                title=title,
                content=content,
                attach=attach,
                emails2=emails2
            )

        # 发送邮件
        Mail.sendEmail(
            title=title,
            content=content,
            t_address=emails2,
            attaches=attach
        )
        logError("blocked?check the content\n%s" % getPrintDict(info))

    @staticmethod
    def saveWrongPage(content2, htmlFile=None):
        """
        保存错误页面
        :param content2: 网页源码内容
        :param htmlFile: html文件
        :return: 新的文件名,html文件
        """
        import random
        if not htmlFile:
            # 如果不是html文件,# 新建htnl文件
            htmlFile = gConfig.get(CFG_LOG_FILE_NAME).replace(".txt", "%s.html" % (random.randint(100, 999)))
            htmlFile = os.path.join(PROJECT_ROOT + "log/", htmlFile)
        fname = os.path.split(htmlFile)[1]
        import codecs

        # 将内容写入到新文件中
        with codecs.open(htmlFile, 'wb', gConfig.get(CFG_HTTP_ENCODING, "utf-8")) as f:
            f.write(content2)

        logInfo("saveWrongPage:%s" % htmlFile)
        return fname, htmlFile


class AntiBlockStategy(object):
    """
    反block策略集合,可以通过gConfig配置策略,策略可以作为一个策略组合,用分号隔开
    如ab.strategy="postpone 3600;changeAccount 1"
    当被block后,
        该batch的任务会被挂起,
        参数重新设置 by gData.get(GD_JOB_ERROR)
        等待重新调度 by worker or foreman
    """

    def __init__(self, strategy):
        """
        :param strategy: 策略可以作为一个策略组合,用分号隔开如"postpone 3600;changeAccount 1"
        :return:
        """
        self.handlers = [filter(lambda x: len(x), handler.strip().split(" ")) for handler in strategy.split(";")]

    def handle(self):
        for handler in self.handlers:
            applyFunc(obj=self, strFunc=handler[0], arrArgs=handler[1:])

    def postpone(self, seconds):
        """
        最简单,延时处理
        :param seconds:延时时间
        :return:
        """
        logInfo("AntiBlock:postpone %s seconds" % seconds)  # 打印提示消息
        gTop.get(GD_JOB_ERROR)[CFG_JOB_BEGINTIME] = getTimestampBySec(time.time() + int(seconds))

    def changeInterval(self, interval):
        """
        修改下载时间间隔
        :param seconds: 时间间隔，以秒为单位
        :return:
        """
        logInfo("AntiBlock:changeInterval %s" % interval)  # 打印提示消息
        gTop.get(GD_JOB_ERROR)[CFG_HTTP_INTERVAL] = interval

    def changeAccount(self, accountId=""):
        """
        切换账号,这个函数的实现需要子类
        :param accountId: 为空标示随机取下一个
        :return:
        """
        logInfo("AntiBlock:changeAccount %s " % accountId)  # 打印提示消息
        gTop.get(GD_JOB_ERROR)[CFG_DOWN_ACCOUNTID] = accountId

    def changeIP(self):
        """
        这个暂时不实现,因为爬虫本身是在变ip服务器上的
        :return:
        """
        logInfo("AntiBlock:change IP")  # 打印提示消息
        self.changeNode()

    def changeNode(self):
        """
        改变节点
        :return:
        """
        logInfo("AntiBlock:change node")  # 打印提示消息
        gTop.get(GD_JOB_ERROR)[CFG_JOB_CHANGENODE] = 1.
