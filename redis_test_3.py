import requests
import redis
import re
import time
import random
import threading
import elasticsearch
from datetime import datetime
from elasticsearch import Elasticsearch

from requests.exceptions import HTTPError, ConnectionError

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
r = redis.StrictRedis(host='192.168.1.157', port=6379, db=0)
es = Elasticsearch("192.168.1.157:9200")
ticket = 50 


class ThreadUrl(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.thread_name = name

    def run(self):
        global ticket

        while True:


            if ticket > 0:
                ticket -=1
                url = 'https://www.renrenche.com/cq/ershouche/p' + str(ticket)
                page_url = requests.get(url, headers=headers, timeout=30)
                recom = re.compile(r'data-car-id="(.*?)"', re.S)
                car_page_url = re.findall(recom, page_url.text)
                for b in car_page_url:

                    temp_car_page_url = 'https://www.renrenche.com/cq/car/' + \
                        str(b)
                    r.set(b, temp_car_page_url)
                print("线程%s找到了！还有%d页面剩余。" % (self.thread_name, ticket))
                

            else:
                break

class My_download_thread(threading.Thread):
    """docstring for download_car"""
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.thread_name = name

    def run(self):
        while  True:
            
            redis_download_url_number = r.dbsize()
            
            if redis_download_url_number >= 0:
                redis_download_url_number -=1
    
    
            
                redis_download_url = r.keys("*")
                for a in redis_download_url:
                    redis_download_url_temp = r.get(a)
                    r.delete(a)
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
                
                
                    
            else:    
                pass

        


def main():
    for i in range(10):
        p = ThreadUrl(i)
        p.start()

    for b in range(10):
        s = My_download_thread(b)
        s.start()

if __name__ == '__main__':
    main()
