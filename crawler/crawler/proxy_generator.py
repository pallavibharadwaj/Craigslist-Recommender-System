#!/usr/bin/python3

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import os

# file containing the proxy list
FILE = "spiders/proxies.txt"
cmd = "rm -f %s" %FILE
os.system(cmd)

ua = 'Mozilla/5.0 (X11; Linux x86_64)'

def main():
    # crawl latest elite proxies from this website
    proxies_req = Request('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent', ua)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')

    soup = BeautifulSoup(proxies_doc, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')

    # Save proxies in a text file
    for row in proxies_table.tbody.find_all('tr'):
        # ip:port
        proxy = row.find_all('td')[0].string+":"+row.find_all('td')[1].string
        with open(FILE, 'a') as f:
            f.write(proxy+"\n")

if __name__ == '__main__':
  main()
