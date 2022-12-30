import multiprocessing
import time
from colorama import Fore
from subdomain_enumeration_engines.virustotal import VirusTotal
from subdomain_enumeration_engines.dnsdumpster import DNSdumpster
from subdomain_enumeration_engines.crtsearch import CrtSearch
from utility.load_list_from_file import load_list_from_file
from utility.utils import extract_subs


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


if __name__ == '__main__':
    start_time = time.perf_counter()

    # this variable holds all enumerate subdomains. (may include duplicates)
    subdomains = []

    # this variable holds all enumerated subdomain and does not contain duplicates
    subdomains_set = set()

    # target to be enumerated
    target_domain = 'crowdstrike.com'

    queue = multiprocessing.Manager().Queue()

    # List of sources from where the subdomains will be enumerated
    enum_engines = [VirusTotal, CrtSearch, DNSdumpster]

    enum_engine_objects = [engine(target_domain, queue) for engine in enum_engines]

    for enum_engine_object in enum_engine_objects:
        enum_engine_object.start()

    for enum_engine_object in enum_engine_objects:
        enum_engine_object.join()

    subdomains_set = set(extract_subs(queue))

    # list of subdomain to be excluded
    exclusion_list = ['www.' + target_domain]

    for el in exclusion_list:
        subdomains_set.remove(el)

    write_list_to_file(subdomains_set, 'subdomains')

    print(f'{Fore.MAGENTA}Found {subdomains_set.__len__()} subdomains for {target_domain}')
    # =========================================================================================
    end_time = time.perf_counter()
    print('=================================================')
    print('End of Program')
    print('=================================================')
    print(f'Program completed in {end_time - start_time} seconds')
