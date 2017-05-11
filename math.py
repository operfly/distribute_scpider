# -*- coding: utf-8 -*-

#  import math
import requests
import redis
import re
from pymongo import MongoClient
import elasticsearch
#from bs4 import BeautifulSoup
from datetime import datetime
from elasticsearch import Elasticsearch

r = redis.StrictRedis(host='192.168.1.135',port=6379,db=0)
es = Elasticsearch("192.168.1.157:9200")

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
print (download())