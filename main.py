import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import Request, urlopen

# driver = webdriver.Chrome('/usr/local/bin/chromedriver')  # Optional argument, if not specified will search path.

names = []
prices = []
category = []

# driver.get("https://www.paknsaveonline.co.nz/category/personal-care")
req = Request("https://www.paknsaveonline.co.nz/category/personal-care", headers={'User-Agent': 'Mozilla/5.0'})
content = urlopen(req)
soup = BeautifulSoup(content,features="lxml")
cnt = 1
for a in soup.findAll('div',attrs={'class':'fs-product-card'}):
    
    names.append(a.find('h3',attrs={'class':"u-p2"}).text)

print(names)