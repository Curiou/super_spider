# -*- encoding: utf-8 -*-
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

from selenium import webdriver
from selenium.webdriver.common.by import By

from spiderx.common.constant import ACCOUNT_TPE_COOKIE, CFG_DOWN_WEBSITE
from spiderx.common.utility.dbUtil import LocalDb
from superbase.constant import CFG_DB_BUSINESS, CFG_JOB_ENABLE, CFG_DB_MONITOR
from superbase.globalData import PROJECT_ROOT, gTop, gConfig
from superbase.utility.ioUtil import md5
from superbase.utility.logUtil import logException, logInfo
from superbase.utility.timeUtil import getTimestamp

VCODE_PATH = PROJECT_ROOT + "temp/vcode/"  # PROJECT_ROOT-->项目根


class VCode(object):

    @staticmethod
    def saveImage(driver, element, rect=None):
        """
        :param driver: 驱动程序
        :param element: 元素
        :param rect: None
        :return:
        """
        # http://stackoverflow.com/questions/10848900/how-to-take-partial-screenshot-frame-with-selenium-webdriver
        """
        1）sudo apt-get install libjpeg-dev
        2）sudo apt-get install libfreetype6-dev
        3）sudo  easy_install PIL #pip install Pillow
        """

        def element_screenshot(driver, element, filename):
            """
            元素位置
            :param driver:
            :param element:
            :param filename:
            :return:
            """
            if element:
                bounding_box = (  # 边界框
                    element.location['x'],  # left 位置左
                    element.location['y'],  # upper 位置上
                    (element.location['x'] + element.size['width']),  # right 位置右
                    (element.location['y'] + element.size['height'])  # bottom 位置下
                )
            else:
                bounding_box = rect  # rect-->None
            return bounding_box_screenshot(driver, bounding_box, filename)

        def bounding_box_screenshot(driver, bounding_box, filename):
            """
            调整图像
            :param driver:
            :param bounding_box:
            :param filename:
            :return:
            """
            # Python Imaging Library是Python平的图像处理标准库
            from PIL import Image
            # 保存当前窗口到PNG图像文件的屏幕截图。
            driver.save_screenshot(filename)
            # 打开并识别给定的图像文件。
            base_image = Image.open(filename)
            # 从这个图像返回一个矩形区域。盒子里是一个4元组定义左、上、右和下像素坐标。
            cropped_image = base_image.crop(bounding_box)
            # 调整尺寸
            base_image = base_image.resize(cropped_image.size)
            # 定义图形大小
            base_image.paste(cropped_image, (0, 0))
            # 保存
            base_image.save(filename)
            return base_image

        # 获取时间戳
        ts = getTimestamp()
        # 路径-->项目根+"temp/vcode/"
        tmpDir = VCODE_PATH
        # 测试一条路径是否存在。返回False，用于中断符号链接
        if not os.path.exists(tmpDir):
            os.makedirs(tmpDir)  # mkdir类似
        import random
        # 随机数  如果需要大量的 请用uuid.uuid4()
        rint = random.randint(1000, 9999)
        # 图片名称=本地时间戳+随机数
        imgName = "%s_%d.png" % (ts, rint)
        fn = tmpDir + imgName
        element_screenshot(driver, element, fn)
        return fn

    @staticmethod
    def vCodeCheck(driver, element, accountHelper, **params):
        """
        :param element:
        :param type:
        :return:
        """
        path = VCode.saveVcodeImage(driver, element)
        return accountHelper.getVCode(path, **params)

    @staticmethod
    def testVcode():
        """
        测试 code
        :return:
        """
        # 浏览器驱动->phantomjs
        driver = webdriver.PhantomJS()
        driver.get("http://hr.zhaopin.com/hrclub/index.html")
        # 匹配数据
        userName = driver.find_element(By.CSS_SELECTOR,
                                       "#form1 > ul:nth-child(1) > li:nth-child(1) > label:nth-child(1) > input:nth-child(1)")
        pwd = driver.find_element(By.CSS_SELECTOR,
                                  "#form1 > ul:nth-child(1) > li:nth-child(2) > label:nth-child(1) > input:nth-child(1)")
        vcode = driver.find_element(By.CSS_SELECTOR,
                                    "#form1 > ul:nth-child(1) > li:nth-child(3) > label:nth-child(1) > input:nth-child(1)")
        userName.send_keys("shanghaiwacai")
        pwd.send_keys("wacai2015")
        # driver.get("http://rd2.zhaopin.com/s/loginmgr/picturetimestamp.asp?t=1429060977000")
        url = "http://rd2.zhaopin.com/s/loginmgr/picturetimestamp.asp?t=%d" % (int(time.time() * 1000))
        VCode.saveVcodeImage(driver, driver.find_element(By.CSS_SELECTOR, "#vimg"))

    @staticmethod
    def saveVcodeImage(driver, element):
        """
        :param driver:
        :param element:
        :return:
        """
        # TODO:


class AccountInfo(object):
    """
    这是个账号相关的骨架，需要自行继承实现
    """

    def getMysqlParams(self, **params):
        """
        返回mysql链接参数，格式如下
        :return: {
            'host': '127.0.0.1',
            'passwd': '',
            'user': 'root',
            'port': 3306,
        }
        """
        raise "pls implement mysql paramas"

    def getVCode(self, imagePath, **params):
        """
        返回打码平台验证码
        :param imagePath: 图像
        :param params: 打码平台需要的参数
        :return: 打码结果
        """
        raise "implement getVCode"

    def getPCode(self, **params):
        """
        返回打码平台短信
        :param params:
        :return:打码结果
        """
        raise "implement getPCode"


class CookieManager(object):
    """
    登录问题：
        1，爬虫自行提供login功能，login的结果是save cookie
        save2Local
        sync2Remote

        2，分布式爬虫可以去取cookie if needed，
        syncFromRemote
        getFromLocal

        3, cookie管理
        cookie失败
        delFromLocal
        sync2Remote
    """

    def __init__(self):
        self.sqlite = LocalDb().getDb()

    @classmethod
    def createMD5Idx(cls, type, source, inTime):
        return md5("%s/%s/%s" % (type, source, inTime))

    def addOne(self, val, source=None):
        """
        :param source: 具体网站
        :param val: 具体值
        :param tpe: 如网站cookie，网站账号
        :return:
        """
        if not source:
            source = gConfig.get(CFG_DOWN_WEBSITE)

        currTime = getTimestamp()
        md5Idx = self.createMD5Idx(ACCOUNT_TPE_COOKIE, source, currTime)
        data = {
            "md5idx": md5Idx,
            "source": source,
            "val": json.dumps(val),
            "inTime": currTime,
            "type": ACCOUNT_TPE_COOKIE,
        }
        self.sqlite.insert("cookie",
                           data
                           )
        self.add2Remote(data)
        return md5Idx

    def delOne(self, md5idx):
        cond = "where md5idx='%s'" % md5idx
        self.sqlite.delete("cookie", cond)
        self.delRemote(cond)

    def getOne(self, cond=""):
        self.checkSync()
        row = self.sqlite.getRow("select md5idx,val from cookie %s order by inTime desc" % cond)
        if row:
            return {
                "md5Idx": row[0],
                "val": json.loads(row[1]),
            }
        else:
            return None

    def add2Remote(self, data):
        if gConfig.get(CFG_JOB_ENABLE):
            db = gTop.get(CFG_DB_MONITOR)
            db.insert("account", data)

    def delRemote(self, cond):
        if gConfig.get(CFG_JOB_ENABLE):
            db = gTop.get(CFG_DB_MONITOR)
            db.delete("account", cond)

    def checkSync(self):
        if gConfig.get(CFG_JOB_ENABLE):
            db = gTop.get(CFG_DB_MONITOR)
            source = gConfig.get(CFG_DOWN_WEBSITE)
            cond1 = "source='%s' and `type`='%s'" % (source, ACCOUNT_TPE_COOKIE)
            remoteTime = db.getOne("select max(inTime) from account where %s" % cond1)
            localTime = self.sqlite.getOne("select max(inTime) from cookie")
            if not remoteTime:
                remoteTime = "20000102030405"
            if not localTime:
                localTime = "20000102030405"
            fields = "md5idx,val,source,status,inTime"
            remote = (db, "account")
            local = (self.sqlite, "cookie")

            def sync(from1, to, smalltime):
                db1, table1 = from1
                db2, table2 = to
                rows = db1.query("select %s from %s where inTime>'%s' and %s " % (fields, table1, smalltime, cond1))
                for row in rows:
                    data = dict(zip(fields.split(","), row))
                    data["type"] = ACCOUNT_TPE_COOKIE
                    db2.insert(table2, data)

            if remoteTime > localTime:
                sync(remote, local, localTime)

            elif remoteTime < localTime:
                sync(local, remote, remoteTime)
