# -*- codeing: utf-8 -*-
#import time
import requests
import re
import redis
#import Queue
import threading

from datetime import datetime
from elasticsearch import Elasticsearch
from time import ctime,sleep



headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
r = redis.StrictRedis(host='192.168.1.135',port=6379,db=0)
es = Elasticsearch("192.168.1.157:9200")

#class Mytheard(threading.Thread):
#    """docstring for Mytheard"""
#    def __init__(self,t_name, Queue):
#        threading.Theard.__init__(self, name = t_name)
#        self.data = Queue
exitFlag = 0


class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print ("Starting " + self.name)
        upload_page_list(self.name, self.counter)

        print ("Exiting " + self.name)


def upload_page_list(threadName, delay):
    for a in range(1,51):
        url = 'https://www.renrenche.com/cq/ershouche/p' + str(a)
        page_url = requests.get(url,headers = headers,timeout = 30)
        recom = re.compile(r'data-car-id="(.*?)"',re.S)
        car_page_url = re.findall(recom,page_url.text)
        for b in car_page_url:
            temp_car_page_url = 'https://www.renrenche.com/cq/car/' + str(b)
            r.set(b,temp_car_page_url)
    return 0

#print (upload_page_list())

#print (download())

threadLock = threading.Lock()
threads = []
t1 = myThread(1, "Thread-1", 1)
t2 = myThread(2, "Thread-2", 2)
threads.append(t1)
threads.append(t2)
#d1 = threading.Thread(target= download)
#d2 = threading.Thread(target= download)
#d3 = threading.Thread(target= download)
#d4 = threading.Thread(target= download)


if __name__ == '__main__':
    print('thread %s is running...' %threading.current_thread().name)
    for t in threads:
        t.start()
    print ("RenRencha Is runing %s" %ctime())
