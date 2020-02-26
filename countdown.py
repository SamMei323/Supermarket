import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import ast
import os
import time
from selenium import webdriver
t0 = time.time()
###########

# req = Request("https://shop.countdown.co.nz/shop/browse/bakery?page=1", headers={'User-Agent': 'Mozilla/5.0'})
# content = urlopen(req)

productName = []
unitPrice = []
category = []
image = []
pricingUnit= []
productId = []
quantity = []


driver = webdriver.Chrome("/usr/local/bin/chromedriver")
driver.get("https://shop.countdown.co.nz/shop/browse/bakery?page=1")
content = driver.page_source

soup = BeautifulSoup(content,features="lxml")

productGrid = soup.find('product-grid-element',id='grid-0')
# print(productGrid)
products = productGrid['products'].replace("null",'''"null"''').replace('false','0').replace('true','0')
products = eval(products)
for product in products:
    print(product['name'])

# for product in soup.findAll('product-grid-element',attrs={'id':'grid-0'}):
#     print(product)
#     print(product.find('h2 _ngcontent-product-c3',attrs={'id':"product-0-title"}))

driver.quit()
###########
print("\nCountdown Total Execution Time: " + str((time.time()-t0)/60) + " minutes")