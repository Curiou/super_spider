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
import random
import time
from urllib import urlencode

import requests
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from superbase.globalData import gConfig
from superbase.utility.logUtil import logException, logInfo, logError

from spiderx.common.utility.crawlerUtil import findElement, encoded_dict, getElementSync
from spiderx.common.utility.parseUtil import unescape
from spiderx.common.constant import CFG_HTTP_INTERVAL, CFG_HTTP_TIMEOUT, CFG_HTTP_ENCODING, \
    CFG_HTTP_MAXREQUEST, CFG_HTTP_UNESCAPE, CFG_HTTP_BROWSER, CFG_HTTP_OUTFORMAT, CFG_HTTP_UA, CFG_DOWN_IMAGE, \
    CFG_HTTP_INITURL, CFG_HTTP_PROXY_INTERVAL, CFG_HTTP_ACCOUNT_INTERVAL, GD_HTTP_DRIVER, CFG_HTTP_INITCOOKIE, \
    CFG_HTTP_INITPROXY


def getHeadersFromDriver(driver, host=None, refer=None, contentType=None):
    """
    pageReferrInSession=http%3A//rdsearch.zhaopin.com/Home/ResultForCustom%3FSF_1_1_3%3D201300%26SF_1_1_6%3D639%26SF_1_1_31%3D5%26SF_1_1_30%3D2%26orderBy%3DDATE_MODIFIED%2C1%26pageSize%3D60%26SF_1_1_27%3D0%26exclude%3D1;
    urlfrom2=121124551;
    adfcid2=by_kw_zdty_qg_000235;
    adfbid2=0;
    dywea=95841923.3513940260523865000.1428384342.1430274046.1430283454.25;
    dywez=95841923.1429449181.12.5.dywecsr=my.zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/myzhaopin/editscho.asp;
    __utma=269921210.2068750238.1428384342.1430274046.1430283459.25;
    __utmz=269921210.1430111192.16.6.utmcsr=hr.zhaopin.com|utmccn=(referral)|utmcmd=referral|utmcct=/hrclub/index.html;
    Hm_lvt_38ba284938d5eddca645bb5e02a02006=1428384342;
    __xsptplus30=30.2.1429281412.1429282493.2%231%7Cother%7Ccnt%7C121124551%7C%7C%23%23bPB6URjmCoyj_yBz16RckXLY5JIuaona%23;
    __zpWAM=1428384357788.259201.1429341084.1429356278.8; utype=0;
    rdgroup=3;
    __utmv=269921210.|2=Member=205765882=1;
    Home_1_CustomizeFieldList=3%3b4%3b5%3b6%3b9%3b31%3b30%3b29%3b7;
    Home_ResultForCustom_orderBy=DATE_MODIFIED%2C1;
    Home_ResultForCustom_pageSize=60; strloginusertype=4;
    LastCity=%e4%b8%8a%e6%b5%b7;
    LastCity%5Fid=538; dywec=95841923; cgmark=2;
    JsNewlogin=205765882; isNewUser=1;
    RDpUserInfo=;
    __utmc=269921210;
    pageReferrInSession=;
    RDsUserInfo=347320664E73556A47655D6144645073466752775D6853735F663F73296A4A651B611B6407731D670D770D6800730D660473066A146509611A645D7326672477586809149B07FF165C6A396526614E645D7331672E775868567352664273526A4E65506145645E73486728772B685C736E28041EA03E3A07892E1C04B70AF305631035FE0D229C354873336A3A655561486423733E6757771C68087306661A73096A37651F6112640573126703771168047307661B73496A146507611E645D7320673E77586850735F663273336A4A655C615E6454734A674A77546850735E6647735E6A4C652C6137645B7344675C77546854735D664B73516A4F655361376428734E6760391205A6272904923C080AA61CE8037A0336E51F3692245E682D7329664E73576A4765586142645D7330672E775868547357664B735C6A366524614E64567348673F7724685C735F663073266A4A652B613064517345675B77506858735C6645735F6A4F655361376427734E6729772668567352664273526A4E65506145645E734B67517721682273596643735C6A246521614E645E734867237735685C7356664773556A596559614264547348673F7731685C7355664373566A4C652;
    SearchHistory_StrategyId_1=%2fHome%2fResultForCustom%3fSF_1_1_3%3d210500%26SF_1_1_4%3d4%252c4%26SF_1_1_6%3d530%26SF_1_1_30%3d3%26SF_1_1_27%3d0%26orderBy%3dDATE_MODIFIED%252c1%26pageSize%3d60%26exclude%3d1%26pageIndex%3d4; NSC_WT-trvje-dbnqvt=ffffffffc3a01f0845525d5f4f58455e445a4a423660; dyweb=95841923.1.10.1430283454; __utmb=269921210.1.10.1430283459

    #ours
    RDsUserInfo=316629614E724664567351664B73556A416558645F6D5373497428663D645B7316675877526857665F6146724D64577357661E730F6A0D655364336D2F734F740C018C05EA16486724772B6859665661317230645B7356664473546A45655D645F6D507341745F66316428734E6760391205A3322003923D1B04B70AE4047A1437FC1B3490375D6D35733F745966486423733E6757771C680D660F611A721A64267313661273046A16650164126D047311740C665D6405731C6707775E68376639614E7245645D73256627735A6A43654564546D58735274556642645C7341675F775E68206629614E724664517357664173526A4E655964556D5A7336742A664E646C3D040AAD23280A85290201A20BF4066F1434F01F229F394C6524642B6D5C7342745466436457734867297721685966586140724C645D7325663F735A6A47655364336D20734F745F66306427734E672977266856665A614072466453735D664273546A4F655364226D20734F7427663064547344675977576851665461427247645E735F663773246A4A6558645D6D32733B74596640645D733A673A7758685666596141725A645773556641735C6A22653C645B6D50734274556648646;
    __utmz=269921210.1430277915.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none);
    __utmc=269921210;
    __utmb=269921210.5.9.1430277946262;
    __utma=269921210.550749975.1430277915.1430277915.1430277915.1;
    dyweb=95841923.4.9.1430277946260;
    dywec=95841923;
    dywea=95841923.1645969264643977000.1430277915.1430277915.1430277915.1;
    rdgroup=3;
    isNewUser=1;
    box=true;
    cgmark=2;
    RDpUserInfo=;
    JsNewlogin=205826092;
    dywez=95841923.1430277915.1.1.dywecsr=(direct)|dyweccn=(direct)|dywecmd=(none)|dywectr=undefined;GUID=7099bf4eac3f4f1b8558a9ff0f7d66d9;
    pageReferrInSession=http%3A//rd2.zhaopin.com/portal/myrd/regnew.asp%3Fza%3D2;
    """
    cookies = driver.get_cookies()
    cookies2 = ";".join(["%s=%s" % (cookie['name'], cookie['value']) for cookie in cookies])
    headers = {
        # "Host":host,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": cookies2,
        # "Referer":"http://ehire.51job.com/Candidate/SearchResume.aspx",
        "Connection": "keep-alive",
        # "Content-Type":"application/x-www-form-urlencoded"
    }
    if host:
        headers["Host"] = host
    if refer:
        headers["Referer"] = refer
    if contentType:
        headers["Content-Type"] = contentType

    return headers


def encGetParam(params):
    """
    整体是将传来的字典转换成key1=value1&key2=value2形式
    :param params:
    :return:
    """
    newParams = encoded_dict(params)
    encParam = urlencode(newParams)
    return encParam


def encPostParam(params, headers):
    """
    将传来的字典转换成key1=value1&key2=value2形式且添加Content-Length头子段
    :param params:
    :param headers:
    :return:
    """
    newParams = encoded_dict(params)
    encParam = urlencode(newParams)
    headers['Content-Length'] = "%d" % (len(encParam))
    return encParam


def urlDecode(str):
    """
    将gbk形式的html编码转换成str型的
    :param str:
    :return:
    """
    from urllib import unquote
    return unquote(str)


def getDriver(driver='headless', ua=None, params=None):
    """
    获得selenium的driver
    :param driver:
    :param ua:
    :param params: driver参数，如代理ip，TODO
    :return:
    """
    from selenium import webdriver
    if driver == 'headless':
        return getPDriver(ua=ua)
    else:
        if driver == "chrome":  # 用chrome做引擎options添加用户头
            from selenium.webdriver.chrome.options import Options
            _chrome_options = Options()
            _chrome_options.add_argument('disable-infobars')
            # _chrome_options.add_argument("--user-data-dir=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data/Default");
            _chrome_options.add_argument("--start-maximized")
            _chrome_options.add_argument("allow-running-insecure-content")
            _chrome_options.add_argument("--test-type")
            return webdriver.Chrome(chrome_options=_chrome_options)
        elif driver == "firefox":
            return webdriver.Firefox()
        elif driver == "ie":
            return webdriver.Ie()


def getPDriver(ua=None):
    """配置phantomJs的参数，可以配置
    FIREFOX = {
        "browserName": "firefox",  # 浏览器名称
        "version": "",             # 操作系统版本
        "platform": "ANY",         # 平台，这里可以是windows、linux、andriod等等
        "javascriptEnabled": True, # 是否启用js
        "marionette": True,        # 这个值没找对应的说明^_^  不解释了
        }
        加载动态数据返回driver驱动
    """
    from selenium import webdriver
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    if not ua:
        ua = gUAgents['windows'][0]
    # 伪造ua信息
    dcap["phantomjs.page.settings.userAgent"] = (ua)
    dcap["phantomjs.page.settings.loadImages"] = True if gConfig.get(CFG_DOWN_IMAGE, 0) else False
    # 添加头文件
    # dcap["phantomjs.page.customHeaders.Referer"] = (
    #    "https://www.google.com/"
    # )
    driver = webdriver.PhantomJS(
        # executable_path='./phantomjs',
        # service_args=service_args,
        desired_capabilities=dcap
    )
    return driver


def nullFunc(*param):
    return None


# User-Agent 头，可以随机取，有些时候高级头获取不到的数据，低级头就可以，
gUAgents = {
    "windows": (
        "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; TencentTraveler 4.0; .NET CLR 2.0.50727)",
    ),
    "mac": (
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    ),
    "android": (
        "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
        "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    ),
    "ios": (
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    ),
}


class ScrollDownHandler2(object):
    """
    这个问题是watiElement是不准的,只用延时就好
    """

    def __init__(self, waitSeconds=1, waitElement=None):
        """
        :param waitSeconds: 简单一点延时等待
        :param waitElement: 精确一点，就用底部元素（key，val）形式,todo,这个慎用
        """
        self.waitSeconds = waitSeconds
        self.waitElement = waitElement

    def handle(self, driver):
        js = "var q=document.documentElement.scrollTop=10000"
        # 加载js文件
        driver.execute_script(js)
        if self.waitElement:
            getElementSync(driver,
                           self.waitElement)  # 调用crawlerUtil里得getElementSync方法，这个方法底层实用了selenium的WebDriverWait，属于显示等待
        time.sleep(self.waitSeconds)  # time定时属于强制等待


class ScrollDownHandler(object):
    """
    向下滚动长度
    """

    def __init__(self, interval=1, intervalLength=4000, totalScroll=25):
        """
        默认拖动25次,10000个像素
        :param interval: 拖动间隔时间(等待刷新)
        :param intervalLength: 拖动长度
        :param totalScroll: 总拖动次数
        """
        self.interval = interval
        self.intervalLength = intervalLength
        self.totalScroll = totalScroll

    def handle(self, driver):
        wait = 0
        while wait < self.totalScroll:
            # 向下拖动一次加载一次
            driver.execute_script("window.scrollBy(0,%s)" % self.intervalLength)
            time.sleep(self.interval)
            wait += 1
        logInfo("scroll down done:interval=%s,len=%s,count=%s" % (self.interval, self.intervalLength, self.totalScroll))


class PageDownHandler(object):
    """
    这个时灵时不灵,慎用
    """

    def __init__(self, interval=1, totalScroll=25):
        """
        :param interval: 拖动间隔时间(等待刷新)
        :param totalScroll: 总拖动次数
        ActionChains：理解链接http://blog.csdn.net/huilan_same/article/details/52305176
        """
        self.interval = interval
        self.totalScroll = totalScroll

    def handle(self, driver):
        wait = 0
        # 创建鼠标键盘点击事件
        action = ActionChains(driver)
        while wait < self.totalScroll:
            action.send_keys(Keys.PAGE_DOWN).perform()  # 发送某个键到当前焦点的元素
            time.sleep(self.interval)
            wait += 1
        logInfo("page down done:interval=%s,count=%s" % (self.interval, self.totalScroll))


def getOneProxyFromPool():
    """
    TODO:
    :return: type,value,如http，http://10.10.1.10:3128
    """


def getOneCookieFromPool():
    """
    TODO:ip代理模块
    :return:type,value,如http，http://10.10.1.10:3128
    """


class HttpAgent(object):
    """
    requests 封装
    """

    def __init__(self):

        self.downNum = 0
        self.downBegin = time.time()
        self.reqNum = 0
        self.newSession()
        self.currentPage = None
        self.antiBlock = None
        self.afterLoadHandler = None

    def setAfterLoad(self, handler):
        """
        后处理，如scroll down
        :param handler: 原型支持接口：
            class MyHandler:
                def handle(self,driver):
                    pass
        :return:
        """
        # 直接给afterLoadHandler赋值handler
        self.afterLoadHandler = handler

    def afterLoad(self):
        """
        后加载的
        :return:
        """
        self.reqNum += 1
        if self.afterLoadHandler:
            self.afterLoadHandler.handle(self.driver)

    def beforeLoad(self):
        """
        用于判断什么时候替换IP，cookie，session
        """
        stime = self._getInterval()  # 返回一个间隔时间
        time.sleep(stime)
        needNewOne = 0
        proxyInterval = gConfig.get(CFG_HTTP_PROXY_INTERVAL, 0)  # CFG_HTTP_PROXY_INTERVAL换代理的间隔，是以次计算
        if proxyInterval and self.reqNum >= proxyInterval:
            self.newProxy()  # 调用IP代理模块
            logInfo("change proxy")  # 打印log日志
            needNewOne += 1

        accountInterval = gConfig.get(CFG_HTTP_ACCOUNT_INTERVAL, 0)  # CFG_HTTP_ACCOUNT_INTERVAL换账号的间隔，是以次计算
        if accountInterval and self.reqNum >= accountInterval:
            self.newCookie()  # 调用登录账号模块
            logInfo("change account")
            needNewOne += 1

        maxRequest = gConfig.get(CFG_HTTP_MAXREQUEST)  # CFG_HTTP_MAXREQUEST一个session 最大能请求次数失效
        if maxRequest and self.reqNum >= maxRequest:
            needNewOne += 1

        if needNewOne > 0:
            self.newSession()  # 调用提取响应的session值模块

    def setAntiBlock(self, antiBlock):
        """
        只是给antiBlock传一个防阻塞函数 fixme 有可能理解不对
        :param antiBlock:
        :return:
        """
        self.antiBlock = antiBlock

    def isBlocked(self):
        """
        antiBlockUtil返回blocked的值或False
        :return:
        """
        if self.antiBlock:
            return self.antiBlock.isBlocked()
        else:
            return False

    def _getUA(self):
        """
        返回一个随机取一个的User-Agent头文件的值
        """
        uas = gUAgents[gConfig.get(CFG_HTTP_UA)]  # CFG_HTTP_UA herder的User-Agent头文件，
        idx = random.randint(0, len(uas) - 1)
        ua = uas[idx]
        logInfo("change http:%s" % (ua))
        return ua

    def _getInterval(self):
        """如果CFG_HTTP_INTERVAL有值就按设置的，如果没有就随机取
        isinstance是判断一个对象是否是一个已知的类型
        友情链接：http://www.runoob.com/python/python-func-isinstance.html
        find是检测字符串中是否包含子字符串 str
        返回的是时间间隔
        """
        stime = gConfig.get(CFG_HTTP_INTERVAL, 0.01)  # 设置爬取时间间隔，默认为0.01
        if isinstance(stime, basestring) and stime.find("-") > 0:  # 是range如1-10,取随机值
            begin, end = stime.split("-")
            begin, end = float(begin), float(end)
            total = end - begin
            stime = begin + random.random() * total
        return stime

    def checkResult(self, url, content):
        """
        下载校验结果
        :param url:
        :param content:
        :return:
        """
        if self.antiBlock:
            ret, handleStrategy = self.antiBlock.checkBlock(url, content)
            if ret:
                logError("##block:check it!!")
                detail = {
                    "interval": gConfig.get(CFG_HTTP_INTERVAL),  # 时间间隔
                    "downNum": self.downNum + self.reqNum,  # 下载数量
                    "downTime": time.time() - self.downBegin,  # 下载用的时间
                }
                self.antiBlock.handleBlock(url, content, handleStrategy, detail)

    def initSession(self):
        """
        初始化session的值
        :return:
        """
        self.downNum += self.reqNum
        self.reqNum = 0
        initUrl = gConfig.get(CFG_HTTP_INITURL, None)  # 调用initurl,用于获得cookie
        if initUrl:
            self.driver.get(initUrl)  # 访问url，获取响应

        if gConfig.get(CFG_HTTP_INITCOOKIE, None):  # 需要新的cookie ,1,0
            self.newCookie()  # 调用登录账号模块

        if gConfig.get(CFG_HTTP_INITPROXY, None):  # 需要新的proxy,1,0
            self.newProxy()  # 调用IP代理模块


class RequestsAgent(HttpAgent):
    def __init__(self):
        """
        继承HttpAgent初始化方法
        """
        HttpAgent.__init__(self)
        self.cookie = None
        self.proxy = None

    def newSession(self):
        """
        更新响应的头文件
        :return:
        """
        # 通过制动化提取响应的session值
        self.driver = requests.session()
        ua = self._getUA()  # User-Agent头
        self.driver.headers.update({
            "User-Agent": ua,
        })
        self.initSession()

    def _fetchData(self, url, func="get", data=None):
        """
        返回一个解码后的结果content
        :param url:
        :param func:
        :param data:
        :return:
        """
        try:
            self.beforeLoad()  # 调用更换ip，cookie 或session的
            timeout = gConfig.get(CFG_HTTP_TIMEOUT, 30)  # 超时等待

            params = {"timeout": timeout}
            if self.cookie:
                params["cookies"] = self.cookie
            if self.proxy:
                params["proxies"] = self.proxy

            if func == "get":  # 访问请求的方式
                r = self.driver.get(url, **params)
            else:
                r = self.driver.post(url, data=data, **params)
            if r.status_code != 200:  # 判断响应返回的状态码
                logError("%s:get url %s" % (r.status_code, url))
            self.afterLoad()
            outFormat = gConfig.get(CFG_HTTP_OUTFORMAT, None)
            if outFormat != "file":
                r.encoding = gConfig.get(CFG_HTTP_ENCODING, "utf-8")
                self.currentPage = r.text
                if gConfig.get(CFG_HTTP_UNESCAPE, None):  # 是否反向转译
                    self.currentPage = unescape(self.currentPage)
                # saveWrongPage(r.text,"test2.html")
                self.checkResult(url, self.currentPage)  # 校验结果
                content = r.json() if outFormat == "json" else self.currentPage
            else:
                content = r

            return content
        except Exception:
            self.newSession()  # 更换头文件获取新的session
            logException()

    def get(self, url):
        """
        返回一个解码后的结果content因为_fetchData是私有方法
        :param url:
        :return:
        """
        return self._fetchData(url)

    def post(self, url, params):
        """
        返回一个解码后的结果content因为_fetchData是私有方法
        :param url:
        :param params:
        :return:
        """
        return self._fetchData(url, func="post", params=params)

    def newProxy(self):
        """
        调用IP代理池，返回一个k-v的值
        :return:
        """
        type, value = getOneProxyFromPool()
        self.proxy = {type: value}

    def newCookie(self):
        """
        调用登录账号池，返回登录的账号， fixme 有可能是一串cookie字符串
        :return:
        """
        self.cookie = getOneCookieFromPool()

    def test(self, r):
        """
        fixme 有一些没有理解
        在内存中读写content
        """
        from pyquery import PyQuery as pq
        from lxml import etree
        from StringIO import StringIO
        css = ".titleTr"
        parser = etree.HTMLParser(encoding='utf-8')  # 对网页解码
        r.encoding = "ISO-8859-1"
        content = r.text
        # StringIO是在内存中读写content。
        root = pq(etree.parse(StringIO(content), parser).getroot())
        print root(css).text()

    # deprecate
    def transcode(self, r):
        """
        对content进行转码
        :param r:
        :return:
        """
        try:
            return r.text.encode("utf-8").decode(r.encoding)
        except Exception:
            options = ("gbk", "ISO-8859-1", "ISO-8859-2", "gb2312")
            for option in options:
                try:
                    return r.text.encode("utf-8").decode(r.encoding)
                except Exception:
                    logException()


class SeleniumAgent(HttpAgent):
    def __init__(self):
        """
        继承HttpAgent初始化方法
        """
        self.driver = None
        HttpAgent.__init__(self)
        self.oriAbility = None
        self.ability = None

    def newSession(self):
        """
        设置浏览器的属性并访问
        """
        if not self.driver:
            from spiderx.common.baseCrawler import gSpider
            self.driver = getDriver(gConfig.get(CFG_HTTP_BROWSER, "headless"), self._getUA())  # 设置浏览器的类型
            self.driver.maximize_window()  # set_window_size(1920, 1080)# 设置浏览器的大小
            self.oriAbility = self.driver.capabilities
            self.ability = self.oriAbility.copy()
            gSpider.get(GD_HTTP_DRIVER).append(self.driver)  # 断点控制
        else:
            self.driver.start_session(self.ability)
        self.initSession()

    def newProxy(self):
        """
        设置IP代理
        :return:
        """
        from selenium.webdriver import Proxy
        from selenium.webdriver.common.proxy import ProxyType

        proxy = Proxy(
            {
                'proxyType': ProxyType.MANUAL,
                'httpProxy': getOneProxyFromPool()[1]
            }
        )
        proxy.add_to_capabilities(self.ability)  # 将所需的功能传递给构造函数

    def newCookie(self):
        """
        设置cookie
        """
        cookie = getOneCookieFromPool()
        self.driver.delete_all_cookies()
        self.driver.add_cookie(cookie)  # 将所需的cookie传递给构造函数

    def get(self, url):
        try:
            self.beforeLoad()
            self.driver.get(url)
            self.afterLoad()
            self.currentPage = self.driver.page_source  # page_source方法可以获取到页面源码。
            self.checkResult(url, self.currentPage)
            # TODO,possible encoding process
            return self.currentPage
        except Exception:
            logException("%s" % (url))

    def getElementByCss(self, css):
        """
        定位到css
        :param css:
        :return:
        """
        return findElement(self.driver, By.CSS_SELECTOR, css)

    def close(self):
        """
        关闭浏览器
        :return:
        """
        if self.driver:
            self.driver.quit()
