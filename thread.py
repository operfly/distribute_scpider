# -*- codeing: utf-8 -*-
import requests
from requests.exceptions import HTTPError, ConnectionError
#from bs4 import BeautifulSoup, NavigableString
import queue
import threading
import time


class AyouBlog():
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
        }
        self.s = requests.session()

    def get_page_url(self):
        urls_set = set()
        url = "http://blog.csdn.net/u013055678?viewmode=contents"
        try:
            html = self.s.get(url, headers=self.headers)
        except HTTPError as e:
            print(str(e))
            return str(e)
        except ConnectionError as e:
            print(str(e))
            return str(e)
        try:
            soup = BeautifulSoup(html.content, "lxml")
            page_div = soup.find_all("span", {"class": "link_title"})
            for url in page_div:
                a_url = "http://blog.csdn.net" + url.find("a").attrs["href"]
                urls_set.add(a_url)
        except AttributeError as e:
            print(str(e))
            return str(e)
        return urls_set




class ThreadUrl(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.s = requests.session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
        }

    def run(self):
        while not self.queue.empty():
            host = self.queue.get()
            try:
                html = self.s.get(host, headers=self.headers)
            except HTTPError as e:
                print(str(e))
                return str(e)
            except ConnectionError as e:
                print(str(e))
                return str(e)
            try:
                soup = BeautifulSoup(html.content, "lxml")
                class_div = soup.find("span", {"class": "link_title"})
                print((class_div.text).strip())
            except AttributeError as e:
                print(str(e))
                return str(e)
            except NavigableString as e:
                print(str(e))
                return str(e)
            self.queue.task_done()


def main():
    queue = queue.queue()

    p = AyouBlog()
    for url in p.get_page_url():
        print(url)
        queue.put(url)

    for i in range(7):
        t = ThreadUrl(queue)
        t.setDaemon(True)
        t.start()

    queue.join()


if __name__ == "__main__":
    start = time.time()
    main()
    print("Elapsed Time: %s" % (time.time() - start))