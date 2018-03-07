from bs4 import BeautifulSoup

response = requests.get(url).text
parser = html.fromstring(response)
raw_wbsite_link = parser.xpath("//span[contains(@class,'biz-website')]/a/@href")

import csv
import requests
from lxml import html  
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
    
import requests
from bs4 import BeautifulSoup


for i in range(1, 101):
    file_name = "Fitness-Miami-{}.csv".format(str(i))
    with open(file_name, 'r') as f:
        next(f)
        read = csv.reader(f)
        new_row_list = []
        for row in read:
            new_row = []
            try:
                new_row = [row[0],row[1],row[2],row[3],row[4], row[5]]
            except:
                new_row = [row[0],row[1],row[2],row[3],row[4]]
            print(new_row)
            new_row_list.append(new_row)
    
    with open("fitness-miami-complete.csv", 'a') as f:
        writer = csv.writer(f)
        for row in new_row_list:
            writer.writerow(row)

