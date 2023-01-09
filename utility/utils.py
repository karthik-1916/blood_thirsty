import argparse
import json
import os.path
import threading

import requests
from threading import Thread
from utility.output_helper import *

lock = threading.Lock()


def extract_subs(queue):
    print_info('Removing duplicate subdomains')
    subdomains = []
    for q in range(queue.qsize()):
        subs = queue.get()
        for sub in subs:
            if '*' not in sub:
                if 'www' not in sub:
                    subdomains.append(sub)

    return subdomains


def load_list_from_file(filename):
    """
    create list from file
    :param filename: file from where list to be created
    :return: list of data
    """
    if '.txt' not in filename:
        filename += '.txt'
    file_obj = open(filename, 'r')
    data = file_obj.read().split('\n')
    file_obj.close()
    return data


def write_list_to_file(list_of_items, filename, path=None):
    """
    this function will write list of subdomains enumerated to a file
    :param list_of_items: list of items to be written to file
    :param filename: name of the file
    """
    if '.txt' not in filename:
        filename += '.txt'
    filepath = ''
    if path is not None:
        filepath = os.path.join(path, filename)
        if not os.path.exists(path):
            os.mkdir(path)

    print_info(f'Writing list to file -----> {filepath}')
    file = open(filepath, 'w')
    for item in list_of_items:
        file.write(item + '\n')
    file.close()


def write_output_to_file(path, filename, contents, filetype='txt'):
    """
    This function will write contents to a file
    :param path: path where the file to be created
    :param filename: name of the file
    :param contents: contents to be written to file
    :param filetype: type of file to be written
    """
    if '.txt' in filename:
        filename = filename.split('.')[0]
    filename += '.' + filetype
    filepath = ''
    if path is not None:
        filepath = os.path.join(path, filename)
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

    file = open(filepath, 'w', encoding='utf-8')

    file.writelines(contents)
    file.close()


def make_http_req(urls):
    print_info('Preparing to make http/https request to subdomains')
    response = []
    threads = []
    for url in urls:
        url = 'https://' + url
        t = Thread(target=req, args=(url, response))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print_info(f'Completed making http/https request to all subdomains')

    return response


def req(url, response):
    try:
        resp = requests.get(url=url, timeout=3)

        response.append(
            {'Link': url, 'Status Code': resp.status_code, 'Response Text': resp.text, 'Request Header': resp.headers})

    except:

        response.append({'Unresponsive': url})


def write_output(response):
    print_info(f'Writing request output to file')
    unresponsive_list = []
    responsive_list = []

    # this for loop will create a list of unresponsive and responsive subdomains
    # later this list will be used to write list to file
    for resp in response:
        if 'Unresponsive' in resp.keys():
            unresponsive_list.append(resp['Unresponsive'])
        else:
            resp_link = resp['Link'] + ' -----> ' + str(resp['Status Code'])
            responsive_list.append(resp_link)

    # These two thread will write list of unresponsive and responsive subdomains to a file
    unresp_subs_thread = Thread(target=write_list_to_file,
                                args=(unresponsive_list, 'unresponsive_subs.txt', os.getcwd() + '\\unresponsive'))
    resp_subs_thread = Thread(target=write_list_to_file,
                              args=(responsive_list, 'responsive_subs.txt', os.getcwd() + '\\responsive'))

    # this for loop will write response data to a file
    resp_data_text_thread = []
    req_header_thread = []
    path = os.path.join(os.getcwd(), 'responsive')
    for resp in response:
        if "Unresponsive" not in resp.keys():
            t1 = Thread(target=write_output_to_file,
                        args=(path, resp["Link"].strip("https://"), resp['Response Text'], 'body'))
            t2 = Thread(target=write_output_to_file,
                        args=(path, resp["Link"].strip("https://"),
                              json.dumps(dict(resp['Request Header']), indent=4, separators=(",", ":")), 'json'))
            resp_data_text_thread.append(t1)
            req_header_thread.append(t2)
            t1.start()
            t2.start()

    unresp_subs_thread.start()
    resp_subs_thread.start()
    unresp_subs_thread.join()
    resp_subs_thread.join()

    for t in resp_data_text_thread:
        t.join()

    for t in req_header_thread:
        t.join()


def setup_arguments():
    program_description = 'Adding Description'

    parser = argparse.ArgumentParser(description=program_description)
    parser.add_argument('-d', '--domain', help='domain name for which subdomains to be enumerated', required=True)
    return parser.parse_args()
