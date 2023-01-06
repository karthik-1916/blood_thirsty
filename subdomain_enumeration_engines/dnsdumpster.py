from multiprocessing import Process
import requests
from colorama import Fore
from bs4 import BeautifulSoup
from utility.output_helper import *


class DNSdumpster(Process):

    def __init__(self, target_domain, queue=None):
        """
        Get subdomains from DNSdumpster
        :param target_domain: Target domain to enumerate subdomain
        :param queue:
        """
        super().__init__()
        self.target_domain = target_domain
        self.base_url = 'https://dnsdumpster.com/'
        self.session = requests.session()
        self.header = {'Referer': 'https://dnsdumpster.com/'}
        self.queue = queue

    def run(self):
        print_info(f'Enumerating subdomains from DNSdumpster')
        self.enumerate_subdomains()

    def enumerate_subdomains(self):
        """
        This method will return list of subdomains
        """
        cookies = self.get_cookies()
        data = self.get_data(cookies)
        resp = self.session.post(url=self.base_url, data=data, headers=self.header)
        resp_text = resp.text
        soup = BeautifulSoup(resp_text, 'html.parser')
        trs = soup.find_all('table')[3].find_all_next('tr')
        subdomains = []
        for tr in trs:
            # print(td.get_text())
            # print(tr.find_next('td').get_text())
            subdomains.append(tr.find_next('td').get_text().split('\n')[0])

        # for sub in subdomains:
        #     print(sub)

        self.queue.put(subdomains)

        # print(f'{Fore.CYAN}Found {subdomains.__len__()} subdomains for {self.target_domain} from DNSdumpster')
        print_info(f'Found {len(subdomains)} subdomains for {self.target_domain} from DNSdumpster')

    def get_cookies(self):
        resp = self.session.get(self.base_url)
        cookies = str(resp.cookies)
        return cookies

    def get_data(self, cookies):
        csfrtoken = ''

        for ch in cookies.split('=')[1]:
            if ch == ' ':
                break
            csfrtoken += ch
        data = {'cookie': f'csrftoken={csfrtoken}', 'csrfmiddlewaretoken': csfrtoken, 'targetip': self.target_domain,
                'user': 'free'}

        return data
