import requests
import pandas as pd
from bs4 import BeautifulSoup
from unidecode import unidecode


#zaman scraper










def scrape_towns():
	cities = pd.read_csv('data/city_meta.csv',usecols=['il']).il #Cities w/ Turkish characters
	n = pd.DataFrame(columns=('city','town', 'AKP', 'CHP','MHP','HDP','others'))
	j = pd.DataFrame(columns=('city','town', 'AKP', 'CHP','MHP','HDP','others'))

	for c in cities:
		url = 'http://www.yenisafak.com/secim-2015-kasim/'+unidecode(c).lower()+'-ili-secim-sonuclari'
		resource = requests.get(url)
		soup = BeautifulSoup(resource.content.decode('utf-8','ignore'), "lxml")
		# kill all script, style, sub, sup and b elements
		for script in soup(["script", "style", "sup", "sub", "b"]):
			script.extract()    # rip it out 
		towns = soup.find_all(class_='data sub-data compare')
		for t in towns:
			info = t.find_all('span')
			nov1 = [c,info[0].text]
			jun7 = [c,info[0].text]
			for i in range(16,21): #Nov 1st results
				nov1.append(float(info[i].text.replace(',','.')))
			for i in range(23,28): #Jun 7th results
				jun7.append(float(info[i].text.replace(',','.')))
			n.loc[len(n)]=nov1
			j.loc[len(j)]=jun7

	j.to_csv('data/jun_towns.csv',index=False,encoding='utf-8')
	n.to_csv('data/nov_towns.csv',index=False,encoding='utf-8')



def scrape_cities():
	resource = requests.get('http://www.yenisafak.com/secim-2015-kasim/secim-sonuclari')
	soup = BeautifulSoup(resource.content.decode('utf-8','ignore'),'html.parser')
	# kill all script, style, sub, sup and b elements
	for script in soup(["script", "style", "sup", "sub", "b"]):
		script.extract()    # rip out some visualization elements
	cities = soup.find_all(class_='data  compare')[3:] #81 city results
	columns = ['city','AKP', 'CHP','MHP','HDP','others','turnout','registered','voted','valid']
	nov = pd.DataFrame(columns=columns); nov.name = 'nov'
	jun = pd.DataFrame(columns=columns); jun.name = 'jun'

	for city_info in cities:
		info = city_info.find_all('span')
		city = info[0].text
		nov1 = [float(info[i].text.replace(',','.')) for i in range(16,21)] #Nov 1st results
		jun7 = [float(info[i].text.replace(',','.')) for i in range(23,28)] #Jun 7th results
		url = 'http://www.yenisafak.com/secim-2015-kasim/'+unidecode(city).lower()+'-ili-secim-sonuclari'
		resource = requests.get(url)
		soup = BeautifulSoup(resource.content.decode('utf-8','ignore'), "lxml")
		# kill all script, style, sub, sup and b elements
		for script in soup(["script", "style", "sup", "sub", "b"]):
			script.extract()    # rip it out 
		turnout = [t.text for t in soup.find_all(class_='graph-3 ')[1].find_all('span')]
		nov1 += [float(turnout[1].replace(',','.'))] + [int(t.replace('.','')) for t in turnout[5::4]]
		jun7 += [float(turnout[3].replace(',','.'))] + [int(t.replace('.','')) for t in turnout[7::4]]

		nov.loc[len(nov)]=[city] + nov1 #add city name and insert row to the dataframe
		jun.loc[len(jun)]=[city] + jun7 #add city name and insert row to the dataframe

	cities = pd.read_csv('data/city_meta.csv',usecols=['il','bolge'])
	jun['region'] = cities['bolge']
	nov['region'] = cities['bolge']
	nov.to_csv('data/nov.csv',index=False,encoding='utf-8')
	jun.to_csv('data/jun.csv',index=False,encoding='utf-8')



def create_json(df):
    """create geojson files annotated with election results"""
    f = json.load(open('turkey.geojson',encoding='utf-8'))
    parties = ['AKP', 'CHP','MHP','HDP','others']
    for ft in f['features']:
        city = ft['properties']['name']
        shares = str(df[df.city==city][parties].values).strip('[]').split()
        p = '<b>'+city+'</b><br>'
        for i in range(len(parties)):
            p += parties[i]+': '+shares[i]+'%<br>'
        p = p[:-4]
        ft['properties'] = {'name':city,'popupContent':p}

    with open('tr_'+df.name+'.geojson', 'w',encoding='utf-8') as outfile:
        json.dump(f,outfile,ensure_ascii=False)

jun.name='jun'
nov.name='nov'
#create_json(nov)
#create_json(jun)


