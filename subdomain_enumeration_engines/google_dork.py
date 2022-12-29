from multiprocessing import Process
import requests
from bs4 import BeautifulSoup


class GoogleDork(Process):
    def __init__(self, target_domain):
        super().__init__()
        self.target_domain = target_domain
        self.base_url = 'https://www.google.com/search?q=site:*.' + self.target_domain + '+-site:www.' + self.target_domain + '&start=0'
        self.session = requests.session()

    def run(self):
        self.enumerate_subdomains()

    def enumerate_subdomains(self):
        resp = self.session.get(url=self.base_url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        print(resp.text)
