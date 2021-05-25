#!/usr/bin/env python3

import socket
import shodan
import argparse

parser = argparse.ArgumentParser()
parse_args = parser.add_argument("key", help="Shodan API key")
args = parser.parse_args()

APIKey = args.key

api = shodan.Shodan(APIKey, proxies=None)

try:
    result = api.search('117.239.178.35')
    print(result['matches'])
    print(result['total'])
    # print(result['data'])
    for i in result['matches']:
        print(i['ip_str'])
except shodan.APIError as e:
    print(e)
