import threading

import requests
from threading import Thread

lock = threading.Lock()


def extract_subs(queue):
    subdomains = []
    for q in range(queue.qsize()):
        subs = queue.get()
        for sub in subs:
            if '*' not in sub:
                if 'crowdstrike' in sub:
                    subdomains.append(sub)

    return subdomains


def load_list_from_file(filename):
    if '.txt' not in filename:
        filename += '.txt'
    file_obj = open(filename, 'r')
    data = file_obj.read().split('\n')
    file_obj.close()
    return data


def write_list_to_file(list_of_items, filename):
    """
    this funtion will write the list of subdomains enumerated to a file
    :param list_of_items: list of items to be written to file
    :param filename: name of the file
    """
    if '.txt' not in filename:
        filename += '.txt'
    print(f'Writing list to file ----->{filename}')
    file = open(filename, 'w')
    for item in list_of_items:
        file.write(item + '\n')
    file.close()


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
