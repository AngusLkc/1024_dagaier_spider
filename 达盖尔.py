#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
import inspect
import logging
import requests
import threading
from pyquery import PyQuery as pq
from Queue import Queue as queue

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)-6s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
logging.addLevelName(50,'CRIT')
logging.addLevelName(30,'WARN')

header={
    "User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Accept-Encoding":"gzip, deflate",
    "Connection":"close"
}

'''国内抓取需配置代理'''
proxy={"http":"socks5://127.0.0.1:1088","https":"socks5://127.0.0.1:1088"}

class ThreadManager(object):
    def __init__(self,num):
        self.thread_num=num
        self.queue=queue()
        self.threadlist=list()
        self.shutdown=threading.Event()
    
    def add_task(self,topic_url,topic_title):
        self.queue.put((topic_url,topic_title))
    
    def __start__(self):
        for i in range(self.thread_num):
            i=ThreadWork(self.queue,self.shutdown,i)
            i.start()
            self.threadlist.append(i)
    
    def waitcomplete(self):
        for i in self.threadlist:
            if i.isAlive():
                i.join()
    
    def isEmpty(self):
        return self.queue.empty()
    
    def __close__(self):
        self.shutdown.set()

class ThreadWork(threading.Thread):
    def __init__(self,work_queue,shutdown,num):
        threading.Thread.__init__(self)
        self.setName(str(num))
        self.tasklist=work_queue
        self.shutdown=shutdown
        self.setDaemon(True)

    def run(self):
        while True:
            if self.shutdown.isSet():
                logging.info(u"线程ID：%s，检测到线程退出标志！"%(self.getName()))
                break
            try:
                url,title=self.tasklist.get(timeout=1)
            except:
                continue
            else:
                dagaier(url,title)

def dagaier(topicurl,title):
    req=requests.session()
    req.headers.update(header)
    req.proxies.update(proxy)
    req.adapters.DEFAULT_RETRIES=5
    req.keep_alive=False
    topic_req=req.get(topicurl,timeout=5)
    topic_req.encoding='gbk'
    if topic_req.status_code!=200:
        logging.warning(u"线程ID：%s，下载主题页失败, Status:%s, URL:%s"%(threading.currentThread().getName(),topic_req.status_code,topicurl))
        return False
    topic_pq=pq(topic_req.text)
    imglist=topic_pq("div[class='tpc_content do_not_catch']>input[type='image']").items()
    for item in imglist:
        if item.attr('src') is not None:
            downimg(item.attr('src'),title)
        elif item.attr('data-src') is not None:
            downimg(item.attr('data-src'),title)
        else:
            logging.warning(u"线程ID：%s，读取帖子内图片URL失败, URL:%s"%(threading.currentThread().getName(),topicurl))
            return False

def downimg(url,title):
    req=requests.session()
    req.headers.update(header)
    req.proxies.update(proxy)
    req.adapters.DEFAULT_RETRIES=5
    req.keep_alive=False
    imgname=url.split('/')[-1]
    try:
        img_req=req.get(url=url,timeout=5)
    except:
        return False
    img_req.encoding='gbk'
    if img_req.status_code==200:
        if not os.path.exists("./images"):
            try:
                os.makedirs("./images")
            except:
                return False
        if not os.path.exists("./images/"+title):
            try:
                os.makedirs("./images/"+title)
            except:
                return False
        with open('./images/'+title+'/'+imgname,'wb+') as fd:
            fd.write(img_req.content)
        return True
    else:
        logging.warning(u"线程ID:%s，下载图片失败, Status:%s, URL:%s"%(threading.currentThread().getName(),img_req.status_code,url))
        return False

if __name__=='__main__':
    os.chdir(os.path.dirname(os.path.realpath(inspect.getfile(inspect.currentframe()))))
    work_manager=ThreadManager(8) #线程数
    work_manager.__start__()
    req=requests.session()
    req.headers.update(header)
    req.proxies.update(proxy)
    req.adapters.DEFAULT_RETRIES=5
    req.keep_alive=False
    BasicURL='http://t66y.com/'
    offset=0
    error_count=0
    while offset<10: #主题列表分页数
        offset+=1
        if error_count>=3:
            logging.error(u"遍历主题列表页失败！页码:%i"%(offset))
            error_count=0
            continue
        PageList='http://t66y.com/thread0806.php?fid=16&search=&page='+str(offset)
        Page_Obj=req.get(url=PageList)
        Page_Obj.encoding='gbk'
        if Page_Obj.status_code!=200:
            error_count+=1
            logging.warn(u"下载主题列表分页失败：%i，重试:%i"%(offset,error_count))
            offset-=1
            continue
        error_count=0
        PagePQ=pq(Page_Obj.text)
        TopicList=PagePQ("tbody>tr[class='tr3 t_one tac']>.tal>h3>a").items()
        for i in TopicList:
            if i.attr('href')[0:8]=='htm_data':
                work_manager.add_task(BasicURL+i.attr('href'),i.text())
    while not work_manager.isEmpty():
        time.sleep(1)
    logging.info(u"设置程序关闭标志")
    work_manager.__close__()
    logging.info(u"等待所有线程退出")
    work_manager.waitcomplete()
    sys.exit(0)
