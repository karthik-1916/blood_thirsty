import threading

import requests
import time
from threading import Thread
from utility.load_list_from_file import load_list_from_file

lock = threading.Lock()


def make_http_req(urls):
    response = []
    session = requests.session()
    threads = []
    for url in urls:
        url = 'https://' + url
        t = Thread(target=req, args=(url, response))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def req(url, response):
    try:
        resp = requests.get(url=url, timeout=3)

        response.append({'Status Code': resp.status_code, 'Response Text': resp.text})
        lock.acquire()
        print(f'---> {url} -----> {resp.status_code}')
        lock.release()
    except:
        lock.acquire()
        print(f'---> {url} -----> Unresponsive')
        lock.release()
        response.append({'Unresponsive': url})
