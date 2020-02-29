from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np

hashtag='food'
browser = webdriver.Chrome(r'C:\Users\Ritika Mangla\Desktop\chromedriver.exe')
browser.get('https://www.instagram.com/explore/tags/'+hashtag)
Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

links=[]
source = browser.page_source
data=bs(source, 'html.parser')
body = data.find('body')
script = body.find('span')
print(script)
for link in script.findAll('a', attrs={'href': re.compile("^http://")}):
     print("JII")
     if re.match("/p", link.get('href')):
        links.append('https://www.instagram.com'+link.get('href'))

        print(links)

links=["https://www.instagram.com/p/B8BehQfgx4v/"]
result = pd.DataFrame()
for i in range(len(links)):
    try:
        page = urlopen(links[i]).read()
        data = bs(page, 'html.parser')
        body = data.find('body')
        script = body.find('script')
        raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
        json_data = json.loads(raw)
        posts = json_data['entry_data']['PostPage'][0]['graphql']
        posts = json.dumps(posts)
        posts = json.loads(posts)
        x = pd.DataFrame.from_dict(json_normalize(posts), orient='columns')
        x.columns = x.columns.str.replace("shortcode_media.", "")
        result = result.append(x)
        print("in try")
        for i in json_data:
            print(json_data[i])
            print("\n")
        print("This is the entry data\n")
        print(json_data['entry_data'])

    except:
        print("in except")
        np.nan



print("\nThis is full data")
print(json_data)
result = result.drop_duplicates(subset='shortcode')
result.index = range(len(result.index))
#edge_media_to_caption': {'edges': [{'node': {'text':
#print(result)
