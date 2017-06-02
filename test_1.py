import requests
import redis
import re
import time
import random
import threading
import elasticsearch
from queue import Queue
from requests.exceptions import HTTPError, ConnectionError

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
r = redis.StrictRedis(host='192.168.1.157', port=6379, db=0)
# es = Elasticsearch("192.168.1.157:9200")
queue = Queue()
ticket = 50 


class ThreadUrl(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.thread_name = name

    def run(self):
        global ticket

        while True:
            elem = random.randrange(10)
            queue.put(elem)

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
                print("线程%s抢到了票！还有%d剩余。" % (self.thread_name, ticket))
                

            else:
                break


def main():
    for i in range(10):
        p = ThreadUrl(i)
        p.start()

if __name__ == '__main__':
    main()
