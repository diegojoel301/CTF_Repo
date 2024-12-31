#!/usr/bin/python
"""
Robots.py by Frank Wizard
Script to request robots.txt content and search content for valid urls
"""

import argparse
import sys
import requests
import colorama 
from colorama import Fore, Style

# CLI Arguments
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('-u', '--url', help="Input url to check, http://example.com", required=True)
parser.add_argument('-o', '--output', help="Output file name")
parser.add_argument('-r', dest='recursive', action='store_true', help="check recursive robot urls")
args = parser.parse_args()

def print_status(status, color):
    print('Status: ' + color + str(status) + Fore.WHITE)

def print_results(url):
    try:
        res = requests.get(url, timeout=5)
    except requests.exceptions.Timeout as e:
        print(Fore.YELLOW + 'Timeout after 5s. Can not reach target url check again...' + Fore.WHITE)
    else:
        status = res.status_code
        print(url)
        if status >= 200 and status < 300:
            print_status(status, Fore.GREEN)
        elif status >= 400 and status < 600:
            print_status(status, Fore.RED)
        else:
            print_status(status, Fore.YELLOW)

def request_findings(text, url):
    for x in text:
        if '*' not in x and len(x) > 0 and not x.startswith('#') and 'User-agent' not in x:
            x = x.replace('Disallow:', '').replace(' ', '').replace('Allow:', '')
            if x.startswith('/'):
                print_results(url + x)
            else:
                print_results(url + '/' + x)

def get_robot_txt():
    if args.output:
        sys.stdout = open(args.output, 'w')
    if args.url:
        url = args.url
        if 'http' not in url:
            url = 'http://' + url
        try:
            res = requests.get(url + '/robots.txt', timeout=5)
        except requests.exceptions.Timeout as e:
            print(Fore.YELLOW + 'Timeout after 5s. Can not reach target url check again...' + Fore.WHITE)
        else:
            if res.ok == True:
                content = res.content
                print(res.text)
                if args.recursive:
                    text = res.text.split('\n')
                    request_findings(text, url)
            else:
                print(Fore.RED + 'not found ' + str(res.status_code) + Fore.WHITE)
    if args.output:
        sys.stdout.close()
        
get_robot_txt()
