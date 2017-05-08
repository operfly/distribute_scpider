# -*- coding: utf-8 -*-
#  import math
import requests
import redis
import re
#from bs4 import BeautifulSoup

r = redis.StrictRedis(host='192.168.1.135',port=6379,db=0)
def download():
    redis_download_url = r.keys("*")
    for a in redis_download_url:
        redis_download_url_temp = r.get(a)
        c = requests.get(redis_download_url_temp)
        b = c.decode('utf-8','ignore')
        print (b)
print(download())
