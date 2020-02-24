import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import Request, urlopen
import ast

# initialize empty lists to store data
productName = []
unitPrice = []
category = []
image = []
pricingUnit=[]

req = Request("https://www.paknsaveonline.co.nz/category/personal-care", headers={'User-Agent': 'Mozilla/5.0'})
content = urlopen(req)
soup = BeautifulSoup(content,features="lxml")

print("start")
for a in soup.findAll('div',attrs={'class':'fs-product-card'}):
    card = a.find('div',attrs={'class','js-product-card-footer fs-product-card__footer-container'})
    productDetails= card['data-options']
    productDetails = productDetails.replace("\r","") ;productDetails = productDetails.replace("\n","");productDetails = productDetails.replace(" ","");productDetails = productDetails.replace("false","0")
    productDetails = eval(productDetails)['ProductDetails']

    unitPrice.append(productDetails["PricePerItem"])
    productName.append(a.find('h3',attrs={'class':"u-p2"}).text.replace('\n','').replace('\r',''))
    pricingUnit.append(productDetails['PriceMode'])
    image.append(a.find('div',attrs={'class','fs-product-card__product-image'})['style'])
print(pd.DataFrame({'productName':productName,'pricingUnit':pricingUnit,'unitPrice':unitPrice}))