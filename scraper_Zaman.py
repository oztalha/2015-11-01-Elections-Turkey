import requests
import pandas as pd
from bs4 import BeautifulSoup
from collections import defaultdict
import io
import json

#zaman scraper
urls = pd.read_csv('data/zaman_urls.csv')
us = dict(zip(urls.ix[:,1],urls.ix[:,0]))
oy = [defaultdict(dict)]*3

for city,url in us.items():
    resource = requests.get(url)
    soup = BeautifulSoup(resource.content.decode('utf-8','ignore'), "lxml")
    parties = soup.select('.compare-list')[0].find_all(class_='clearfix')
    for o in oy:
        o[city] = defaultdict(dict)
    for p in parties:
        name = p.find(class_='compare-party-name').text.strip()
        rates = [float(r.text.replace('%','').replace(',','.')) for r in p.findAll(class_='compare-percentage')]
        votes = [int(v.text.replace('.','')) for v in p.findAll(class_='compare-vote')]
        for i in range(3):
            oy[i][city][name]['rate'] = rates[i]
            oy[i][city][name]['vote'] = votes[i]

with io.open('data/zaman_oy.json', 'w', encoding='utf8') as json_file:
    json.dump(oy,json_file,ensure_ascii=False)

