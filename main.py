import multiprocessing
import time
from subdomain_enumeration_engines.virustotal import VirusTotal
from subdomain_enumeration_engines.dnsdumpster import DNSdumpster
from subdomain_enumeration_engines.crtsearch import CrtSearch
from utility.utils import *
from utility.output_helper import *

args = setup_arguments()

if __name__ == '__main__':

    start_time = time.perf_counter()

    # target to be enumerated
    target_domain = args.domain

    print_info(f'Domain Set -----> {target_domain}\n')

    # this variable holds all enumerate subdomains. (may include duplicates)
    subdomains = []

    # this variable holds all enumerated subdomain and does not contain duplicates
    subdomains_set = set()

    queue = multiprocessing.Manager().Queue()

    # List of sources from where the subdomains will be enumerated
    enum_engines = [VirusTotal, CrtSearch, DNSdumpster]

    enum_engine_objects = [engine(target_domain, queue) for engine in enum_engines]

    # run processes
    for enum_engine_object in enum_engine_objects:
        enum_engine_object.start()

    for enum_engine_object in enum_engine_objects:
        enum_engine_object.join()

    # holds list of unique subdomains of a given target domain
    subdomains_set = set(extract_subs(queue))

    # Write the final list of subdomains to a file
    write_list_to_file(subdomains_set, 'subdomains', os.getcwd())

    response = make_http_req(subdomains_set)

    write_output(response)

    # print(f'{Fore.MAGENTA}Found {subdomains_set.__len__()} subdomains for {target_domain}')
    print_info(f'Found {len(subdomains_set)} subdomains for {target_domain}', fore_color=Fore.WHITE,
               back_color=Back.GREEN)
    # =========================================================================================
    end_time = time.perf_counter()
    print_info('=================================================')
    print_info('End of Program')
    print_info(f'Program completed in {end_time - start_time} seconds')
    print_info('=================================================')
