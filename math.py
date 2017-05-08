#coding:gbk
import math
import requests
import redis
import re
from bs4 import BeautifulSoup

r = redis.StrictRedis(host='127.0.0.1',port=6379,db=0)
def download():
    redis_download_url = r.keys("*")
    for a in redis_download_url:
        redis_download_url_temp = r.get(a)
        c = requests.get(redis_download_url_temp)
        re_car_name = re.compile('<title>(.*)</title>',re.S)
        car_name = re.findall(re_car_name, c.text)

        re_car_money = re.compile(r'<p class="price detail-title-right-tagP">￥(.*)万</p>')
        car_money = re.findall(re_car_money, c.text)
        #print (c.url)
        print(car_name)
        print(car_money)
print(download())