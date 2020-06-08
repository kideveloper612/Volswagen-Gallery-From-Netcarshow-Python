import requests
import os
import csv
from bs4 import BeautifulSoup
import time
import sys
import re


def send_request(url, method='GET', payload={}):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0'\
        }
        res = requests.request(method=method, url=url, headers=headers, data=payload)
        if res.status_code == requests.codes.ok:
            return res
        return send_request(url=url, method=method, payload=payload)
    except ConnectionError:
        print(ConnectionError)
        time.sleep(5)
        return send_request(url=url, method=method, payload=payload)


def parse(html):
    return BeautifulSoup(html, 'html5lib')


def write_csv(lines, filename):
    with open(file=filename, encoding='utf8', mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(lines)


def main():
    land_soup = parse(send_request(url=base_url).text)
    lands = land_soup.find('ul', attrs={'class': 'lst'}).find_all('li')
    for land in lands:
        year = land.find(text=True, recursive=False).strip()
        if int(year) < 2015:
            sys.exit()
        span = land.find('span', attrs={'class': 'exMN'})
        span.decompose()
        model = land.a.text.strip()
        over = land.a['onmouseover'].replace("sT(event, ['", '').replace("'])", '').strip()
        line = [year, 'Volkswagen', model, over]
        print(line)


if __name__ == '__main__':
    print('----- Start -----')
    base_url = 'https://www.netcarshow.com/volkswagen/'
    main()
    print('---- The End ----')