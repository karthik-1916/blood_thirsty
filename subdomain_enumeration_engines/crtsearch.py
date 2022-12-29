from multiprocessing import Process
import requests
from colorama import Fore
from bs4 import BeautifulSoup


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
        self.params = {'q': target_domain}
        self.session = requests.session()
        self.queue = queue

    def run(self):
        print(f'Enumerating subdomains from CrtSearch')
        self.enumerate_subdomains()

    def enumerate_subdomains(self):
        """
        This method will return list of subdomains
        """
        resp = self.session.get(url=self.base_url, params=self.params)
        soup = BeautifulSoup(resp.text, 'html.parser')
        subdomain_length = len(soup.find_all('table')[1].find_all_next('tr'))
        subdomains = []
        for i in range(1, subdomain_length):
            sub = soup.find_all('table')[1].find_all_next('tr')[i].find_all_next('td')[4].get_text()
            subdomains.append(sub)

        # for sub in subdomains:
        #     print(Fore.GREEN + sub)

        self.queue.put(subdomains)

        print(f'{Fore.CYAN}Found {subdomains.__len__()} subdomains for {self.target_domain} from CrtSearch')
