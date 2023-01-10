import requests
from multiprocessing import Process
from utility.output_helper import *
from bs4 import BeautifulSoup

class RapidDNS(Process):
    def __init__(self, target_domain, queue=None):
        super().__init__()
        self.target_domain = target_domain
        self.queue = queue
        self.page_no = 1
        self.base_url = f'https://rapiddns.io/subdomain/{self.target_domain}?page={self.page_no}'
        self.session = requests.session()
        self.subdomains = set()

    def run(self):
        print_info(f'Enumerating subdomains from RapidDNS')
        self.enumerate_subdomains()

    def enumerate_subdomains(self):
        while(self.page_no):
            resp = self.session.get(url=self.base_url)
            soup = BeautifulSoup(resp.text, 'html.parser')

            if soup.find('td') != None:
                trs = soup.find('tbody').find_all_next('tr')
                for td in trs:
                    sub = td.find_next('td').get_text()
                    # print(sub)
                    self.subdomains.add(sub)
                                
                self.page_no += 1
                self.base_url = f'https://rapiddns.io/subdomain/{self.target_domain}?page={self.page_no}'                 

            else:
                self.queue.put(self.subdomains)
                break
        
