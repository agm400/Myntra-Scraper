#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import math
from lxml import etree
import pandas as pd
import concurrent.futures

s = requests.Session()
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}
url = 'https://www.myntra.com/'
response = s.get(url, headers = headers, timeout = 10)



headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}
url = 'https://www.myntra.com/shop/home-living'
response = s.get(url, headers = headers, timeout = 10)



headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}
url = 'https://www.myntra.com/home-furnishing-menu?f=Categories%3ALamps%20Lanterns%20and%20Lamp%20Shades%3A%3Acategories%3ALamps%20Lanterns%20and%20Lamp%20Shades&p=3&plaEnabled=false'
response = s.get(url, headers = headers, timeout = 10)



headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}
url = 'https://www.myntra.com/gateway/v2/search/home-furnishing-menu?plaEnabled=false&rows=100&o=0'
response = s.get(url, headers = headers, timeout = 10)



data = json.loads(response.text)
data['products']

total_products = data['totalCount']
total_pages = math.ceil(total_products/len(data['products']))
data_final = []


def Scrapper(page_num):
    print(page_num)
    url_myntra = 'https://www.myntra.com/gateway/v2/search/home-furnishing-menu?plaEnabled=false&rows=100&o='+str(page_num*100)
    response_myntra = s.get(url_myntra, headers = headers, timeout = 10)
    data_myntra = json.loads(response_myntra.text)
    print(len(data_myntra['products']))
    for j in data_myntra['products']:
        #print(j)
        product_details = {}
        product_details['URL detail'] = 'https://www.myntra.com/'+j['landingPageUrl']
        product_details['Product ID'] = j['productId']
        product_details['Product'] = j['productName']
        product_details['Brand'] = j['brand']
        product_details['Price'] = j['price']
        product_details['Season'] = j['season']
        product_details['Sale'] = j['discountDisplayLabel']
        product_details['Category'] = j['category']
        product_details['Stock Keeping Unit ID'] = j['inventoryInfo'][0]['skuId']
        product_details['Images'] = [q['src'] for q in j['images']]

        
        #Making the Product Details section of the dictionary
        url_individual = product_details['URL detail']
        response_individual = s.get(url_individual, headers = headers, timeout = 10)        
        tree = etree.HTML(response_individual.text)
        details = tree.xpath("//body/script/text()")[2]
        details.split("myx = ")
        json_file = json.loads(details.split("myx = ")[1].strip())
        product_details['Product Details'] = [i['description'].replace("<br>"," ") for i in json_file['pdpData']['productDetails']]
        data_final.append(product_details)
        

for i in range(total_pages+1):
    Scrapper(i)


# In[ ]:




