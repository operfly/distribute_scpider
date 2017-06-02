# -*- codeing: utf-8 -*-
#import time
import requests
import re
import redis
#import Queue
import threading,multiprocessing

from datetime import datetime
from elasticsearch import Elasticsearch
from time import ctime,sleep



headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
r = redis.StrictRedis(host='192.168.1.157',port=6379,db=0)
es = Elasticsearch("192.168.1.157:9200")

#class Mytheard(threading.Thread):
#    """docstring for Mytheard"""
#    def __init__(self,t_name, Queue):
#        threading.Theard.__init__(self, name = t_name)
#        self.data = Queue




def upload_page_list():
    for a in range(1,80):
        url = 'https://www.renrenche.com/cq/ershouche/p' + str(a)
        page_url = requests.get(url,headers = headers,timeout = 30)
        recom = re.compile(r'data-car-id="(.*?)"',re.S)
        car_page_url = re.findall(recom,page_url.text)
        for b in car_page_url:
            temp_car_page_url = 'https://www.renrenche.com/cq/car/' + str(b)
            r.set(b,temp_car_page_url)
    return 0

#print (upload_page_list())

def download():
    try:
        redis_download_url = r.keys("*")
        for a in redis_download_url:
            redis_download_url_temp = r.get(a)
            c = requests.get(redis_download_url_temp)
            re_car_name = re.compile('<title>(.*)</title>',re.S)
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
#print (download())



if __name__ == '__main__':
    print("RenRencha Is runing  %s" % ctime())
    for a in range(5):
        b = threading.Thread(target=upload_page_list(),name ='Thread'+str(a))
        b.start()
        print('thread %s is running...' % threading.current_thread().name)
        b.join()
    for c in range(5):
        d = threading.Thread(target=download(),name = 'Thread ' +str(a))
        d.start()
        print('thread %s is running...' % threading.current_thread().name)
        d.join()
    print ("RenRencha Is over  %s" %ctime())