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
packageType= []
volumeSize = []
categories = ['bakery','deli-chilled-foods','easter','fruit-vegetables','meat','seafood',
'baby-care','baking-cooking','biscuits-crackers','breakfast-foods','canned-prepared-foods',
'chocolate-sweets-snacks','cleaning-homecare','clothing-manchester','drinks-hot-cold','frozen-foods','health-wellness','home-kitchenware',
'liquor-beer-cider','liquor-wine','meal-ingredients','office-entertainment','personal-care','pet-care','toys-party-needs']

categories = ['deli-chilled-foods','easter','fruit-vegetables','meat','seafood',
'baby-care','baking-cooking','biscuits-crackers','breakfast-foods','canned-prepared-foods',
'chocolate-sweets-snacks','cleaning-homecare','clothing-manchester','drinks-hot-cold','frozen-foods','health-wellness','home-kitchenware',
'liquor-beer-cider','liquor-wine','meal-ingredients','office-entertainment','personal-care','pet-care','toys-party-needs']

for cat in categories:
    driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    driver.get("https://shop.countdown.co.nz/shop/browse/"+cat)
    content = driver.page_source
    soup = BeautifulSoup(content,features="lxml")
    pages = []
    for a in soup.findAll('li',attrs={'class':'page-number'}):
        pages.append((int(a.find('a').text)))
    numPages = max(pages);pages=None
    driver.quit()

    for pageNum in range(1,numPages+1):
        driver = webdriver.Chrome("/usr/local/bin/chromedriver")
        driver.get("https://shop.countdown.co.nz/shop/browse/"+cat+'?page='+str(pageNum))
        content = driver.page_source
        soup = BeautifulSoup(content,features="lxml")
        productGrid = soup.find('product-grid-element',id='grid-0')
        # print(productGrid)
        products = productGrid['products'].replace("null",'''"null"''').replace('false','False').replace('true','True')
        products = eval(products)

        for product in products:
            category.append(cat)
            productName.append(product['name'])
            productId.append(product['sku'])
            unitPrice.append(float(product['price']['salePrice']))
            image.append("https://shop.countdown.co.nz/"+product['images']['big'])
            pricingUnit.append(product['unit'])
            packageType.append(product['size']['packageType'])
            volumeSize.append(product['size']['packageType'])
        driver.quit()

    df = pd.DataFrame({'category':category,'productId':productId,'productName':productName,'packageType':packageType,'volumeSize':volumeSize,'pricingUnit':pricingUnit,'unitPrice':unitPrice,'image':image})
    df.to_csv(os.path.expanduser("~/Desktop/SupermarketData/Countdown/countdown_"+cat+".csv"),index=False)
    productName = []
    unitPrice = []
    category = []
    image = []
    pricingUnit= []
    productId = []
    packageType= []
    volumeSize = []

# driver.quit()
###########
print("\nCountdown Total Execution Time: " + str((time.time()-t0)/60) + " minutes")