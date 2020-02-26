import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import ast
import os
import time

t0 = time.time()
# create list of paknsave catergories
categories = ['drinks','fresh-foods-and-bakery','chilled-frozen-and-desserts','pantry','drinks','beer-cider-and-wine','personal-care','baby-toddler-and-kids','pets','kitchen-dining-and-household']
# categories = ['drinks']

# initialize empty lists to store data
productName = []
unitPrice = []
category = []
image = []
pricingUnit= []
productId = []
quantity = []

for cat in categories:
###
    print(cat)
###
    req = Request("https://www.paknsaveonline.co.nz/category/"+cat, headers={'User-Agent': 'Mozilla/5.0'})
    content = urlopen(req)
    soup = BeautifulSoup(content,features="lxml")
    numPages = (int(soup.findAll('a', attrs={'class':"btn btn--tertiary btn--large fs-pagination__btn"})[-1].text))
    
    for pageNum in range(1,numPages+1):
        req = Request("https://www.paknsaveonline.co.nz/category/"+cat+'?pg='+str(pageNum), headers={'User-Agent': 'Mozilla/5.0'})
        content = urlopen(req)
        soup = BeautifulSoup(content,features="lxml")
###
        if(pageNum%5 == 0 or pageNum==1):
            print(pageNum)
###
        for a in soup.findAll('div',attrs={'class':'fs-product-card'}):
            card = a.find('div',attrs={'class','js-product-card-footer fs-product-card__footer-container'})
            dataOptions= card['data-options'] # note here dataOptions is a bs4 tag object/dictionary that contains information about product
            dataOptions = dataOptions.replace("\r","").replace("\n","").replace(" ","").replace("false","0").replace("true","0")
            productDetails = eval(dataOptions)['ProductDetails']

            category.append(cat)
            productId.append(eval(dataOptions)['productId'])
            unitPrice.append(float(productDetails["PricePerItem"]))
            productName.append(a.find('h3',attrs={'class':"u-p2"}).text.replace('\n','').replace('\r',''))
            pricingUnit.append(productDetails['PriceMode'])
            image.append(a.find('div',attrs={'class','fs-product-card__product-image'})['style'].replace("background-image: url('","").replace("')",""))
            quantity.append(a.find('p',attrs={'class','u-color-half-dark-grey u-p3'}).text)

    df = pd.DataFrame({'productId':productId,'productName':productName,'category':category,'quantity':quantity,'pricingUnit':pricingUnit,'unitPrice':unitPrice,'image':image})
    df.to_csv(os.path.expanduser("~/Desktop/SupermarketData/paknsave_"+cat+".csv"),index=False)
    productName = []
    unitPrice = []
    category = []
    image = []
    pricingUnit= []
    productId = []
    quantity=[]

print("Paknsave Total Execution Time: " + str((time.time()-t0)/60) + " minutes")
