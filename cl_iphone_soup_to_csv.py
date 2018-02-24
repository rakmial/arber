'''scrape run hourly by cronie, creates data table with the following:
<timestamp>,<data_id>,<href>,<title_string>,<posted_datetime>,<price>

'''

import urllib.request
import csv
from bs4 import BeautifulSoup
import datetime

#open Humboldt County's iPhone query on craigslist
hum_iphone_url = "https://humboldt.craigslist.org/search/moa?query=iphone"
with urllib.request.urlopen(hum_iphone_url) as response:
   html = response.read()

soup = BeautifulSoup(html, 'html.parser')

#Extract data from different elements
date_boxes = soup.find_all('time', attrs={'class': 'result-date'})
date_times = [x['datetime'] for x in date_boxes]

title_boxes = soup.find_all('a', attrs={'class': 'result-title'})
data_ids = [x['data-id'] for x in title_boxes]
hrefs = [x['href'] for x in title_boxes]
title_strings = [x.string for x in title_boxes]

price_boxes = soup.find_all('span', attrs={'class': 'result-price'})
prices = [x.string for x in price_boxes]

#get a timestamp for each datum, then zip rounded int timestamp to row made of each datum collected
timestamps = [int(float(repr(datetime.datetime.today().timestamp()))) for i in range(len(data_ids))]
rows = list(zip(timestamps,data_ids,hrefs,title_strings,date_times,prices))
print(rows)

with open('../arber/hum_trade_data.csv','a',newline='') as csvfile:
    writer = csv.writer(csvfile,delimiter=',',quoting=csv.QUOTE_MINIMAL)
    writer.writerows(rows)
