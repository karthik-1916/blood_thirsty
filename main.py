#! /usr/bin/python
import multiprocessing
import time
from subdomain_enumeration_engines.virustotal import VirusTotal
from subdomain_enumeration_engines.dnsdumpster import DNSdumpster
from subdomain_enumeration_engines.crtsearch import CrtSearch
from subdomain_enumeration_engines.rapiddns import RapidDNS
from utility.utils import *
from utility.output_helper import *

args = setup_arguments()

if __name__ == '__main__':

    start_time = time.perf_counter()

    # target to be enumerated
    target_domain = args.domain

    print_info(f'Domain Set -----> {target_domain}\n', silent=args.silent)

    # this variable holds all enumerated subdomain and does not contain duplicates
    subdomains_set = set()

    queue = multiprocessing.Manager().Queue()

    # List of sources from where the subdomains will be enumerated
    enum_engines = [VirusTotal, CrtSearch, DNSdumpster, RapidDNS]

    enum_engine_objects = [engine(target_domain, args, queue) for engine in enum_engines]

    # run processes
    for enum_engine_object in enum_engine_objects:
        enum_engine_object.start()

    for enum_engine_object in enum_engine_objects:
        enum_engine_object.join()

    # holds list of unique subdomains of a given target domain
    subdomains_set = set(extract_subs(queue, args))

    # Write the final list of subdomains to a file
    write_list_to_file(subdomains_set, 'subdomains', args, os.getcwd())

    if not args.subs_only:
        response = make_http_req(subdomains_set, args=args)
        write_output(response, args=args)

    if args.silent:
        for sub in subdomains_set:
            print(sub)

    # =========================================================================================
    end_time = time.perf_counter()
    print_info('=================================================', silent=args.silent)
    print_info(f'Found {len(subdomains_set)} unique subdomains for {target_domain}', fore_color=Fore.BLACK,
               back_color=Back.GREEN, silent=args.silent)
    print_info(f'Program completed in {end_time - start_time} seconds', silent=args.silent)
    print_info('=================================================', silent=args.silent)
