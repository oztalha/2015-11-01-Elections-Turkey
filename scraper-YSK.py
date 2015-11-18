# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 11:14:40 2015

@author: Talha
"""

from splinter import Browser
import time

browser = Browser('firefox')
browser.visit("https://sonuc.ysk.gov.tr")

il    = 1
ilce  = 1
errors=[]

# re-run this loop after manually fixing the session-timeout issue,
# il and ilce values will be resumed autmatically from where they left
# because the exception is raised before/without them being updated/reset
while il < 86:
    iller = browser.find_by_id('j_id48:j_id49:j_id108:cmbSecimCevresi').first.find_by_tag('option')
    browser.select('j_id48:j_id49:j_id108:cmbSecimCevresi',iller[il].value)
    time.sleep(3) # ilcelerin yuklenmesini bekle
    ilce_len = len(browser.find_by_id("j_id48:j_id49:j_id120:cmbIlceSecimKurulu").first.find_by_tag('option'))
    while ilce < ilce_len:
        try:
            ilceler = browser.find_by_id("j_id48:j_id49:j_id120:cmbIlceSecimKurulu").first.find_by_tag('option')
            browser.select('j_id48:j_id49:j_id120:cmbIlceSecimKurulu',ilceler[ilce].value)
            time.sleep(3) #lutfen bekleyinizi bekle 
            browser.find_by_name('j_id48:j_id49:j_id192').first.click()
            time.sleep(4) #sorgulamasini bekle 
            browser.find_by_id("j_id48:tabloBilgileriPanel:j_id425").first.click()
            time.sleep(3) #kabul ediyorum mesajini bekle 
            browser.find_by_id("j_id1028:j_id1029:j_id1035").first.click()
            time.sleep(5) #excel dosyasini indirmesini bekle
            print('[OK]:',il,ilce)
            ilce += 1 #update ilce
        except:
            print('[ERROR]:',il,ilce)
            errors.append((il,ilce))
            if errors.count((il,ilce))>=3:
                raise #raise exception if the same ilce fails three times.
    il  += 1 #update il
    ilce = 1 #reset ilce
    


# verify that we downloaded all the files
il=1
ilceler = {} 
while il < 86:
    iller = browser.find_by_id('j_id48:j_id49:j_id108:cmbSecimCevresi').first.find_by_tag('option')
    bolge = iller[il].text
    browser.select('j_id48:j_id49:j_id108:cmbSecimCevresi',iller[il].value)
    time.sleep(4) # ilcelerin yuklenmesini bekle
    ilceler[bolge] = [i.text.strip() for i in browser.find_by_id("j_id48:j_id49:j_id120:cmbIlceSecimKurulu").first.find_by_tag('option')][1:]
    il += 1
 
import json   
with open('data/ilce-secim-kurullari.json','w',encoding='utf-8') as ilcef:
    json.dump(ilceler,ilcef,ensure_ascii=False)


from glob import glob
fs = glob('*.xls')
not_oneAndOnlyOne=[]
for k in ilceler.keys():
    starts = ['ssps-'+k+'-'+v+'-' for v in ilceler[k]]
    for s in starts:
        if 1 is not len([f for f in fs if f.startswith(s)]):
            not_oneAndOnlyOne.append(s)

# number of İlçe Seçim Kurulu == 1080
sum([len(v) for v in ilceler.values()])


# create a single csv file from all the xls files
import pandas as pd
dfs = [pd.read_excel(f,skiprows=0,header=1) for f in fs]
df = pd.concat(dfs)
df.to_csv('data/ysk.csv',index=False,encoding='utf8')
