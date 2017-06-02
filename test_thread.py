# -*- codeing: utf-8 -*-
#import time
import requests
import re
import redis
import threadpool
#import Queue
import pool
import threading,multiprocessing
from requests.exceptions import HTTPError,ConnectionError
from multiprocessing import Pool
from datetime import datetime
from elasticsearch import Elasticsearch
from time import ctime,sleep
from multiprocessing import Process, JoinableQueue 


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
r = redis.StrictRedis(host='192.168.1.157',port=6379,db=0)
es = Elasticsearch("192.168.1.157:9200")

#class Mytheard(threading.Thread):
#    """docstring for Mytheard"""
#    def __init__(self,t_name, Queue):
#        threading.Theard.__init__(self, name = t_name)
#        self.data = Queue


class My_upload_thread(threading.Thread):
    """docstring for My_upload_thread"""
    def __init__(self):
        
        self.s = requests.session()
        

    def upload_page_list(self):
        url = 'https://www.renrenche.com/cq/ershouche/p'
        try:
            for a in range(1,80):
                page_url = requests.get(url + str(a),timeout = 30,headers = headers)
                recom = re.compile(r'data-car-id="(.*?)"',re.S)
                car_page_url = re.findall(recom,page_url.text)
        except HTTPError as e:
            print(str(e))
            return(str(e))
        except ConnectionError as e:
            print(str(e))
            return(str(e))

        try:
            for b in car_page_url:
                temp_car_page_url = 'https://www.renrenche.com/cq/car/' + str(b)
                r.set(b,temp_car_page_url)
        except HTTPError as e:
            print(str(e))
            return(str(e))
        except ConnectionError as e:
            print(str(e))
            return(str(e))


    #print (upload_page_list())

class My_download_thread(threading.Thread):
    """docstring for My_upload_thread"""
    def __init__(self, name):
        threading.Thread.__init__(self)
        self._name= name 

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


def main():
    work_list = list()
    queue = JoinableQueue()



    m = My_upload_thread()
    print ("upload_page_list is over %s " %ctime())
    for url in m.upload_page_list(5):
        print(url)
        queue.put(url)

    for i in range(5):
        thread = m.upload_page_list(queue)
        threads.append(thread)
        t.start()
    queue.join()
    for w in work_list:
        w.terminate()
    print ("upload_page_list is over %s " %ctime())





    #print ("RenRencha Is over  %s" %ctime())

if __name__ =="__main__":

    main()
    print("Elapsed Time: %s" % ctime())  