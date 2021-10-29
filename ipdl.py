#!/usr/bin/env python
"""
IPD_LOOKUP TOOL
Utilizes PyDNSBL to determine if an IP or domain is malicious or not
"""

import pydnsbl
from pydnsbl.providers import BASE_PROVIDERS
from more_providers import more_providers
from pull_providers import pull_providers

from time import sleep

__author__ = "Kaleb Sego"
__copyright__ = "Copyright 2021"
__license__ = "GPLv3"
__version__ = "1.1.0"
__maintainer__ = "Kaleb Sego"
__contact__ = "https://github.com/AlbusNoir"


# handle additional providers more flexibly and assign ip_checker accordingly
if len(more_providers) == 0:
    providers = BASE_PROVIDERS
    ip_checker = pydnsbl.DNSBLIpChecker(providers = providers)

    print('Additional providers not found. Using base provider list...')
    sleep(1)  # not needed I just like seeing the pause

elif len(more_providers) > 0:
    providers = BASE_PROVIDERS + more_providers
    ip_checker = pydnsbl.DNSBLIpChecker(providers = providers)

    print('Additional providers found. Adding to provider list...')
    sleep(1)  # not needed I just like seeing the pause


domain_checker = pydnsbl.DNSBLDomainChecker()


def main():
    """Main driver function"""
    print('''
     _____ ______ _____   _       
    (_____|_____ (____ \ | |      
       _   _____) )   \ \| |      
      | | |  ____/ |   | | |      
     _| |_| |    | |__/ /| |_____ 
    (_____)_|    |_____/ |_______)
    -------------------------------
    IP & Domain Lookup
    1) Run verbose
    2) Run non-verbose
    3) Pull additional providers
    4) Help
    5) Quit
    ''')

    while True:
        i = input('> ')

        if i == '1':
            verbose()
            break
        elif i == '2':
            non_verbose()
            break
        elif i == '3':
            print('''WARNING: 
            running pull_providers will pull down approx 300 providers into the available providers.
            This may result in a significant increase in the amount of time it takes to run queries.
            This is provided as an optional function and is NOT required to perform queries.''')
            proceed = input('\nDo you wish to proceed? Y/n\n > ')

            if proceed.lower() == 'y':
                pull_providers()
                print('Providers list has been updated. Please re-run IPDL to have make these available to use in '
                      'queries')
                break
            elif proceed.lower() == 'n':
                continue
            else:
                print('Handling unexpected input as a "No"')
                break
        elif i == '4':
            print('''
            IPDLookup is a tool that accepts IP addresses and domains and runs them through various databases to 
            determine if they are malicious or not.
            
            "Malicious" is determined by the existence of an IP in a database. Just because an IP or domain is in a 
            database does not mean it is inherently harmful. Further investigation is still needed.
            
            IPDLookup runs in two modes: verbose and non-verbose.
            Verbose will output the following: blacklist(T/F), which blacklist the IP/domain is in, the category the 
            IP/domain was assigned to, and a list of providers(databases) the IP/domain was scanned through
            
            Non-verbose will output the following: blacklist(T/F)
            
            You do NOT need to run pull_providers to run queries using IPDL. Pull_providers is an added feature to 
            extend the amount of providers you run queries against. It does not add any kind of extra to IPDL, 
            just allows queries to hit more providers to check blacklists. If you do not want to use this added 
            feature, you are free not to.
            ''')
        elif i == '4':
            break
        else:
            print(f'Input Error: {i} not an option')


def verbose():
    """If verbose mode is selected"""
    print('''
    MODE: VERBOSE
    1) IP Lookup
    2) Domain Lookup
    3) Quit     
   ''')

    while True:
        i = input('> ')

        if i == '1':
            verbose_lookup_ip()
            break
        elif i == '2':
            verbose_lookup_domain()
            break
        elif i == '3':
            break
        else:
            print(f'Input Error: {i} not an option')


def non_verbose():
    """Non-verbose"""
    print('''
    MODE: FAST
    1) IP Lookup
    2) Domain Lookup
    3) Quit     
   ''')

    while True:
        i = input('> ')

        if i == '1':
            non_verbose_lookup_ip()
            break
        elif i == '2':
            non_verbose_lookup_domain()
            break
        elif i == '3':
            break
        else:
            print(f'Input Error: {i} not an option')


def verbose_lookup_ip():
    """Perform ip lookup for verbose mode"""
    ip = input('Enter IP address(s), separated by a comma, no spaces: ')

    ip_list = ip.split(",")

    for ip in ip_list:

        result = ip_checker.check(ip)
        caught_by = result.detected_by if result.blacklisted else 'N/A'
        bl = result.blacklisted
        cat = result.categories if result.blacklisted else 'N/A'
        prov = result.providers

        print(f'''RESULTS of {ip}:
        Blacklisted: {bl}
        Detected By: {caught_by}
        Categories: {cat}
        Scanned By: {prov}
        ''')


def verbose_lookup_domain():
    """Perform domain lookup for verbose mode"""
    domain = input('Enter domain(s), separated by a comma, no spaces: ')

    domain_list = domain.split(",")

    for domain in domain_list:

        result = domain_checker.check(domain)
        caught_by = result.detected_by if result.blacklisted else 'N/A'
        bl = result.blacklisted
        cat = result.categories if result.blacklisted else 'N/A'
        prov = result.providers

        print(f'''RESULTS of {domain}:
                Blacklisted: {bl}
                Detected By: {caught_by}
                Categories: {cat}
                Scanned By: {prov}
        ''')


def non_verbose_lookup_ip():
    """Perform ip lookup for non-verbose mode"""
    ip = input('Enter IP address(s), separated by a comma, no spaces: ')

    ip_list = ip.split(",")

    for ip in ip_list:

        result = ip_checker.check(ip)
        bl = result.blacklisted

        print(f'''RESULTS of {ip}:
        Blacklisted: {bl}
        
        For more information, run verbose mode
        ''')


def non_verbose_lookup_domain():
    """Perform domain lookup for non-verbose mode"""
    domain = input('Enter domain(s), separated by a comma, no spaces: ')

    domain_list = domain.split(",")

    for domain in domain_list:

        result = domain_checker.check(domain)
        bl = result.blacklisted

        print(f'''RESULTS of {domain}:
        Blacklisted: {bl}
        
        For more information, run verbose mode
        ''')


if __name__ == '__main__':
    main()
