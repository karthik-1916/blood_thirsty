from multiprocessing import Process
import json
import requests
from utility.output_helper import *


class VirusTotal(Process):
    def __init__(self, target_domain, queue):
        super().__init__()
        self.target_domain = target_domain
        self.base_url = ''
        self.api_url = 'https://www.virustotal.com/vtapi/v2/domain/report'
        self.api_key = '73d8feaa3cae67ac594141b2570966063efb2f47c9fb6592accf177bea6456ba'
        self.params = {'apikey': self.api_key, 'domain': self.target_domain}
        self.session = requests.session()
        self.queue = queue

    def run(self):
        print_info(f'Enumerating subdomains from VirusTotal')
        self.enumerate_subdomains()

    def enumerate_subdomains(self):
        resp = json.loads(self.session.get(url=self.api_url, params=self.params).text)
        subdomains = resp['subdomains']

        self.queue.put(subdomains)

        # print(f'{Fore.CYAN}Found {len(resp["subdomains"])} subdomains for {self.target_domain} from VirusTotal')
        print_info(f'Found {len(subdomains)} subdomains for {self.target_domain} from VirusTotal')
