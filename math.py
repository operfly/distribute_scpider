#coding:gbk
import math
import requests
import redis
import re

r = redis.StrictRedis(host='192.168.1.135',port=6379,db=0)
def download():
    redis_download_url = r.keys("*")
    for a in redis_download_url:
        redis_download_url_temp = r.get(str(a))
        c = requests.get(redis_download_url_temp)
        re_car_name = re.compile('<title>.*</title>')
        car_name = re.findall(re_car_name, c.text)

        re_car_money = re.compile('<span class="dialog-price">.*</span>',re.S)
        car_money = re.findall(re_car_money, c.text)
        print car_name
        print car_money
print download()