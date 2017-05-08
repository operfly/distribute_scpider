import time
import requests
import re
import redis
#import Queue
import threading



headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
r = redis.StrictRedis(host='127.0.0.1',port=6379,db=0)

#class Mytheard(threading.Thread):
#    """docstring for Mytheard"""
#    def __init__(self,t_name, Queue):
#        threading.Theard.__init__(self, name = t_name)
#        self.data = Queue
def upload_page_list():
    for a in range(1,51):
        url = 'https://www.renrenche.com/cq/ershouche/p' + str(a)
        page_url = requests.get(url,headers = headers,timeout = 30)
        recom = re.compile(r'data-car-id="(.*?)"',re.S)
        car_page_url = re.findall(recom,page_url.text)
        for b in car_page_url:
            temp_car_page_url = 'https://www.renrenche.com/cq/car/' + str(b)
            r.set(b,temp_car_page_url)
        print (r.get(b))
    return 0
print (upload_page_list())

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