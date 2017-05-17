#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import requests
import re
import redis
import queue
import threading
from datetime import datetime
from elasticsearch import Elasticsearch
from multiprocessing import Process, JoinableQueue
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
    }
r = redis.StrictRedis(host='192.168.1.157', port=6379, db=0)
es = Elasticsearch("192.168.1.157:9200")


class AyouBlog():
    def __init__(self):
        threading.Thread.__init__(self)

    #    def get_page_url(self):
    #        urls_set = set()
    #        url = "http://blog.csdn.net/u013055678?viewmode=contents"
    #        try:
    #            html = self.s.get(url, headers=self.headers)
    #        except HTTPError as e:
    #            print(str(e))
    #            return str(e)
    #        except ConnectionError as e:
    #            print(str(e))
    #            return str(e)
    #        try:
    #            soup = BeautifulSoup(html.content, "lxml")
    #            page_div = soup.find_all("span", {"class": "link_title"})
    #            for url in page_div:
    #                a_url = "http://blog.csdn.net" + url.find("a").attrs["href"]
    #                urls_set.add(a_url)
    #        except AttributeError as e:
    #            print(str(e))
    #            return str(e)
    #        return urls_set
    def upload_page_list(self):
        for a in range(1, 51):
            url = 'https://www.renrenche.com/cq/ershouche/p' + str(a)
            page_url = requests.get(url, headers=headers, timeout=30)
            recom = re.compile(r'data-car-id="(.*?)"', re.S)
            car_page_url = re.findall(recom, page_url.text)
            for b in car_page_url:
                temp_car_page_url = 'https://www.renrenche.com/cq/car/' + str(b)
                r.set(b, temp_car_page_url)
        return 0


class ThreadUrl(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.s = requests.session()

    #    def run(self):
    #        while not self.queue.empty():
    #            host = self.queue.get()
    #            try:
    #                html = self.s.get(host, headers=self.headers)
    #            except HTTPError as e:
    #                print(str(e))
    #                return str(e)
    #            except ConnectionError as e:
    #                print(str(e))
    #                return str(e)
    #            try:
    #                soup = BeautifulSoup(html.content, "lxml")
    #                class_div = soup.find("span", {"class": "link_title"})
    #                print((class_div.text).strip())
    #            except AttributeError as e:
    #                print(str(e))
    #                return str(e)
    #            except NavigableString as e:
    #                print(str(e))
    #                return str(e)
    #            self.queue.task_done()
    def download(self):
        try:
            redis_download_url = r.keys("*")
            for a in redis_download_url:
                redis_download_url_temp = r.get(a)
                c = requests.get(redis_download_url_temp)
                re_car_name = re.compile('<title>(.*)</title>', re.S)
                car_name = re.findall(re_car_name, c.text)

                re_car_money = re.compile(u'<span class="dialog-price">(.*)万</span>  &nbsp;建议价')
                car_money = re.findall(re_car_money, c.text)
                data = {
                    "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0800"),
                    "car_name": car_name,
                    "car_money": car_money
                }
                es.index(index="car_name", doc_type="car_name", body=data)
        except Exception as e:
            return -1


#def main():
#    que = JoinableQueue()
#    p = AyouBlog()
#    p.upload_page_list()
#
#
#    for i in range(7):
#        t = ThreadUrl.download(que)
#        t.setDaemon(True)
#        t.start()
#
#    que.join()



#if __name__ == "__main__":
#    que = queue.Queue()
#    print ("Scpite is runing: %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#    p = AyouBlog()
#    p.upload_page_list()
#    print ("Download is runing %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#    s = ThreadUrl
#
#    for i in range(7):
#        t = s.download(que)
#        t.setDaemon(True)
#        t.start()
#
#    que.join()
#    start = time.time()
#
#    print("Elapsed Time: %s" % (time.time() - start))

def main():    #进程列表  
    worker_list = list()  
  
    #创建队列  
    queue = JoinableQueue()  
  
    #将URL放进队列  
    p = AyouBlog()  
    for url in p.upload_page_list():  
        print(str(url))
        queue.put(str(url)) 
  
    #开多进程  
    for i in range(3):  
        t = ThreadUrl(queue)  
        worker_list.append(t)  
        t.start()  
  
    #队列清空后再执行其它  
    queue.join()  
   
     #进程关闭(这个是不是多余啊?)  
    for w in worker_list:  
        w.terminate()  
   
   
if __name__=="__main__":  
    start = time.time()  
    main()  
    print("Elapsed Time: %s" % (time.time() - start))  
