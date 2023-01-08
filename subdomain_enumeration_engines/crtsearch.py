from multiprocessing import Process
import requests
from bs4 import BeautifulSoup
from utility.output_helper import *
import json


class CrtSearch(Process):
    def __init__(self, target_domain, queue=None):
        """
        Get subdomains from CrtSearch
        :param target_domain: Target domain to enumerate subdomain
        :param queue:
        """
        super().__init__()
        self.target_domain = target_domain
        self.base_url = 'https://crt.sh/'
        self.params = {'q': target_domain, 'output': 'json'}
        self.session = requests.session()
        self.queue = queue

    def run(self):
        print_info('Enumerating subdomains from CrtSearch')
        self.enumerate_subdomains()

    def enumerate_subdomains(self):
        """
        This method will return list of subdomains
        """
        subs_json = self.session.get(url=self.base_url, params=self.params).json()

        # soup = BeautifulSoup(resp.text, 'html.parser')
        subdomains = set()
        for subs in subs_json:
            sub = subs['name_value']
            subdomains.add(sub)

        self.queue.put(subdomains)

        print_info(f'Found {len(subdomains)} subdomains for {self.target_domain} from CrtSearch')
