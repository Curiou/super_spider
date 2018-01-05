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
import multiprocessing
import os
import subprocess
import sys
import threading
import time

from superbase.constant import CFG_DB_MONITOR, CFG_DB_BUSINESS
from superbase.utility import timeUtil
from superbase.utility.logUtil import logException, logDebug


def assert2(condition, info="assert error"):
    """
    声明
    :param condition: 环境
    :param info: 错误消息
    :return:
    """

    if not condition:
        print condition
        # raise AssertionError(info)
        assert (condition)


def runProcess(cmd, outInfo=None, maxOutInfoNum=1000, debug=False, redirect=False):
    """
    运行多进程
    :param cmd:
    :param outInfo: 输出的console信息list
    :param log: 可定制的logger
    :param maxOutInfoNum: 最多输出的console 信息行数
    :param debug: debug模式只是输出命令行
    :param redirectFile: 是否用重定向文件模式
    :return:
    """
    # cmd += "\n" #what the hell use it?
    from superbase.utility.logUtil import logInfo
    try:
        if redirect:
            idx = cmd.rfind(">")
            if idx > 0:  # 判断是否需要重定向,重定向必须是绝对路径
                outfile = cmd[idx + 1:].strip()
                outfile = os.path.abspath(outfile)
                logInfo("redirect-file=%s" % outfile)
                dir1 = os.path.dirname(outfile)
                from superbase.utility.ioUtil import mkdir
                mkdir(dir1)
                redirectFile = open(outfile, "w")
                cmd = cmd[:idx]
        else:
            redirectFile = None
        logDebug("\n%s the cmd is %s\n" % (timeUtil.getCurTime(), cmd))
        if debug:
            return
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        lineNum = 0
        while True:
            line = p.stdout.readline()
            if not line:
                break
            # log.debug(line)
            if (outInfo != None):
                outInfo.append(line);
                lineNum += 1
                if maxOutInfoNum > 0 and lineNum > maxOutInfoNum:
                    del outInfo[:-1]
                    lineNum = 0
                    if redirectFile:
                        redirectFile.flush()
                if redirectFile:
                    redirectFile.write(line)
        if redirectFile:
            redirectFile.close()

        logDebug("process-done:%s" % cmd)
    except Exception:
        from superbase.utility.logUtil import logException
        logException()

    return outInfo


class TProcessEngine(threading.Thread):  #############这里有问题???
    """
    多线程引擎
    notifyDone is a class with a callback() method
    class Notify:
        def callback(self,outInfo=None):
            pass
    """

    def __init__(self, cmd, outInfo=None, maxOutInfoNum=1000, debug=False, redirect=False, hang=False, notifyDone=None):
        super(TProcessEngine, self).__init__()
        self.cmd = cmd
        self.outInfo = outInfo
        self.notifyDone = notifyDone
        self.debug = debug
        self.maxOutInfoNum = maxOutInfoNum
        self.redirect = redirect
        if not hang:
            self.start()

    # 运行
    def run(self):
        runProcess(self.cmd, self.outInfo, maxOutInfoNum=self.maxOutInfoNum, debug=self.debug, redirect=self.redirect)
        if self.notifyDone != None:
            self.notifyDone.callback(self.outInfo)


def timeoutFunc(cmd, timeout, interval=1):
    """
    超时处理
    :param cmd: class cmd:
                    def execute():
                      返回结果就结束任务,otherwise,继续
    :param timeout: 超时的时间
    :param interval: 延时间隔
    :return:
    """
    begin = time.time()
    while begin + timeout > time.time():
        time.sleep(interval)
        result = cmd.execute()
        if result:
            return result


def mThread(threadNum, func, argsList):
    """
    多线程
    :param threadNum: 线程数
    :param func: 要使用多线程的函数
    :param argsList: [（进程1的参数tuple,queue），（进程2的参数tuple）,...]
    :return:
    """
    record = []
    q = multiprocessing.Queue()

    class MyThread(threading.Thread):
        def __init__(self, args):
            threading.Thread.__init__(self)
            self.args = args

        def run(self):
            return func(*self.args)

    for i in range(threadNum):
        param = list(argsList[i])
        param.append(q)
        thread = MyThread(param)
        thread.start()
        record.append(thread)

    for thread in record:
        thread.join()
    return q


def mProcess(processNum, func, argsList):
    """
    多进程
    :param processNum: 进程数
    :param func: 要使用多进程的函数
    :param argsList: [（进程1的参数tuple），（进程2的参数tuple）,...]
    :return:
    """
    record = []
    q = multiprocessing.Queue()

    for i in range(processNum):
        param = list(argsList[i])
        param.append(q)
        process = multiprocessing.Process(target=func, args=tuple(param))
        process.start()
        record.append(process)

    for process in record:
        process.join()
    return q


def applyFunc(obj, strFunc, arrArgs):
    """
    调用方法
    :param obj: 要使用的类
    :param strFunc: 方法名
    :param arrArgs: 参数
    :return:
    """
    try:
        objFunc = getattr(obj, strFunc)
        return apply(objFunc, arrArgs)
    except:
        logException()


def callMethod(cls, argv):
    """
    脚本的入口函数
    :param cls:class
    :param argv: cfg method params, cfg can be null
    :return:
    """
    try:
        cfg = argv[0]
        if cfg.find("=") > 0:
            obj = cls(cfg)
            return applyFunc(obj, argv[1], argv[2:])
        else:
            obj = cls()
            return applyFunc(obj, argv[0], argv[1:])
    except Exception:
        logException()
    finally:  # close global resource if has
        from superbase.globalData import gTop
        gTop.release()


def callFunction(func, argv):
    """
    调用函数优化
    :param func: 要调用的方法
    :param argv: 参数
    :return:
    """
    try:
        apply(func, argv)
    except Exception:
        logException()


def reloadModule(name):
    """
    重新加载模块
    :param name: 模块名
    :return:
    """
    try:
        reload(sys.modules[name])
    except Exception:
        logException()


def isProcessAlive(cmd):
    """
    判断进程是否存活
    :param cmd:
    :return: True/False
    """
    import psutil
    for pid in psutil.pids():
        p = psutil.Process(pid)
        info = " ".join(p.cmdline())
        if info.find(cmd) >= 0:
            return True

    return False


def showProcess(exe='python'):
    """
    获取进程的进程号和cmdline
    :param exe:
    :return:
    """
    import psutil
    # 遍历所有运行的进程的进程号,然后通过进程号获取每个进程的cmdline
    for pid in psutil.pids():
        p = psutil.Process(pid)
        try:
            cmd = p.cmdline()  # 获取进程的cmdline,形式: /bin/bash
            if len(cmd) > 0:
                if exe:
                    if cmd[0].find(exe) < 0:
                        continue
                info = " ".join(cmd)
                print ("pid=%s %s" % (pid, info))
        except Exception:
            pass
