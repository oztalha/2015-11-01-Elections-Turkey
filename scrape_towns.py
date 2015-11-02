import requests
import pandas as pd
from bs4 import BeautifulSoup

orj = pd.read_csv('data/city_meta.csv',usecols=['il']).il #Cities w/ Turkish characters
cities = pd.read_csv('data/TR_11_15.csv',usecols=['PROVINCE']).PROVINCE.apply(str.lower)
city_dict = dict(zip(cities, orj))

n = pd.DataFrame(columns=('city','town', 'AKP', 'CHP','MHP','HDP','others'))
j = pd.DataFrame(columns=('city','town', 'AKP', 'CHP','MHP','HDP','others'))

for c in cities:
    url = 'http://www.yenisafak.com/secim-2015-kasim/'+c+'-ili-secim-sonuclari'
    resource = requests.get(url)
    soup = BeautifulSoup(resource.content.decode('utf-8','ignore'), "lxml")
    # kill all script, style, sub, sup and b elements
    for script in soup(["script", "style", "sup", "sub", "b"]):
        script.extract()    # rip it out 
    towns = soup.find_all(class_='data sub-data compare')
    for t in towns:
        info = t.find_all('span')
        nov1 = [city_dict[c],info[0].text]
        jun7 = [city_dict[c],info[0].text]
        for i in range(16,21): #Nov 1st results
            nov1.append(float(info[i].text.replace(',','.')))
        for i in range(23,28): #Jun 7th results
            jun7.append(float(info[i].text.replace(',','.')))
        n.loc[len(n)]=nov1
        j.loc[len(j)]=jun7

j.to_csv('data/jun_towns.csv',index=False,encoding='utf-8')
n.to_csv('data/nov_towns.csv',index=False,encoding='utf-8')