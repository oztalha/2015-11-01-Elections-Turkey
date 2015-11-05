# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 12:52:34 2015

@author: Talha
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time


driver = webdriver.Firefox()
driver.get('https://t3.oyveotesi.org/#/sonuc')
wait = WebDriverWait(driver,10)
dfs = []
errors = []
# il seciniz okunu tikla
wait.until(lambda driver: driver.find_element_by_css_selector('.col-md-4 > div:nth-child(1) > div:nth-child(2) > span:nth-child(2)')).click()
#iller listesini al
iller = wait.until(lambda driver: driver.find_element_by_css_selector('.list-group')).text.split('\n')
for i,il in enumerate(iller,1):
    print(il,' - - - - - - - -')
    #i'yinci ili tikla
    if i == 1:
        wait.until(lambda driver: driver.find_element_by_css_selector('a.list-group-item:nth-child('+str(i)+')')).click()
    else:
        e = wait.until(lambda driver: driver.find_element_by_css_selector('.col-md-4 > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)'))
        e.clear()
        e.send_keys(il+'\n')
    #ilce seciniz okunu tikla
    wait.until(lambda driver: driver.find_element_by_css_selector('.col-md-4 > div:nth-child(3) > div:nth-child(2) > span:nth-child(2) > span:nth-child(1)')).click()
    #ilceler listesini al
    ilceler = wait.until(lambda driver: driver.find_element_by_css_selector('.list-group')).text.split('\n')
    for j,ilce in enumerate(ilceler,1):
        print(ilce)
        #j'nci ilceyi tikla
        if j == 1:
            wait.until(lambda driver: driver.find_element_by_css_selector('a.list-group-item:nth-child('+str(j)+')')).click()
        else:
            e = wait.until(lambda driver: driver.find_element_by_css_selector('.col-md-4 > div:nth-child(3) > div:nth-child(2) > input:nth-child(1)'))
            e.clear()
            e.send_keys(ilce+'\n')
        #sandik numarasi seciniz okunu tikla
        wait.until(lambda driver: driver.find_element_by_css_selector('div.ng-isolate-scope:nth-child(5) > div:nth-child(2) > span:nth-child(2) > span:nth-child(1)')).click()
        #sandik listesini al
        sandiklar = wait.until(lambda driver: driver.find_element_by_css_selector('.list-group')).text.split('\n')
        for k,sandik in enumerate(sandiklar,1):
            #k'nci sandigi tikla
            if k ==1:
                wait.until(lambda driver: driver.find_element_by_css_selector('a.list-group-item:nth-child('+str(k)+')')).click()
            else:
                e = wait.until(lambda driver: driver.find_element_by_css_selector('div.ng-isolate-scope:nth-child(5) > div:nth-child(2) > input:nth-child(1)'))
                e.clear()
                e.send_keys(sandik+'\n') 
            #sonuclari sorgula
            wait.until(lambda driver: driver.find_element_by_css_selector('.btn-lg')).click()
            try:
                df = pd.read_html(wait.until(lambda driver: driver.find_element_by_css_selector('.table')).get_attribute('outerHTML'))[0]
                df = df.T
                df['sandik'] = sandik
                df['ilce'] = ilce
                df['il'] = il
                dfs.append(df)
            except:
                errors.append([il,ilce,sandik])
                pass
